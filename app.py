import streamlit as st
from react_agent import run_react_agent


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

st.markdown("""
<style>

    /* Main background */
    .stApp {
        background-color: #f7f8fc;
    }

    /* Header */
    .hero {
        padding: 28px 10px 20px 10px;
    }

    .hero-title {
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .hero-subtitle {
        font-size: 18px;
        color: #667085;
    }

    /* Cards */
    .card {
        background: white;
        border: 1px solid #e6e8ef;
        border-radius: 14px;
        padding: 20px;
        margin-bottom: 15px;
    }

    .card-title {
        font-size: 17px;
        font-weight: 700;
        margin-bottom: 6px;
    }

    .card-text {
        color: #667085;
        font-size: 14px;
    }

    /* Status */
    .status {
        background: #ecfdf3;
        border: 1px solid #abefc6;
        color: #067647;
        padding: 10px 14px;
        border-radius: 10px;
        font-weight: 600;
        margin-bottom: 15px;
    }

    /* Tool badges */
    .tool {
        display: inline-block;
        background: #f2f4f7;
        border: 1px solid #e4e7ec;
        border-radius: 20px;
        padding: 7px 12px;
        margin: 4px;
        font-size: 13px;
    }

    /* Report */
    .report {
        background: white;
        border: 1px solid #e6e8ef;
        border-radius: 14px;
        padding: 25px;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #98a2b3;
        font-size: 13px;
        padding: 25px;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 🤖 AgentX")

    st.caption("Autonomous Intelligence Platform")

    st.divider()

    st.markdown("### Agent Capabilities")

    st.markdown("🔬 **Research Tracking**")
    st.caption("Scientific publications and research trends")

    st.markdown("📰 **News Monitoring**")
    st.caption("Recent industry developments")

    st.markdown("🏢 **Competitor Intelligence**")
    st.caption("Competitor activities and positioning")

    st.markdown("🧠 **Agentic Reasoning**")
    st.caption("Plan → Act → Observe → Decide")

    st.markdown("🔧 **External Tools**")
    st.caption("Crossref • OpenAlex • Research APIs")

    st.divider()

    st.markdown("### Agent Workflow")

    st.markdown("""
    **1. Understand Goal**

    ↓

    **2. Select Tools**

    ↓

    **3. Gather Information**

    ↓

    **4. Analyze Results**

    ↓

    **5. Generate Insights**
    """)

    st.divider()

    st.caption("AgentX Hackathon Prototype")


# ============================================================
# HERO SECTION
# ============================================================

st.markdown("""
<div class="hero">

<div class="hero-title">
🤖 AgentX
</div>

<div class="hero-subtitle">
Autonomous Research & Competitor Intelligence
</div>

</div>
""", unsafe_allow_html=True)


# ============================================================
# TOP CARDS
# ============================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="card">
        <div class="card-title">🔬 Research</div>
        <div class="card-text">
        Track scientific publications and emerging research.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
        <div class="card-title">📰 News</div>
        <div class="card-text">
        Monitor recent developments and industry activity.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="card">
        <div class="card-title">⚔ Competitors</div>
        <div class="card-text">
        Identify competitive trends, risks and opportunities.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="card">
        <div class="card-title">🧠 Agentic AI</div>
        <div class="card-text">
        Dynamically selects tools and analyzes results.
        </div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# INTELLIGENCE REQUEST
# ============================================================

st.markdown("## 🎯 Intelligence Request")

st.markdown(
    "Tell AgentX what you want to investigate. "
    "The agent will decide which tools are required."
)

task = st.text_area(
    "Research objective",
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
        task = (
            "Find recent research about generative AI "
            "and provide DOI information."
        )
        st.session_state["task"] = task
        st.rerun()

with example2:
    if st.button(
        "⚔ OpenAI vs Google",
        use_container_width=True
    ):
        task = (
            "Compare OpenAI and Google in recent AI "
            "developments. Identify competitive trends, "
            "risks, opportunities and recommendations."
        )
        st.session_state["task"] = task
        st.rerun()

with example3:
    if st.button(
        "📰 AI Industry Trends",
        use_container_width=True
    ):
        task = (
            "Find recent AI industry news and identify "
            "important trends for an AI startup."
        )
        st.session_state["task"] = task
        st.rerun()


# ============================================================
# USE SELECTED EXAMPLE
# ============================================================

if "task" in st.session_state:

    task = st.session_state["task"]

    st.info(
        f"Selected task: {task}"
    )


# ============================================================
# ANALYZE BUTTON
# ============================================================

st.markdown("")

analyze = st.button(
    "🚀  Analyze Intelligence",
    type="primary",
    use_container_width=True
)


# ============================================================
# RUN AGENT
# ============================================================

if analyze:

    if not task.strip():

        st.warning(
            "Please enter an intelligence request first."
        )

    else:

        st.markdown(
            '<div class="status">'
            '🟢 Agent is working — selecting tools and '
            'analyzing information...'
            '</div>',
            unsafe_allow_html=True
        )

        with st.spinner(
            "AgentX is researching, observing and analyzing..."
        ):

            try:

                result = run_react_agent(task)

                if result:

                    st.session_state["result"] = result

                    st.success(
                        "✅ Intelligence analysis completed."
                    )

                else:

                    st.warning(
                        "Agent returned an empty response."
                    )

            except Exception as e:

                st.error(
                    f"❌ Agent error: {type(e).__name__}"
                )

                st.code(str(e))


# ============================================================
# RESULT
# ============================================================

if "result" in st.session_state:

    st.divider()

    st.markdown("## 📊 Intelligence Report")

    st.markdown("""
    <div class="report">
    """, unsafe_allow_html=True)

    st.markdown(
        st.session_state["result"]
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


# ============================================================
# TOOL STACK
# ============================================================

st.divider()

st.markdown("### 🔧 Intelligence Tool Stack")

st.markdown("""
<span class="tool">🧠 ReAct Agent</span>
<span class="tool">🔬 Research API</span>
<span class="tool">📚 Crossref</span>
<span class="tool">🌐 OpenAlex</span>
<span class="tool">📰 News</span>
<span class="tool">🏢 Competitor Intelligence</span>
""", unsafe_allow_html=True)


# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">
    <b>AgentX</b> · Autonomous Research & Competitor Intelligence
    <br>
    Hackathon Prototype · Goal → Tools → Observations → Insights
</div>
""", unsafe_allow_html=True)