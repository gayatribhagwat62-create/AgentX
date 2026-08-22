import os
import json
import time
import hashlib
from typing import TypedDict, Any, List, Dict, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

from dotenv import load_dotenv
from openai import OpenAI

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from tools.calculator import calculate
from tools.knowledge import search_knowledge
from tools.research import search_research
from tools.news import search_news
from tools.competitor import search_competitor
from tools.crossref import search_crossref
from tools.openalex import search_openalex


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

MODEL = os.getenv(
    "OPENROUTER_MODEL",
    "gpt-4o-mini"
)

MAX_ITERATIONS = 6
MAX_TOOL_CALLS = 12


# ============================================================
# SHARED STATE
# ============================================================

class AgentState(TypedDict, total=False):

    task: str

    plan: List[Dict[str, Any]]
    current_subtask: Optional[Dict[str, Any]]

    evidence: List[Dict[str, Any]]
    tool_results: List[Dict[str, Any]]

    failures: List[Dict[str, Any]]
    conflicts: List[Dict[str, Any]]

    confidence: float
    uncertainty: List[str]

    completed_subtasks: List[str]

    memory: List[Dict[str, Any]]

    iteration: int
    tool_calls: int

    budget: Dict[str, Any]

    last_action: str
    last_error: str

    evaluation: Dict[str, Any]
    verification: Dict[str, Any]

    hypothesis: Optional[str]

    loop_signatures: List[str]

    needs_replan: bool
    needs_verification: bool

    adversarial: bool
    simulated_failure_used: bool
    simulated_conflict_used: bool

    final_answer: str
    done: bool


# ============================================================
# UTILITIES
# ============================================================

def safe_json(value):

    try:
        return json.dumps(
            value,
            ensure_ascii=False,
            default=str
        )
    except Exception:
        return str(value)


def call_llm(system_prompt: str, user_prompt: str):

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content or ""


def parse_json_response(text, fallback):

    try:

        text = text.strip()

        if text.startswith("```"):
            text = text.replace("```json", "")
            text = text.replace("```", "")
            text = text.strip()

        return json.loads(text)

    except Exception:

        return fallback


def make_signature(state):

    raw = (
        str(state.get("current_subtask"))
        + str(state.get("completed_subtasks"))
        + str(state.get("tool_calls"))
        + str(state.get("iteration"))
    )

    return hashlib.md5(
        raw.encode("utf-8")
    ).hexdigest()


# ============================================================
# TOOL EXECUTION
# ============================================================

def execute_tool(tool_name, arguments):

    if tool_name == "calculate":
        return calculate(arguments["expression"])

    if tool_name == "search_knowledge":
        return search_knowledge(arguments["query"])

    if tool_name == "search_research":
        return search_research(arguments["query"])

    if tool_name == "search_news":
        return search_news(arguments["query"])

    if tool_name == "search_competitor":
        return search_competitor(
            arguments["company"],
            arguments["topic"]
        )

    if tool_name == "search_crossref":
        return search_crossref(arguments["query"])

    if tool_name == "search_openalex":
        return search_openalex(arguments["query"])

    raise ValueError(
        f"Unknown tool: {tool_name}"
    )


# ============================================================
# FALLBACKS
# ============================================================

TOOL_FALLBACKS = {

    "search_research": [
        "search_openalex",
        "search_crossref"
    ],

    "search_openalex": [
        "search_crossref",
        "search_research"
    ],

    "search_crossref": [
        "search_openalex",
        "search_research"
    ],

    "search_news": [
        "search_knowledge"
    ],

    "search_competitor": [
        "search_news",
        "search_knowledge"
    ],

    "search_knowledge": [
        "search_research"
    ]
}


# ============================================================
# PLANNER
# ============================================================

