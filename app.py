import streamlit as st

from react_agent import run_react_agent


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AgentX Intelligence",
    page_icon="🤖",
    layout="wide"
)


# ============================================================
# HEADER
# ============================================================

st.title("🤖 AgentX")
st.subheader("Research & Competitor Intelligence Agent")

st.write(
    "An autonomous AI agent that researches developments, "
    "news and competitor activity and produces actionable insights."
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("⚙️ Agent Capabilities")

    st.success("🔬 Research Tracking")
    st.success("📰 News Monitoring")
    st.success("🏢 Competitor Tracking")
    st.success("🧠 ReAct Reasoning")
    st.success("📊 Intelligence Analysis")

    st.divider()

    st.caption("AgentX Hackathon Prototype")


# ============================================================
# TASK INPUT
# ============================================================

st.markdown("### 🔎 Intelligence Request")

task = st.text_area(
    "Enter your research or competitor tracking task:",
    placeholder=(
        "Example: Compare OpenAI and Google in recent AI "
        "developments. Identify trends, risks, opportunities "
        "and recommend what an AI startup should do."
    ),
    height=140
)


# ============================================================
# ANALYZE BUTTON
# ============================================================

if st.button(
    "🚀 Analyze",
    type="primary",
    use_container_width=True
):

    if not task.strip():

        st.warning(
            "Please enter an intelligence task first."
        )

    else:

      with st.spinner("🤖 Agent is researching and analyzing..."):

           try:

              result = run_react_agent(task)

              if result:
                  st.session_state["result"] = result
                  st.success("✅ Analysis completed!")
              else:
                  st.warning("⚠️ Agent returned an empty response.")

           except Exception as e:

              st.error(f"❌ Agent error: {type(e).__name__}")
              st.code(str(e))


# ============================================================
# RESULT
# ============================================================

if "result" in st.session_state:

    st.divider()

    st.markdown("## 📊 Intelligence Report")

    result = st.session_state["result"]

    st.markdown(result)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "AgentX • Autonomous Research & Competitor Intelligence"
)