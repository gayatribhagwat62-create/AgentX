
import streamlit as st
import json
import os
from react_agent import run_react_agent
# ============================================================
# PERSISTENT MEMORY
# ============================================================

MEMORY_FILE = "agentx_memory.json"


def load_memory():
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    return []


def save_memory(history):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(
            history[-5:],
            f,
            ensure_ascii=False,
            indent=2
        )



# ============================================================
# SESSION STATE
# ============================================================

if "conversation_history" not in st.session_state:
    st.session_state["conversation_history"] = load_memory()

if "result" not in st.session_state:
    st.session_state["result"] = ""

if "task" not in st.session_state:
    st.session_state["task"] = ""

if "selected_section" not in st.session_state:
    st.session_state["selected_section"] = "home"


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AgentX | Intelligence Platform",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
<style>

/* ============================================================
   GLOBAL
============================================================ */

.stApp {
    background:
        radial-gradient(
            circle at top right,
            rgba(99,102,241,0.10),
            transparent 30%
        ),
        linear-gradient(
            135deg,
            #f8faff 0%,
            #f5f7fb 45%,
            #eef2ff 100%
        );

    color: #172033;
}

.block-container {
    max-width: 1450px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}


/* ============================================================
   SIDEBAR
============================================================ */

section[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            #111827 0%,
            #172554 100%
        );

    border-right: 1px solid rgba(255,255,255,0.08);
}

section[data-testid="stSidebar"] * {
    color: #f8fafc !important;
}

section[data-testid="stSidebar"] .stCaption {
    color: #aeb9cc !important;
}

section[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.12);
}


/* ============================================================
   SIDEBAR BUTTONS
============================================================ */

section[data-testid="stSidebar"] .stButton > button {
    background: rgba(255,255,255,0.06) !important;
    color: white !important;
    border: 1px solid rgba(255,255,255,0.10) !important;
    text-align: left !important;
    justify-content: flex-start !important;
}

section[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(99,102,241,0.35) !important;
    border-color: #818cf8 !important;
}


/* ============================================================
   HERO
============================================================ */

.hero {
    position: relative;
    padding: 42px 38px;
    margin-bottom: 30px;
    border-radius: 24px;
    overflow: hidden;

    background:
        linear-gradient(
            135deg,
            #111827 0%,
            #1e1b4b 55%,
            #312e81 100%
        );

    box-shadow:
        0 20px 50px rgba(30,41,59,0.18);
}

.hero:after {
    content: "";
    position: absolute;
    width: 280px;
    height: 280px;
    right: -80px;
    top: -100px;
    border-radius: 50%;
    background: rgba(129,140,248,0.22);
}

.hero-title {
    position: relative;
    z-index: 2;
    font-size: 48px;
    font-weight: 850;
    letter-spacing: -1.5px;
    color: white;
    margin-bottom: 8px;
}

.hero-subtitle {
    position: relative;
    z-index: 2;
    font-size: 18px;
    color: #c7d2fe;
}


/* ============================================================
   FEATURE CARDS
============================================================ */

.card {
    background: rgba(255,255,255,0.94);
    border: 1px solid #e5e7eb;
    border-radius: 18px;
    padding: 22px;
    min-height: 125px;
    margin-bottom: 12px;

    box-shadow:
        0 8px 25px rgba(15,23,42,0.06);

    transition: all 0.2s ease;
}

.card:hover {
    transform: translateY(-3px);

    box-shadow:
        0 14px 35px rgba(15,23,42,0.10);

    border-color: #c7d2fe;
}

.card-title {
    font-size: 18px;
    font-weight: 750;
    margin-bottom: 9px;
    color: #111827;
}

.card-text {
    color: #64748b;
    font-size: 14px;
    line-height: 1.6;
}


/* ============================================================
   CARD BUTTONS
============================================================ */

.card-button .stButton > button {
    border-radius: 10px !important;
    background: white !important;
    color: #4338ca !important;
    border: 1px solid #c7d2fe !important;
    font-weight: 700 !important;
}

.card-button .stButton > button:hover {
    background: #eef2ff !important;
}


/* ============================================================
   HEADINGS
============================================================ */

h2 {
    font-weight: 800 !important;
    letter-spacing: -0.5px;
    color: #111827;
}