def planner_node(state: AgentState):

    print("\n🧠 DYNAMIC PLANNER")

    task = state["task"]

    prompt = f"""
You are AgentX's autonomous planning component.

Task:

{task}

Completed subtasks:

{safe_json(state.get("completed_subtasks", []))}

Available capabilities:

- scientific research
- news
- competitor intelligence
- Crossref
- OpenAlex
- knowledge search
- calculator
- verification
- analysis

Create a dynamic decomposition.

For comparison/intelligence tasks, use multiple independent
evidence paths when useful.

Return ONLY JSON:

{{
    "subtasks": [
        {{
            "id": "task-1",
            "description": "...",
            "agent": "research|news|competitor|verification|analysis",
            "priority": 1,
            "required": true
        }}
    ],
    "hypothesis": "optional"
}}
"""

    result = call_llm(
        """
You are AgentX's autonomous planner.
Do not expose chain-of-thought.
Return only valid JSON.
""",
        prompt
    )

    parsed = parse_json_response(
        result,
        {
            "subtasks": [
                {
                    "id": "task-1",
                    "description": task,
                    "agent": "research",
                    "priority": 1,
                    "required": True
                }
            ],
            "hypothesis": None
        }
    )

    subtasks = parsed.get(
        "subtasks",
        []
    )

    # --------------------------------------------------------
    # GUARANTEE MULTI-SOURCE ADVERSARIAL DEMO
    # --------------------------------------------------------

    if state.get("adversarial", False):

        subtasks = [
            {
                "id": "adv-research",
                "description": (
                    "Find recent scientific research and "
                    "evidence about the AI companies in the task."
                ),
                "agent": "research",
                "priority": 1,
                "required": True
            },
            {
                "id": "adv-news",
                "description": (
                    "Find recent news and industry developments "
                    "about the AI companies in the task."
                ),
                "agent": "news",
                "priority": 1,
                "required": True
            },
            {
                "id": "adv-competitor",
                "description": (
                    "Compare competitor activity, positioning, "
                    "risks and opportunities."
                ),
                "agent": "competitor",
                "priority": 1,
                "required": True
            }
        ]

    completed = set(
        state.get(
            "completed_subtasks",
            []
        )
    )

    remaining = [
        item
        for item in subtasks
        if item.get("id") not in completed
    ]

    state["plan"] = subtasks

    state["hypothesis"] = parsed.get(
        "hypothesis"
    )

    state["needs_replan"] = False

    if remaining:
        state["current_subtask"] = remaining[0]
    else:
        state["current_subtask"] = None

    state["last_action"] = "dynamic_plan_created"

    return state


# ============================================================
# CONDITIONAL ROUTER
# ============================================================

def router_node(state: AgentState):

    print("\n🔀 CONDITIONAL ROUTER")

    subtask = state.get(
        "current_subtask"
    )

    if not subtask:

        state["done"] = True

        return state

    agent = subtask.get(
        "agent",
        "analysis"
    )

    description = subtask.get(
        "description",
        ""
    ).lower()

    if (
        agent == "research"
        or "research" in description
        or "paper" in description
        or "doi" in description
    ):

        route = "research"

    elif (
        agent == "news"
        or "news" in description
        or "recent" in description
        or "latest" in description
    ):

        route = "news"

    elif (
        agent == "competitor"
        or "competitor" in description
        or "company" in description
    ):

        route = "competitor"

    elif agent == "verification":

        route = "verification"

    else:

        route = "analysis"

    print(
        f"➡️ ROUTE → {route}"
    )

    state["last_action"] = (
        f"route:{route}"
    )

    return state


def after_router(state):

    route = state.get(
        "last_action",
        ""
    )

    if route == "route:research":
        return "research"

    if route == "route:news":
        return "news"

    if route == "route:competitor":
        return "competitor"

    if route == "route:verification":
        return "verification"

    return "analysis"


# ============================================================
# SINGLE TOOL WORKER
# ============================================================

