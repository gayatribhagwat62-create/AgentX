import os
import json

from dotenv import load_dotenv
from openai import OpenAI

from tools.calculator import calculate
from tools.knowledge import search_knowledge
from tools.research import search_research
from tools.news import search_news
from tools.competitor import search_competitor


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

MAX_STEPS = 8


# ============================================================
# TOOLS AVAILABLE TO THE AGENT
# ============================================================

TOOLS = [

    # --------------------------------------------------------
    # Calculator
    # --------------------------------------------------------

    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Calculate a mathematical expression.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string"
                    }
                },
                "required": ["expression"]
            }
        }
    },

    # --------------------------------------------------------
    # Knowledge
    # --------------------------------------------------------

    {
        "type": "function",
        "function": {
            "name": "search_knowledge",
            "description": "Search the local knowledge base.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string"
                    }
                },
                "required": ["query"]
            }
        }
    },

    # --------------------------------------------------------
    # Research
    # --------------------------------------------------------

    {
        "type": "function",
        "function": {
            "name": "search_research",
            "description": "Search scientific research papers about a topic.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Research topic"
                    }
                },
                "required": ["query"]
            }
        }
    },

    # --------------------------------------------------------
    # News
    # --------------------------------------------------------

    {
        "type": "function",
        "function": {
            "name": "search_news",
            "description": "Search recent developments and news related to a topic.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Topic to search for recent developments"
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
    "type": "function",
    "function": {
        "name": "search_competitor",
        "description": "Track research and recent activity related to a competitor.",
        "parameters": {
            "type": "object",
            "properties": {
                "company": {
                    "type": "string",
                    "description": "Competitor company name"
                },
                "topic": {
                    "type": "string",
                    "description": "Topic to investigate"
                }
            },
            "required": ["company", "topic"]
        }
    }
}
]


# ============================================================
# REACT AGENT
# ============================================================

def run_react_agent(task):

    messages = [

        # ----------------------------------------------------
        # SYSTEM
        # ----------------------------------------------------

        {
            "role": "system",
            "content": """
You are AgentX, an autonomous research and competitive
intelligence AI agent.

Your job is to understand the user's goal, decide what
information is required, use the appropriate tools, observe
their results, and continue until the task is sufficiently
completed.

You MUST behave like an agent, not like a simple chatbot.

Available tools:

1. calculate
   Use for mathematical calculations.

2. search_knowledge
   Use for information stored in the local knowledge base.

3. search_research
   Use for scientific research papers and academic developments.

4. search_news
   Use for recent industry developments and news.

------------------------------------------------------------
AGENTIC PROCESS
------------------------------------------------------------

Follow this pattern:

DECIDE
→ ACT
→ OBSERVE
→ DECIDE AGAIN
→ ACT
→ OBSERVE
→ ANALYZE
→ FINAL RESULT

Do not simply say that you are searching.

When research intelligence is requested:

1. Search relevant research.
2. Search recent developments/news.
3. Observe the results.
4. Decide whether more information is needed.
5. Compare and analyze the collected information.
6. Identify important trends.
7. Identify risks and opportunities.
8. Prioritize important findings.
9. Give actionable recommendations.

Do NOT return raw search results only.

The final answer should be concise but useful.

For intelligence tasks, structure the final response as:

Executive Summary

Key Findings

Emerging Trends

Risks

Opportunities

Priority

Actionable Recommendations

Sources

Do not reveal private chain-of-thought.
Only show short action/status messages.
"""
        },

        # ----------------------------------------------------
        # USER TASK
        # ----------------------------------------------------

        {
            "role": "user",
            "content": task
        }
    ]


    # ========================================================
    # REACT LOOP
    # ========================================================

    for step in range(1, MAX_STEPS + 1):

        print(f"\n🧠 Agent Step {step}")

        try:

            response = client.chat.completions.create(
                model="openrouter/free",
                messages=messages,
                tools=TOOLS,
                tool_choice="auto"
            )

        except Exception as e:

            print("\n❌ AI API Error:")
            print(e)

            return "Agent failed because of an AI API error."


        message = response.choices[0].message


        # ====================================================
        # NO TOOL CALL = FINAL ANSWER
        # ====================================================

        if not message.tool_calls:

            print("✅ Task completed")

            return message.content


        # ====================================================
        # ADD ASSISTANT TOOL CALL TO CONVERSATION
        # ====================================================

        messages.append(message)


        # ====================================================
        # EXECUTE TOOLS
        # ====================================================

        for tool_call in message.tool_calls:

            tool_name = tool_call.function.name

            try:

                arguments = json.loads(
                    tool_call.function.arguments
                )

            except json.JSONDecodeError:

                result = {
                    "error": "Invalid tool arguments"
                }

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(result)
                    }
                )

                continue


            print(f"🔧 Action: {tool_name}")


            # =================================================
            # CALCULATOR
            # =================================================

            if tool_name == "calculate":

                expression = arguments["expression"]

                result = calculate(expression)

                print(
                    f"👀 Observation: {result}"
                )


            # =================================================
            # KNOWLEDGE
            # =================================================

            elif tool_name == "search_knowledge":

                query = arguments["query"]

                result = search_knowledge(query)

                print(
                    "👀 Observation: Knowledge retrieved"
                )


            # =================================================
            # RESEARCH
            # =================================================

            elif tool_name == "search_research":

                query = arguments["query"]

                result = search_research(query)

                if isinstance(result, list):

                    print(
                        f"👀 Observation: "
                        f"{len(result)} research results found"
                    )

                else:

                    print(
                        f"👀 Observation: {result}"
                    )


            # =================================================
            # NEWS
            # =================================================

            elif tool_name == "search_news":

                query = arguments["query"]

                result = search_news(query)

                if isinstance(result, list):

                    print(
                        f"👀 Observation: "
                        f"{len(result)} news results found"
                    )

                else:

                    print(
                        f"👀 Observation: {result}"
                    )

            elif tool_name == "search_competitor":

                 company = arguments["company"]
                 topic = arguments["topic"]

                 result = search_competitor(
                    company,
                    topic
                     )

                 print(
                "👀 Observation: "
                "competitor intelligence retrieved"
            )
            # =================================================
            # UNKNOWN TOOL
            # =================================================

            else:

                result = {
                    "error": f"Unknown tool: {tool_name}"
                }

                print(
                    f"❌ Unknown tool: {tool_name}"
                )


            # =================================================
            # SEND OBSERVATION BACK TO AGENT
            # =================================================

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(
                        result,
                        ensure_ascii=False,
                        default=str
                    )
                }
            )


    # ========================================================
    # MAX STEPS REACHED
    # ========================================================

    return (
        "The agent reached the maximum number of steps "
        "before completing the task."
    )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    print("🤖 AgentX ReAct Agent")

    task = input(
        "\nEnter your task: "
    )

    result = run_react_agent(task)

    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("🤖 FINAL RESULT")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    print(result)