h3 {
    font-weight: 750 !important;
    color: #1e293b;
}


/* ============================================================
   TEXT AREA
============================================================ */

.stTextArea textarea {
    border-radius: 16px !important;
    border: 1px solid #dbe1ea !important;
    background: white !important;
    padding: 18px !important;
    font-size: 16px !important;
    line-height: 1.6 !important;

    box-shadow:
        0 5px 20px rgba(15,23,42,0.04);
}

.stTextArea textarea:focus {
    border-color: #6366f1 !important;

    box-shadow:
        0 0 0 3px rgba(99,102,241,0.12) !important;
}


/* ============================================================
   BUTTONS
============================================================ */

.stButton > button {
    border-radius: 12px !important;
    font-weight: 700 !important;
    border: 1px solid #dbe1ea !important;
    min-height: 44px;

    transition: all 0.2s ease !important;
}

.stButton > button:hover {
    transform: translateY(-2px);
    border-color: #818cf8 !important;

    box-shadow:
        0 7px 20px rgba(99,102,241,0.15);
}

button[kind="primary"] {
    background:
        linear-gradient(
            135deg,
            #4f46e5,
            #7c3aed
        ) !important;

    border: none !important;
    color: white !important;
    font-size: 16px !important;
    min-height: 52px !important;

    box-shadow:
        0 10px 25px rgba(79,70,229,0.25);
}

button[kind="primary"]:hover {
    background:
        linear-gradient(
            135deg,
            #4338ca,
            #6d28d9
        ) !important;

    box-shadow:
        0 14px 32px rgba(79,70,229,0.32);
}


/* ============================================================
   STATUS
============================================================ */

.status {
    background:
        linear-gradient(
            135deg,
            #ecfdf5,
            #f0fdf4
        );

    border: 1px solid #a7f3d0;
    color: #047857;

    padding: 14px 18px;
    border-radius: 14px;

    font-weight: 650;
    margin: 15px 0;
}


/* ============================================================
   REPORT
============================================================ */

.report {
    background: rgba(255,255,255,0.96);
    border: 1px solid #e2e8f0;
    border-radius: 20px;

    padding: 30px;
    margin-top: 12px;

    box-shadow:
        0 12px 35px rgba(15,23,42,0.07);

    line-height: 1.75;
}

.report h1,
.report h2,
.report h3 {
    color: #111827;
}

.report strong {
    color: #312e81;
}


/* ============================================================
   MEMORY
============================================================ */

.memory-card {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 16px;

    padding: 18px;
    margin-bottom: 12px;

    box-shadow:
        0 5px 18px rgba(15,23,42,0.04);
}


/* ============================================================
   EXPANDERS
============================================================ */

div[data-testid="stExpander"] {
    background: rgba(255,255,255,0.9);
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    margin-bottom: 10px;
}

div[data-testid="stExpander"]:hover {
    border-color: #a5b4fc;
}


/* ============================================================
   TOOL BADGES
============================================================ */

.tool {
    display: inline-flex;
    align-items: center;

    background: white;
    border: 1px solid #e0e7ff;
    color: #3730a3;

    border-radius: 999px;

    padding: 9px 15px;
    margin: 5px 5px 5px 0;

    font-size: 13px;
    font-weight: 650;

    box-shadow:
        0 4px 12px rgba(79,70,229,0.06);
}


/* ============================================================
   FEATURE INFO PANEL
============================================================ */

.feature-panel {
    background:
        linear-gradient(
            135deg,
            #ffffff,
            #eef2ff
        );

    border: 1px solid #c7d2fe;
    border-radius: 18px;

    padding: 24px;
    margin: 15px 0 25px;

    box-shadow:
        0 8px 25px rgba(79,70,229,0.08);
}

.feature-panel-title {
    font-size: 22px;
    font-weight: 800;
    color: #312e81;
    margin-bottom: 8px;
}

.feature-panel-text {
    color: #475569;
    line-height: 1.7;
}


/* ============================================================
   TOOL DETAIL BOX
============================================================ */

.tool-detail {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 16px 18px;
    margin-top: 10px;
}

.tool-detail-title {
    font-size: 16px;
    font-weight: 800;
    color: #312e81;
    margin-bottom: 5px;
}