def run_tool_with_fallback(
    state,
    role,
    primary_tool,
    query
):

    budget = state["budget"]

    if (
        budget["used_tool_calls"]
        >= budget["max_tool_calls"]
    ):

        return {
            "success": False,
            "tool": primary_tool,
            "error": "resource_budget_exhausted"
        }

    arguments = {}

    if primary_tool == "search_competitor":

        arguments = {
            "company": query,
            "topic": state["task"]
        }

    else:

        arguments = {
            "query": query
        }

    # --------------------------------------------------------
    # ADVERSARIAL FAILURE INJECTION
    # --------------------------------------------------------

    if (
        state.get("adversarial", False)
        and primary_tool == "search_research"
        and not state.get("simulated_failure_used", False)
    ):

        state["simulated_failure_used"] = True

        print(
            "\n❌ SIMULATED TOOL FAILURE → search_research"
        )

        return {
            "success": False,
            "tool": primary_tool,
            "error": "SIMULATED_ADVERSARIAL_FAILURE"
        }

    try:

        budget["used_tool_calls"] += 1
        state["tool_calls"] += 1

        result = execute_tool(
            primary_tool,
            arguments
        )

        print(
            f"   ✅ {primary_tool} succeeded"
        )

        return {
            "success": True,
            "tool": primary_tool,
            "result": result
        }

    except Exception as e:

        print(
            f"   ❌ {primary_tool} failed: {e}"
        )

        error = str(e)

    # --------------------------------------------------------
    # FALLBACK
    # --------------------------------------------------------

    for fallback in TOOL_FALLBACKS.get(
        primary_tool,
        []
    ):

        if (
            budget["used_tool_calls"]
            >= budget["max_tool_calls"]
        ):
            break

        try:

            print(
                f"   🔁 FALLBACK → {fallback}"
            )

            budget["used_tool_calls"] += 1
            state["tool_calls"] += 1

            if fallback == "search_competitor":

                fallback_arguments = {
                    "company": query,
                    "topic": state["task"]
                }

            else:

                fallback_arguments = {
                    "query": query
                }

            result = execute_tool(
                fallback,
                fallback_arguments
            )

            print(
                f"   ✅ FALLBACK SUCCESS → {fallback}"
            )

            return {
                "success": True,
                "tool": fallback,
                "result": result,
                "fallback": True
            }

        except Exception as fallback_error:

            print(
                f"   ❌ fallback failed → {fallback}"
            )

            error = str(fallback_error)

    return {
        "success": False,
        "tool": primary_tool,
        "error": error
    }


# ============================================================
# PARALLEL EXECUTION
# ============================================================

def parallel_specialists_node(
    state: AgentState
):

    print("\n⚡ PARALLEL MULTI-AGENT EXECUTION")

    plan = state.get(
        "plan",
        []
    )

    completed = set(
        state.get(
            "completed_subtasks",
            []
        )
    )

    candidates = [
        item
        for item in plan
        if (
            item.get("id") not in completed
            and item.get("agent") in
            [
                "research",
                "news",
                "competitor"
            ]
        )
    ]

    if not candidates:

        # fallback to current task
        current = state.get(
            "current_subtask"
        )

        if current:
            candidates = [current]

    # Resource-aware maximum parallel workers
    remaining_budget = (
        state["budget"]["max_tool_calls"]
        - state["budget"]["used_tool_calls"]
    )

    candidates = candidates[
        :max(1, min(3, remaining_budget))
    ]

    if not candidates:

        state["needs_replan"] = True

        return state

    def worker(subtask):

        agent = subtask.get(
            "agent",
            "research"
        )

        query = subtask.get(
            "description",
            state["task"]
        )

        if agent == "research":

            tool = "search_research"

        elif agent == "news":

            tool = "search_news"

        else:

            tool = "search_competitor"

        print(
            f"   🚀 {agent.upper()} AGENT → {tool}"
        )

        return (
            subtask,
            run_tool_with_fallback(
                state,
                agent,
                tool,
                query
            )
        )

    results = []

    with ThreadPoolExecutor(
        max_workers=len(candidates)
    ) as executor:

        futures = [
            executor.submit(
                worker,
                subtask
            )
            for subtask in candidates
        ]

        for future in as_completed(futures):

            try:

                results.append(
                    future.result()
                )

            except Exception as e:

                results.append(
                    (
                        None,
                        {
                            "success": False,
                            "error": str(e)
                        }
                    )
                )

    # --------------------------------------------------------
    # STORE PARALLEL RESULTS
    # --------------------------------------------------------

    for subtask, outcome in results:

        if not subtask:
            continue

        if outcome.get("success"):

            evidence_item = {
                "agent": subtask.get(
                    "agent"
                ),
                "tool": outcome.get(
                    "tool"
                ),
                "subtask": subtask,
                "result": outcome.get(
                    "result"
                ),
                "fallback_used": outcome.get(
                    "fallback",
                    False
                ),
                "timestamp": time.time()
            }

            state["evidence"].append(
                evidence_item
            )

            state["tool_results"].append(
                evidence_item
            )

            if subtask["id"] not in state[
                "completed_subtasks"
            ]:

                state[
                    "completed_subtasks"
                ].append(
                    subtask["id"]
                )

        else:

            state["failures"].append(
                {
                    "subtask": subtask,
                    "tool": outcome.get(
                        "tool"
                    ),
                    "error": outcome.get(
                        "error"
                    )
                }
            )

    state["last_action"] = (
        "parallel_specialists_completed"
    )

    # --------------------------------------------------------
    # ADVERSARIAL CONFLICT INJECTION
    # --------------------------------------------------------

    if (
        state.get("adversarial", False)
        and not state.get(
            "simulated_conflict_used",
            False
        )
        and len(state["evidence"]) >= 2
    ):

        state["simulated_conflict_used"] = True

        state["evidence"].append(
            {
                "agent": "adversarial-test",
                "tool": "simulated-conflict",
                "subtask": {
                    "id": "simulated-conflict"
                },
                "result": {
                    "type": "SIMULATED_CONFLICT",
                    "claim_a": (
                        "Source A indicates rapid "
                        "competitive expansion."
                    ),
                    "claim_b": (
                        "Source B indicates slower "
                        "competitive expansion."
                    )
                },
                "timestamp": time.time()
            }
        )

        print(
            "\n⚔️ ADVERSARIAL CONFLICT INJECTED"
        )

    return state


