import json

from tools.research import search_research
from tools.crossref import search_crossref
from tools.news import search_news
from tools.competitor import search_competitor


# ============================================================
# RESEARCH SPECIALIST AGENT
# ============================================================

def research_agent(task):

    print("\n🔬 RESEARCH AGENT")
    print("Role: Scientific research, publications and DOI evidence")

    print("🔧 Action: search_research")

    research_results = search_research(task)

    print("👀 Research observation received")

    print("🔧 Action: search_crossref")

    crossref_results = search_crossref(task)

    print("👀 Crossref observation received")

    return {
        "agent": "Research Specialist",
        "responsibility": "Scientific research and DOI evidence",
        "research": research_results,
        "crossref": crossref_results
    }


# ============================================================
# COMPETITOR SPECIALIST AGENT
# ============================================================

def competitor_agent(task):

    print("\n⚔ COMPETITOR AGENT")
    print("Role: Competitor activity, market developments and news")

    print("🔧 Action: search_competitor")
    
    competitor_results = []
    
    for company in ["OpenAI", "Google"]:
    
            print(f"🔧 Action: search_competitor ({company})")
    
            result = search_competitor(
                company=company,
                topic=task
           )
    
            competitor_results.append({
                "company": company,
                "data": result
            })
    
            print(
                f"👀 Observation: {company} intelligence received"
             )
    
    print("🔧 Action: search_news")
    
    news_results = search_news(task)
    
    print("👀 News observation received")





    return {
        "agent": "Competitor Specialist",
        "responsibility": "Competitor and market intelligence",
        "competitor": competitor_results,
        "news": news_results
    }


# ============================================================
# ORCHESTRATOR
# ============================================================

def run_multi_agent(task):

    print("\n" + "=" * 60)
    print("🤖 AGENTX MULTI-AGENT SYSTEM")
    print("=" * 60)

    print("\n🎯 ORCHESTRATOR")
    print("Delegating the goal to specialized agents...")

    # --------------------------------------------------------
    # Agent 1
    # --------------------------------------------------------

    research_report = research_agent(task)

    # --------------------------------------------------------
    # Agent 2
    # --------------------------------------------------------

    competitor_report = competitor_agent(task)

    # --------------------------------------------------------
    # Collaboration
    # --------------------------------------------------------

    print("\n🧠 ORCHESTRATOR")
    print("Combining outputs from both specialized agents...")

    final_report = build_final_report(
        task,
        research_report,
        competitor_report
    )

    print("\n✅ ORCHESTRATOR COMPLETED")

    return final_report


# ============================================================
# FINAL REPORT BUILDER
# ============================================================

def build_final_report(
    task,
    research_report,
    competitor_report
):

    research_data = research_report.get(
        "research",
        []
    )

    crossref_data = research_report.get(
        "crossref",
        []
    )

    competitor_data = competitor_report.get(
        "competitor",
        []
    )

    news_data = competitor_report.get(
        "news",
        []
    )

    report = []

    report.append("# AgentX Multi-Agent Intelligence Report")

    report.append("\n## 🎯 User Goal")
    report.append(task)

    report.append("\n## 🔬 Research Specialist Findings")

    if isinstance(research_data, list):

        for i, item in enumerate(
            research_data[:5],
            1
        ):

            if isinstance(item, dict):

                title = item.get(
                    "title",
                    "Research paper"
                )

                date = item.get(
                    "date",
                    item.get(
                        "publication_date",
                        "Unknown date"
                    )
                )

                doi = item.get(
                    "doi",
                    item.get(
                        "DOI",
                        "Not available"
                    )
                )

                report.append(
                    f"{i}. **{title}** — "
                    f"{date} — DOI: {doi}"
                )

            else:

                report.append(
                    f"{i}. {str(item)}"
                )

    else:

        report.append(
            str(research_data)
        )

    report.append("\n### Crossref Evidence")

    if isinstance(crossref_data, list):

        for i, item in enumerate(
            crossref_data[:5],
            1
        ):

            if isinstance(item, dict):

                title = item.get(
                    "title",
                    "Paper"
                )

                doi = item.get(
                    "DOI",
                    item.get(
                        "doi",
                        "Not available"
                    )
                )

                report.append(
                    f"{i}. **{title}** — DOI: {doi}"
                )

            else:

                report.append(
                    f"{i}. {str(item)}"
                )

    else:

        report.append(
            str(crossref_data)
        )

    report.append(
        "\n## ⚔ Competitor Specialist Findings"
    )

    if isinstance(
        competitor_data,
        dict
    ):

        for key, value in competitor_data.items():

            report.append(
                f"- **{key}:** {value}"
            )

    elif isinstance(
        competitor_data,
        list
    ):

        for i, item in enumerate(
            competitor_data[:5],
            1
        ):

            report.append(
                f"{i}. {item}"
            )

    else:

        report.append(
            str(competitor_data)
        )

    report.append("\n### 📰 News Intelligence")

    if isinstance(news_data, list):

        for i, item in enumerate(
            news_data[:5],
            1
        ):

            if isinstance(item, dict):

                title = item.get(
                    "title",
                    "News item"
                )

                date = item.get(
                    "date",
                    item.get(
                        "published",
                        ""
                    )
                )

                report.append(
                    f"{i}. **{title}** {date}"
                )

            else:

                report.append(
                    f"{i}. {item}"
                )

    elif isinstance(news_data, dict):

        for key, value in news_data.items():

            report.append(
                f"- **{key}:** {value}"
            )

    else:

        report.append(
            str(news_data)
        )

    # --------------------------------------------------------
    # Collaboration summary
    # --------------------------------------------------------

    report.append(
        "\n## 🤝 Multi-Agent Collaboration"
    )

    report.append(
        "The Research Specialist provided scientific "
        "evidence and DOI information."
    )

    report.append(
        "The Competitor Specialist provided competitor "
        "and news intelligence."
    )

    report.append(
        "The Orchestrator combined both perspectives "
        "into one intelligence report."
    )

    # --------------------------------------------------------
    # Actionable intelligence
    # --------------------------------------------------------

    report.append(
        "\n## 💡 Actionable Intelligence"
    )

    report.append(
        "- Monitor emerging research trends identified "
        "by the Research Specialist."
    )

    report.append(
        "- Track competitor and industry developments "
        "identified by the Competitor Specialist."
    )

    report.append(
        "- Use research evidence together with competitor "
        "signals before making product decisions."
    )

    report.append(
        "\n## 🧠 Architecture"
    )

    report.append(
        "User Goal → Orchestrator → Research Specialist "
        "+ Competitor Specialist → Orchestrator → "
        "Final Intelligence"
    )

    return "\n".join(report)


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    print("\n🤖 AgentX Multi-Agent Intelligence")

    task = input(
        "\nEnter your intelligence task: "
    )

    try:

        result = run_multi_agent(task)

        print("\n")
        print("=" * 60)
        print("📊 FINAL MULTI-AGENT INTELLIGENCE REPORT")
        print("=" * 60)

        print(result)

    except Exception as e:

        print("\n❌ Multi-Agent Error")
        print(type(e).__name__)
        print(str(e))