.tool-detail-text {
    color: #64748b;
    font-size: 14px;
    line-height: 1.6;
}


/* ============================================================
   FOOTER
============================================================ */

.footer {
    text-align: center;
    color: #94a3b8;
    font-size: 13px;
    padding: 35px 15px 10px;
}

.footer b {
    color: #4f46e5;
}


/* ============================================================
   MOBILE
============================================================ */

@media (max-width: 900px) {

    .hero {
        padding: 30px 24px;
    }

    .hero-title {
        font-size: 36px;
    }

    .hero-subtitle {
        font-size: 16px;
    }

    .card {
        min-height: auto;
    }

    .report {
        padding: 20px;
    }
}

</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 🤖 AgentX")
    st.caption("Autonomous Intelligence Platform")

    st.divider()

    st.markdown("### Agent Capabilities")

    if st.button(
        "🔬 Research Tracking",
        use_container_width=True,
        key="side_research"
    ):
        st.session_state["selected_section"] = "research"
        st.rerun()

    st.caption("Scientific publications and research trends")

    if st.button(
        "📰 News Monitoring",
        use_container_width=True,
        key="side_news"
    ):
        st.session_state["selected_section"] = "news"
        st.rerun()

    st.caption("Recent industry developments")

    if st.button(
        "🏢 Competitor Intelligence",
        use_container_width=True,
        key="side_competitor"
    ):
        st.session_state["selected_section"] = "competitors"
        st.rerun()

    st.caption("Competitor activities and positioning")

    if st.button(
        "🧠 Agentic Reasoning",
        use_container_width=True,
        key="side_agent"
    ):
        st.session_state["selected_section"] = "agent"
        st.rerun()

    st.caption("Plan → Act → Observe → Decide")

    if st.button(
        "🔧 External Tools",
        use_container_width=True,
        key="side_tools"
    ):
        st.session_state["selected_section"] = "tools"
        st.rerun()

    st.caption("Crossref • OpenAlex • Research APIs")

    if st.button(
        "🧠 Short-Term Memory",
        use_container_width=True,
        key="side_memory"
    ):
        st.session_state["selected_section"] = "memory"
        st.rerun()

    st.caption("Maintains recent conversation context")

    st.divider()

    st.markdown("### Agent Workflow")

    st.markdown(
        """
**1. Understand Goal**

↓

**2. Select Tools**

↓

**3. Gather Information**

↓

**4. Analyze Results**

↓

**5. Remember Context**

↓

**6. Generate Insights**
"""
    )

    st.divider()

    st.caption("AgentX Hackathon Prototype")


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
<div class="hero">

<div class="hero-title">
🤖 AgentX
</div>

<div class="hero-subtitle">
Autonomous Research & Competitor Intelligence
</div>

</div>
""",
    unsafe_allow_html=True
)


# ============================================================
# FEATURE CARDS
# ============================================================

st.markdown("## ⚡ Intelligence Modules")

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.markdown(
        """
<div class="card">
    <div class="card-title">🔬 Research</div>
    <div class="card-text">
    Track scientific publications, research trends
    and DOI information.
    </div>
</div>
""",
        unsafe_allow_html=True
    )

    if st.button(
        "Explore Research →",
        key="card_research",
        use_container_width=True
    ):
        st.session_state["selected_section"] = "research"
        st.rerun()


with col2:

    st.markdown(
        """
<div class="card">
    <div class="card-title">📰 News</div>
    <div class="card-text">
    Monitor recent AI industry developments,
    news and emerging trends.
    </div>
</div>
""",
        unsafe_allow_html=True
    )

    if st.button(
        "Explore News →",
        key="card_news",
        use_container_width=True
    ):
        st.session_state["selected_section"] = "news"
        st.rerun()


with col3:

    st.markdown(
        """
<div class="card">
    <div class="card-title">⚔ Competitors</div>
    <div class="card-text">
    Compare companies, identify competitive trends,
    risks and opportunities.
    </div>
</div>
""",
        unsafe_allow_html=True
    )

    if st.button(
        "Explore Competitors →",
        key="card_competitors",
        use_container_width=True
    ):
        st.session_state["selected_section"] = "competitors"
        st.rerun()


with col4:

    st.markdown(
        """