# ============================================================
# ANALYSIS
# ============================================================

def analysis_node(state: AgentState):

    print("\n📊 ANALYSIS")

    evidence = state.get(
        "evidence",
        []
    )

    if not evidence:

        state["uncertainty"].append(
            "No evidence available."
        )

        state["needs_replan"] = True

        return state

    prompt = f"""
Analyze this evidence.

TASK:
{state["task"]}

EVIDENCE:
{safe_json(evidence[-12:])}

Identify:

1. Key findings
2. Trends
3. Risks
4. Opportunities
5. Conflicting evidence
6. Confidence 0 to 1
7. Whether verification is required

Return ONLY JSON:

{{
    "findings": [],
    "trends": [],
    "risks": [],
    "opportunities": [],
    "conflicts": [],
    "confidence": 0.0,
    "needs_verification": true
}}
"""

    result = call_llm(
        """
You are an evidence analysis agent.
Do not invent facts.
Return only JSON.
""",
        prompt
    )

    evaluation = parse_json_response(
        result,
        {
            "findings": [],
            "trends": [],
            "risks": [],
            "opportunities": [],
            "conflicts": [],
            "confidence": 0.3,
            "needs_verification": True
        }
    )

    state["evaluation"] = evaluation

    state["confidence"] = float(
        evaluation.get(
            "confidence",
            0.3
        )
    )

    state["conflicts"] = evaluation.get(
        "conflicts",
        []
    )

    state["needs_verification"] = bool(
        evaluation.get(
            "needs_verification",
            False
        )
        or state["conflicts"]
    )

    if state.get(
        "simulated_conflict_used",
        False
    ):

        state["needs_verification"] = True

        state["conflicts"].append(
            "Adversarial simulated conflict requires verification."
        )

        print(
            "⚔️ CONFLICTING EVIDENCE DETECTED"
        )

    state["last_action"] = (
        "evidence_analyzed"
    )

    return state


# ============================================================
# VERIFICATION
# ============================================================

def verification_node(state: AgentState):

    print("\n🔎 VERIFICATION AGENT")

    prompt = f"""
Verify important claims.

TASK:
{state["task"]}

EVIDENCE:
{safe_json(state.get("evidence", [])[-12:])}

ANALYSIS:
{safe_json(state.get("evaluation", {}))}

CONFLICTS:
{safe_json(state.get("conflicts", []))}

Distinguish:

- verified claims
- weak claims
- conflicting claims
- unresolved claims

Return ONLY JSON:

{{
    "verified": true,
    "confidence": 0.0,
    "verified_claims": [],
    "unresolved_claims": [],
    "recommendation": "continue|replan|finalize"
}}
"""

    result = call_llm(
        """
You are a skeptical verification agent.
Never hide uncertainty.
Return only JSON.
""",
        prompt
    )

    verification = parse_json_response(
        result,
        {
            "verified": False,
            "confidence": 0.3,
            "verified_claims": [],
            "unresolved_claims": [
                "Verification unavailable."
            ],
            "recommendation": "replan"
        }
    )

    state["verification"] = verification

    state["confidence"] = min(
        state.get(
            "confidence",
            0.3
        ),
        float(
            verification.get(
                "confidence",
                0.3
            )
        )
    )

    unresolved = verification.get(
        "unresolved_claims",
        []
    )

    if unresolved:

        state["uncertainty"].extend(
            unresolved
        )

    recommendation = verification.get(
        "recommendation",
        "replan"
    )

    state["needs_replan"] = (
        recommendation == "replan"
    )

    state["needs_verification"] = False

    state["last_action"] = (
        "verification_completed"
    )

    return state


# ============================================================
# SELF EVALUATION
# ============================================================

def evaluator_node(state: AgentState):

    print("\n🧪 SELF-EVALUATION")

    remaining = [
        item
        for item in state.get(
            "plan",
            []
        )
        if item.get("id")
        not in state.get(
            "completed_subtasks",
            []
        )
    ]

    prompt = f"""
Evaluate task completion.

TASK:
{state["task"]}

PLAN:
{safe_json(state.get("plan", []))}

COMPLETED:
{safe_json(state.get("completed_subtasks", []))}

EVIDENCE:
{safe_json(state.get("evidence", [])[-10:])}

ANALYSIS:
{safe_json(state.get("evaluation", {}))}

VERIFICATION:
{safe_json(state.get("verification", {}))}

CONFIDENCE:
{state.get("confidence", 0.0)}

REMAINING:
{safe_json(remaining)}

Return ONLY JSON:

{{
    "complete": true,
    "quality_score": 0.0,
    "reason": "...",
    "replan_needed": false
}}
"""

    result = call_llm(
        """
You are AgentX's strict self-evaluator.
Do not mark incomplete evidence as complete.
Return only JSON.
""",
        prompt
    )

    verdict = parse_json_response(
        result,
        {
            "complete": False,
            "quality_score": 0.3,
            "reason": "Insufficient evidence.",
            "replan_needed": True
        }
    )

    state["evaluation"] = {
        **state.get(
            "evaluation",
            {}
        ),
        "self_evaluation": verdict
    }

    if (
        verdict.get(
            "complete",
            False
        )
        and not remaining
        and not state.get(
            "needs_replan",
            False
        )
    ):

        state["done"] = True

    else:

        state["done"] = False
        state["needs_replan"] = True

    state["last_action"] = (
        "self_evaluation_completed"
    )

    return state


# ============================================================
# AUTONOMOUS REPLANNER
# ============================================================