<div class="card">
    <div class="card-title">🧠 Agentic AI</div>
    <div class="card-text">
    Dynamically selects tools, reasons over results
    and maintains task context.
    </div>
</div>
""",
        unsafe_allow_html=True
    )

    if st.button(
        "View Agent →",
        key="card_agent",
        use_container_width=True
    ):
        st.session_state["selected_section"] = "agent"
        st.rerun()


# ============================================================
# SELECTED FEATURE PANEL
# ============================================================

selected = st.session_state["selected_section"]


# ------------------------------------------------------------
# RESEARCH
# ------------------------------------------------------------

if selected == "research":

    st.markdown(
        """
<div class="feature-panel">

<div class="feature-panel-title">
🔬 Research Intelligence
</div>

<div class="feature-panel-text">

AgentX searches scientific research and external
research sources to identify recent publications,
important findings and DOI information.

<br><br>

<b>Tools:</b> Research API + Crossref + OpenAlex

</div>

</div>
""",
        unsafe_allow_html=True
    )


# ------------------------------------------------------------
# NEWS
# ------------------------------------------------------------

elif selected == "news":

    st.markdown(
        """
<div class="feature-panel">

<div class="feature-panel-title">
📰 News Intelligence
</div>

<div class="feature-panel-text">

AgentX monitors recent AI industry developments
and gathers relevant news to identify emerging
trends and important events.

<br><br>

<b>Tool:</b> News Search API

</div>

</div>
""",
        unsafe_allow_html=True
    )


# ------------------------------------------------------------
# COMPETITORS
# ------------------------------------------------------------

elif selected == "competitors":

    st.markdown(
        """
<div class="feature-panel">

<div class="feature-panel-title">
⚔ Competitor Intelligence
</div>

<div class="feature-panel-text">

AgentX can investigate companies such as
<b>OpenAI</b> and <b>Google</b>, collect research
and news signals, and identify competitive trends,
risks and opportunities.

<br><br>

<b>Architecture:</b>

<br>

Competitor Specialist
→ Research Specialist
→ Orchestrator

</div>

</div>
""",
        unsafe_allow_html=True
    )


# ------------------------------------------------------------
# AGENTIC REASONING
# ------------------------------------------------------------

elif selected == "agent":

    st.markdown(
        """
<div class="feature-panel">

<div class="feature-panel-title">
🧠 Agentic Reasoning
</div>

<div class="feature-panel-text">

<b>AgentX follows a dynamic agentic reasoning architecture.</b>

<br><br>

<div style="
display:flex;
align-items:center;
justify-content:center;
flex-wrap:wrap;
gap:8px;
font-size:15px;
font-weight:700;
color:#312e81;
">

<span>Understand</span>
<span>→</span>
<span>Plan</span>
<span>→</span>
<span>Select Tool</span>
<span>→</span>
<span>Act</span>
<span>→</span>
<span>Observe</span>
<span>→</span>
<span>Reason</span>
<span>→</span>
<span>Evaluate</span>
<span>→</span>
<span>Replan</span>

</div>

<br>

AgentX does not follow a fixed sequence. The agent dynamically
selects tools, evaluates evidence, detects failures and can
replan when additional investigation is required.

</div>

</div>
""",
        unsafe_allow_html=True
    )

    st.markdown("### 🧠 Agent Capabilities")

    agent_col1, agent_col2 = st.columns(2)

    with agent_col1:

        st.markdown(
            """
<div class="tool-detail">

<div class="tool-detail-title">
🧠 Dynamic Planning
</div>

<div class="tool-detail-text">
Creates an investigation plan dynamically based on
the user's objective instead of following a fixed workflow.
</div>

</div>
""",
            unsafe_allow_html=True
        )

        st.markdown(
            """
<div class="tool-detail">

<div class="tool-detail-title">
🔀 Conditional Routing
</div>

<div class="tool-detail-text">
Routes the task to Research, News, Competitor or
Verification agents depending on the current state.
</div>

</div>
""",
            unsafe_allow_html=True
        )

        st.markdown(
            """
<div class="tool-detail">

<div class="tool-detail-title">
⚡ Parallel Execution
</div>

<div class="tool-detail-text">
Multiple specialist agents can execute independently
and gather evidence in parallel.
</div>