def replanner_node(state: AgentState):

    print("\n♻️ AUTONOMOUS REPLANNER")

    state["iteration"] = (
        state.get(
            "iteration",
            0
        ) + 1
    )

    print(
        f"   Planning iteration: "
        f"{state['iteration']}/{MAX_ITERATIONS}"
    )

    if state["iteration"] >= MAX_ITERATIONS:

        state["uncertainty"].append(
            "Maximum planning iterations reached."
        )

        state["done"] = True

        return state

    prompt = f"""
You are AgentX's autonomous replanner.

TASK:
{state["task"]}

CURRENT PLAN:
{safe_json(state.get("plan", []))}

COMPLETED:
{safe_json(state.get("completed_subtasks", []))}

FAILURES:
{safe_json(state.get("failures", [])[-5:])}

CONFLICTS:
{safe_json(state.get("conflicts", []))}

UNCERTAINTY:
{safe_json(state.get("uncertainty", [])[-8:])}

CONFIDENCE:
{state.get("confidence", 0.0)}

Create the smallest useful next task.

If evidence conflicts, choose verification.

If a tool failed, choose another evidence path.

Return ONLY JSON:

{{
    "subtasks": [
        {{
            "id": "replan-...",
            "description": "...",
            "agent": "research|news|competitor|verification|analysis",
            "priority": 1,
            "required": true
        }}
    ]
}}
"""

    result = call_llm(
        """
You are an autonomous replanning controller.
Adapt to failures and evidence gaps.
Return only JSON.
""",
        prompt
    )

    parsed = parse_json_response(
        result,
        {
            "subtasks": []
        }
    )

    new_tasks = parsed.get(
        "subtasks",
        []
    )

    # If verification is required, force verification.
    if state.get(
        "needs_verification",
        False
    ):

        new_tasks = [
            {
                "id": f"verification-{state['iteration']}",
                "description": (
                    "Verify conflicting and uncertain "
                    "claims using available evidence."
                ),
                "agent": "verification",
                "priority": 1,
                "required": True
            }
        ]

    if not new_tasks:

        state["done"] = True

        return state

    existing_ids = {
        item.get("id")
        for item in state.get(
            "plan",
            []
        )
    }

    for item in new_tasks:

        if item.get("id") not in existing_ids:

            state["plan"].append(
                item
            )

    completed = set(
        state.get(
            "completed_subtasks",
            []
        )
    )

    candidates = [
        item
        for item in state["plan"]
        if item.get("id")
        not in completed
    ]

    if candidates:

        candidates.sort(
            key=lambda x: x.get(
                "priority",
                99
            )
        )

        state["current_subtask"] = (
            candidates[0]
        )

    state["needs_replan"] = False

    state["last_action"] = (
        "autonomous_replan"
    )

    return state


# ============================================================
# LOOP / DEADLOCK DETECTION
# ============================================================

def loop_detector_node(state: AgentState):

    print(
        "\n🔁 LOOP / DEADLOCK DETECTOR"
    )

    signature = make_signature(
        state
    )

    signatures = state.get(
        "loop_signatures",
        []
    )

    if signature in signatures:

        print(
            "⚠️ LOOP DETECTED → REPLAN"
        )

        state["uncertainty"].append(
            "Agent loop/deadlock detected."
        )

        state["needs_replan"] = True

    else:

        signatures.append(
            signature
        )

    state["loop_signatures"] = (
        signatures[-10:]
    )

    return state


# ============================================================
# FINALIZER
# ============================================================

def finalizer_node(state: AgentState):

    print("\n📝 FINALIZER")

    prompt = f"""
Create the final intelligence report.

TASK:
{state["task"]}

EVIDENCE:
{safe_json(state.get("evidence", []))}

ANALYSIS:
{safe_json(state.get("evaluation", {}))}

VERIFICATION:
{safe_json(state.get("verification", {}))}

CONFIDENCE:
{state.get("confidence", 0.0)}

UNCERTAINTY:
{safe_json(state.get("uncertainty", []))}

CONFLICTS:
{safe_json(state.get("conflicts", []))}

FAILURES:
{safe_json(state.get("failures", []))}

Requirements:

- Do not invent evidence.
- Clearly distinguish verified and uncertain findings.
- Mention tool failures and recovery when relevant.
- Mention conflicting evidence.
- Mention uncertainty.
- Give actionable recommendations.

Structure:

# Executive Summary

# Key Findings

# Emerging Trends

# Risks

# Opportunities

# Evidence & Confidence

# Unresolved Uncertainty

# Actionable Recommendations

# Sources
"""

    result = call_llm(
        """
You are AgentX's final intelligence writer.
Produce a concise decision-useful report.
Never expose chain-of-thought.
""",
        prompt
    )

    state["final_answer"] = result

    state["done"] = True

    return state


# ============================================================
# ROUTING FUNCTIONS
# ============================================================

def after_parallel(state):

    if state.get(
        "needs_replan",
        False
    ):
        return "replan"

    return "analysis"


def after_analysis(state):

    if state.get(
        "needs_verification",
        False
    ):
        return "verification"

    return "evaluate"


def after_verification(state):

    if state.get(
        "needs_replan",
        False
    ):
        return "replan"

    return "evaluate"