</div>
""",
            unsafe_allow_html=True
        )

        st.markdown(
            """
<div class="tool-detail">

<div class="tool-detail-title">
💾 Shared State & Checkpointing
</div>

<div class="tool-detail-text">
Agents share task state and checkpoint progress so
execution can recover from failures.
</div>

</div>
""",
            unsafe_allow_html=True
        )

    with agent_col2:

        st.markdown(
            """
<div class="tool-detail">

<div class="tool-detail-title">
♻️ Autonomous Replanning
</div>

<div class="tool-detail-text">
The planner can modify the investigation strategy
when evidence is incomplete or a tool fails.
</div>

</div>
""",
            unsafe_allow_html=True
        )

        st.markdown(
            """
<div class="tool-detail">

<div class="tool-detail-title">
🛡️ Failure Recovery & Fallback
</div>

<div class="tool-detail-text">
If an external tool fails, AgentX can use an alternative
tool or route the task to another specialist.
</div>

</div>
""",
            unsafe_allow_html=True
        )

        st.markdown(
            """
<div class="tool-detail">

<div class="tool-detail-title">
⚔️ Conflict Resolution
</div>

<div class="tool-detail-text">
Detects conflicting evidence and sends uncertain claims
for additional verification before finalizing the result.
</div>

</div>
""",
            unsafe_allow_html=True
        )

        st.markdown(
            """
<div class="tool-detail">

<div class="tool-detail-title">
🔎 Verification & Self-Evaluation
</div>

<div class="tool-detail-text">
Evaluates evidence quality, confidence and unresolved
uncertainty before producing the final report.
</div>

</div>
""",
            unsafe_allow_html=True
        )

    st.markdown("### 🔄 Runtime Agent Loop")

    st.markdown(
        """
<div class="feature-panel">

<div class="feature-panel-text">

<b>
Goal
→ Dynamic Plan
→ Route
→ Parallel Agents
→ Observe
→ Analyze
→ Verify
→ Self-Evaluate
→ Replan
→ Finalize
</b>

<br><br>

This loop enables AgentX to recover from tool failures,
resolve conflicting evidence and adapt its execution
strategy autonomously.

</div>

</div>
""",
        unsafe_allow_html=True
    )


# ------------------------------------------------------------
# EXTERNAL TOOLS
# ------------------------------------------------------------

elif selected == "tools":

    st.markdown(
        """
<div class="feature-panel">

<div class="feature-panel-title">
🔧 External Tool Stack
</div>

<div class="feature-panel-text">

AgentX uses multiple external information sources
and specialist tools instead of relying only on the
language model.

<br><br>

<b>Tool Selection:</b>

<br><br>

Research → Scientific Evidence

<br>
Crossref → DOI Verification

<br>
OpenAlex → Research Metadata

<br>
News → Current Industry Signals

<br>
Competitor Intelligence → Company Analysis

<br>
Verification → Evidence Validation

</div>

</div>
""",
        unsafe_allow_html=True
    )

    st.markdown("### 🔧 Tool Details")

    tool_col1, tool_col2 = st.columns(2)

    with tool_col1:

        st.markdown(
            """
<div class="tool-detail">

<div class="tool-detail-title">
🔬 Research API
</div>

<div class="tool-detail-text">
Searches scientific publications and research
relevant to the intelligence objective.
</div>

</div>
""",
            unsafe_allow_html=True
        )

        st.markdown(
            """
<div class="tool-detail">

<div class="tool-detail-title">
📚 Crossref
</div>

<div class="tool-detail-text">
Verifies DOI information and retrieves publication
metadata for research evidence.
</div>

</div>
""",
            unsafe_allow_html=True
        )

        st.markdown(
            """
<div class="tool-detail">

<div class="tool-detail-title">
🌐 OpenAlex
</div>

<div class="tool-detail-text">
Provides scholarly metadata and research information
from a large academic database.
</div>

</div>
""",
            unsafe_allow_html=True
        )

    with tool_col2:

        st.markdown(
            """
<div class="tool-detail">

<div class="tool-detail-title">
📰 News Search
</div>

<div class="tool-detail-text">
Finds recent industry developments and news signals
relevant to the investigation.
</div>

</div>
""",
            unsafe_allow_html=True
        )

        st.markdown(
            """
<div class="tool-detail">

<div class="tool-detail-title">
🏢 Competitor Intelligence
</div>

<div class="tool-detail-text">
Analyzes competitor activity, positioning, risks
and opportunities.
</div>

</div>
""",
            unsafe_allow_html=True
        )

        st.markdown(
            """
<div class="tool-detail">

<div class="tool-detail-title">
🔎 Verification Agent
</div>

<div class="tool-detail-text">
Checks conflicting or uncertain evidence and improves
confidence before finalization.
</div>

</div>
""",
            unsafe_allow_html=True
        )

    st.markdown("### 🔗 Agent ↔ Tool Architecture")

    st.markdown(
        """
<div class="feature-panel">

<div class="feature-panel-text">

<div style="
text-align:center;
font-size:16px;
font-weight:750;
color:#312e81;
line-height:2;
">

🧠 <b>Agent Planner</b>
<br>
↓
<br>
🔀 <b>Conditional Router</b>
<br>
↓
<br>
🔬 Research &nbsp;&nbsp; 📰 News &nbsp;&nbsp; 🏢 Competitor
<br>
↓
<br>
📊 <b>Shared Evidence State</b>
<br>
↓
<br>
🔎 <b>Verification</b>
<br>
↓
<br>
🧪 <b>Self-Evaluation</b>
<br>
↓
<br>
♻️ <b>Autonomous Replanning</b>

</div>

</div>

</div>
""",
        unsafe_allow_html=True
    )
# ------------------------------------------------------------
# MEMORY
# ------------------------------------------------------------

elif selected == "memory":

    memory_count = len(
        st.session_state["conversation_history"]
    )

    st.markdown(
        f"""
<div class="feature-panel">

<div class="feature-panel-title">
🧠 Short-Term Memory
</div>

<div class="feature-panel-text">

AgentX stores recent user requests and agent
responses in Streamlit session state.

<br><br>

<b>Current stored interactions:</b>
{memory_count}

<br><br>

The latest five interactions are supplied as
context for follow-up tasks.

</div>

</div>
""",
        unsafe_allow_html=True
    )


# ============================================================
# INTELLIGENCE REQUEST
# ============================================================

st.markdown("## 🎯 Intelligence Request")

st.write(
    "Tell AgentX what you want to investigate. "
    "The agent will decide which tools are required and "
    "use previous conversation context when available."
)


# ============================================================
# TASK INPUT
# ============================================================

task_input = st.text_area(
    "Research objective",
    value=st.session_state["task"],
    placeholder=(
        "Example:\n"
        "Compare OpenAI and Google in recent AI developments. "
        "Find research and news, identify competitive trends, "
        "risks, opportunities and recommend what an AI startup "
        "should do."
    ),
    height=150,
    label_visibility="collapsed"
)

st.session_state["task"] = task_input


# ============================================================
# QUICK EXAMPLES
# ============================================================

st.markdown("### 💡 Try an example")

example1, example2, example3 = st.columns(3)


with example1:

    if st.button(
        "🔬 Generative AI Research",
        use_container_width=True
    ):

        st.session_state["task"] = (
            "Find recent research about generative AI "
            "and provide DOI information."
        )

        st.rerun()


with example2:

    if st.button(
        "⚔ OpenAI vs Google",
        use_container_width=True
    ):

        st.session_state["task"] = (
            "Compare OpenAI and Google in recent AI "
            "developments. Identify competitive trends, "
            "risks, opportunities and recommendations."
        )

        st.rerun()


with example3:

    if st.button(
        "📰 AI Industry Trends",
        use_container_width=True
    ):

        st.session_state["task"] = (
            "Find recent AI industry news and identify "
            "important trends for an AI startup."
        )

        st.rerun()


# ============================================================
# CURRENT TASK
# ============================================================

task = st.session_state["task"]

if task:

    st.info(
        f"🎯 Selected task: {task}"
    )


# ============================================================
# MEMORY STATUS
# ============================================================

memory_count = len(
    st.session_state["conversation_history"]
)

if memory_count > 0:

    st.success(
        f"🧠 Memory active — {memory_count} previous "
        f"interaction(s) available as context."
    )


# ============================================================
# ANALYZE BUTTON
# ============================================================

st.markdown("")

analyze = st.button(
    "🚀 Analyze Intelligence",
    type="primary",
    use_container_width=True
)


# ============================================================
# RUN AGENT WITH CONTEXT
# ============================================================

if analyze:

    if not task.strip():

        st.warning(
            "Please enter an intelligence request first."
        )

    else:

        st.markdown(
            """