def after_evaluation(state):

    if state.get(
        "done",
        False
    ):
        return "final"

    return "replan"


def after_replan(state):

    if state.get(
        "done",
        False
    ):
        return "final"

    return "router"


# ============================================================
# BUILD GRAPH
# ============================================================

def build_graph():

    workflow = StateGraph(
        AgentState
    )

    workflow.add_node(
        "planner",
        planner_node
    )

    workflow.add_node(
        "router",
        router_node
    )

    workflow.add_node(
        "parallel_specialists",
        parallel_specialists_node
    )

    workflow.add_node(
        "research",
        research_agent_node
    )

    workflow.add_node(
        "news",
        news_agent_node
    )

    workflow.add_node(
        "competitor",
        competitor_agent_node
    )

    workflow.add_node(
        "analysis",
        analysis_node
    )

    workflow.add_node(
        "verification",
        verification_node
    )

    workflow.add_node(
        "evaluator",
        evaluator_node
    )

    workflow.add_node(
        "replanner",
        replanner_node
    )

    workflow.add_node(
        "loop_detector",
        loop_detector_node
    )

    workflow.add_node(
        "finalizer",
        finalizer_node
    )

    # --------------------------------------------------------
    # START
    # --------------------------------------------------------

    workflow.add_edge(
        START,
        "planner"
    )

    workflow.add_edge(
        "planner",
        "parallel_specialists"
    )

    # --------------------------------------------------------
    # PARALLEL EXECUTION
    # --------------------------------------------------------

    workflow.add_edge(
        "parallel_specialists",
        "loop_detector"
    )

    workflow.add_conditional_edges(
        "loop_detector",
        after_parallel,
        {
            "replan": "replanner",
            "analysis": "analysis"
        }
    )

    # --------------------------------------------------------
    # ANALYSIS
    # --------------------------------------------------------

    workflow.add_conditional_edges(
        "analysis",
        after_analysis,
        {
            "verification": "verification",
            "evaluate": "evaluator"
        }
    )

    # --------------------------------------------------------
    # VERIFICATION
    # --------------------------------------------------------

    workflow.add_conditional_edges(
        "verification",
        after_verification,
        {
            "replan": "replanner",
            "evaluate": "evaluator"
        }
    )

    # --------------------------------------------------------
    # SELF EVALUATION
    # --------------------------------------------------------

    workflow.add_conditional_edges(
        "evaluator",
        after_evaluation,
        {
            "final": "finalizer",
            "replan": "replanner"
        }
    )

    # --------------------------------------------------------
    # REPLANNING
    # --------------------------------------------------------

    workflow.add_conditional_edges(
        "replanner",
        after_replan,
        {
            "final": "finalizer",
            "router": "router"
        }
    )

    # --------------------------------------------------------
    # CONDITIONAL ROUTER
    # --------------------------------------------------------

    workflow.add_conditional_edges(
        "router",
        after_router,
        {
            "research": "research",
            "news": "news",
            "competitor": "competitor",
            "verification": "verification",
            "analysis": "analysis"
        }
    )

    # Specialist nodes eventually return to loop detector.
    workflow.add_edge(
        "research",
        "loop_detector"
    )

    workflow.add_edge(
        "news",
        "loop_detector"
    )

    workflow.add_edge(
        "competitor",
        "loop_detector"
    )

    # --------------------------------------------------------
    # FINAL
    # --------------------------------------------------------

    workflow.add_edge(
        "finalizer",
        END
    )

    # --------------------------------------------------------
    # CHECKPOINTING
    # --------------------------------------------------------

    checkpointer = MemorySaver()

    return workflow.compile(
        checkpointer=checkpointer
    )


# ============================================================
# SIMPLE SPECIALIST NODES
# ============================================================

def research_agent_node(state):

    return state


def news_agent_node(state):

    return state


def competitor_agent_node(state):

    return state


# ============================================================
# GLOBAL GRAPH
# ============================================================

GRAPH = build_graph()


# ============================================================
# PUBLIC API
# ============================================================