<div class="status">
🟢 Agent is working — selecting tools,
using context and analyzing information...
</div>
""",
            unsafe_allow_html=True
        )

        # ----------------------------------------------------
        # READ SHORT-TERM MEMORY
        # ----------------------------------------------------

        history = st.session_state[
            "conversation_history"
        ]

        recent_history = history[-5:]

        context = ""

        if recent_history:

            context = (
                "\n\n"
                "IMPORTANT: The following is previous "
                "conversation context. Use it to understand "
                "follow-up questions and avoid asking the "
                "user to repeat information.\n\n"
            )

            for item in recent_history:

                context += (
                    f"User: {item['user']}\n"
                )

                context += (
                    f"Agent: {item['agent']}\n\n"
                )

        # ----------------------------------------------------
        # CONTEXT AWARE TASK
        # ----------------------------------------------------

        context_aware_task = (
            task +
            context
        )

        # ----------------------------------------------------
        # RUN AGENT
        # ----------------------------------------------------

        with st.spinner(
            "AgentX is researching, observing, "
            "remembering and analyzing..."
        ):

            try:

                result = run_react_agent(
                    context_aware_task
                )

                if result:

                    st.session_state["result"] = result

                    st.session_state[
                        "conversation_history"
                    ].append(
                        {
                            "user": task,
                            "agent": result
                        }
                    )
                    save_memory(st.session_state["conversation_history"])
                    st.success(
                        "✅ Intelligence analysis completed "
                        "and conversation saved to memory."
                    )

                else:

                    st.warning(
                        "Agent returned an empty response."
                    )

            except Exception as e:

                st.error(
                    f"❌ Agent error: {type(e).__name__}"
                )

                st.code(
                    str(e)
                )


# ============================================================
# RESULT
# ============================================================

if st.session_state["result"]:

    st.divider()

    st.markdown("## 📊 Intelligence Report")

    st.markdown(
        """
<div class="report">
""",
        unsafe_allow_html=True
    )

    st.markdown(
        st.session_state["result"]
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


# ============================================================
# CONVERSATION MEMORY
# ============================================================

if st.session_state["conversation_history"]:

    st.divider()

    st.markdown("## 🧠 Conversation Memory")

    st.caption(
        "AgentX maintains recent conversation context "
        "for follow-up intelligence requests."
    )

    for i, item in enumerate(
        st.session_state["conversation_history"][-5:],
        1
    ):

        with st.expander(
            f"Memory {i} — Previous Interaction"
        ):

            st.markdown("**👤 User Request**")

            st.write(
                item["user"]
            )

            st.markdown("**🤖 Agent Response**")

            st.write(
                item["agent"]
            )

    if st.button(
        "🗑️ Clear Conversation Memory"
    ):

        st.session_state[
            "conversation_history"
        ] = []

        st.session_state[
            "result"
        ] = ""

        st.session_state[
            "task"
        ] = ""

        st.session_state[
            "selected_section"
        ] = "home"
        save_memory([])
        st.rerun()


# ============================================================
# TOOL STACK
# ============================================================

st.divider()

st.markdown("### 🔧 Intelligence Tool Stack")

st.markdown(
    """
<span class="tool">🧠 ReAct Agent</span>
<span class="tool">🔬 Research API</span>
<span class="tool">📚 Crossref</span>
<span class="tool">🌐 OpenAlex</span>
<span class="tool">📰 News</span>
<span class="tool">🏢 Competitor Intelligence</span>
<span class="tool">🧠 Short-Term Memory</span>
""",
    unsafe_allow_html=True
)


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
<div class="footer">

<b>AgentX</b> · Autonomous Research & Competitor Intelligence

<br>

Hackathon Prototype ·
Goal → Context → Tools → Collaboration → Insights

</div>
""",
    unsafe_allow_html=True
)