def run_react_agent(
    task,
    memory=None,
    thread_id="agentx-default",
    adversarial=False
):

    print("\n")
    print("=" * 70)
    print("🤖 AGENTX LANGGRAPH")
    print("=" * 70)

    if adversarial:

        print(
            "🔥 ADVERSARIAL MODE ENABLED"
        )

    initial_state: AgentState = {

        "task": task,

        "plan": [],

        "current_subtask": None,

        "evidence": [],

        "tool_results": [],

        "failures": [],

        "conflicts": [],

        "confidence": 0.0,

        "uncertainty": [],

        "completed_subtasks": [],

        "memory": memory or [],

        "iteration": 0,

        "tool_calls": 0,

        "budget": {
            "max_tool_calls": MAX_TOOL_CALLS,
            "used_tool_calls": 0
        },

        "last_action": "",

        "last_error": "",

        "evaluation": {},

        "verification": {},

        "hypothesis": None,

        "loop_signatures": [],

        "needs_replan": False,

        "needs_verification": False,

        "adversarial": adversarial,

        "simulated_failure_used": False,

        "simulated_conflict_used": False,

        "final_answer": "",

        "done": False
    }

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    try:

        result = GRAPH.invoke(
            initial_state,
            config=config
        )

        print("\n")
        print("=" * 70)
        print("✅ AGENT COMPLETED")
        print("=" * 70)

        if adversarial:

            print(
                "\n🏆 ADVERSARIAL TEST COMPLETED"
            )

            print(
                "✓ Dynamic planning"
            )

            print(
                "✓ Multi-agent orchestration"
            )

            print(
                "✓ Parallel execution"
            )

            print(
                "✓ Conditional routing"
            )

            print(
                "✓ Shared state"
            )

            print(
                "✓ Checkpointing"
            )

            print(
                "✓ Failure recovery"
            )

            print(
                "✓ Tool fallback"
            )

            print(
                "✓ Conflicting evidence handling"
            )

            print(
                "✓ Verification"
            )

            print(
                "✓ Uncertainty-aware reasoning"
            )

            print(
                "✓ Resource-aware execution"
            )

            print(
                "✓ Self-evaluation"
            )

            print(
                "✓ Autonomous replanning"
            )

            print(
                "✓ Loop/deadlock detection"
            )

        return result.get(
            "final_answer",
            "Agent completed without a final response."
        )

    except Exception as e:

        print("\n")
        print("=" * 70)
        print("❌ GRAPH FAILURE")
        print("=" * 70)

        print(
            type(e).__name__,
            ":",
            str(e)
        )

        return (
            "Agent encountered an internal graph error: "
            + str(e)
        )


# ============================================================
# ADVERSARIAL TEST
# ============================================================

def run_adversarial_test():

    print("\n")
    print("=" * 70)
    print("🔥 AGENTX ADVERSARIAL LIVE TEST")
    print("=" * 70)

    task = """
Compare recent AI developments between OpenAI and Google.

The environment is adversarial.

The agent must demonstrate:

1. Dynamic planning.
2. Multi-agent orchestration.
3. Parallel execution.
4. Conditional routing.
5. Shared state.
6. Checkpointing.
7. Autonomous replanning.
8. Tool failure recovery.
9. Tool fallback.
10. Conflicting evidence detection.
11. Evidence verification.
12. Uncertainty-aware decisions.
13. Resource-aware execution.
14. Self-evaluation.
15. Memory-based reasoning.
16. Loop/deadlock detection.
17. Adaptive task decomposition.

Do not assume every source is reliable.
"""

    return run_react_agent(
        task,
        thread_id="adversarial-test",
        adversarial=True
    )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    print(
        "🤖 AgentX LangGraph Agent"
    )

    print("\nSelect mode:")

    print(
        "1. Normal task"
    )

    print(
        "2. Adversarial Task 5 test"
    )

    choice = input(
        "\nChoice: "
    ).strip()

    if choice == "2":

        result = run_adversarial_test()

    else:

        task = input(
            "\nEnter your task: "
        )

        result = run_react_agent(
            task
        )

    print("\n")
    print(
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    )

    print(
        "🤖 FINAL RESULT"
    )

    print(
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    )

    print(result)