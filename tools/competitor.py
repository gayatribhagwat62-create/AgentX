from tools.research import search_research
from tools.news import search_news


def search_competitor(company, topic):

    # Create a company-focused query
    company_topic = f"{company} recent AI developments"

    print(f"   🔎 Research query: {company_topic}")
    print(f"   🔎 News query: {company_topic}")

    research = search_research(
        company_topic,
        limit=3
    )

    news = search_news(
        company_topic,
        limit=3
    )

    return {
        "company": company,
        "topic": company_topic,
        "research": research,
        "news": news
    }


if __name__ == "__main__":

    company = input("Enter competitor: ")
    topic = input("Enter topic: ")

    result = search_competitor(
        company,
        topic
    )

    print("\n🏢 COMPETITOR INTELLIGENCE\n")

    print("Company:", result["company"])
    print("Topic:", result["topic"])

    print("\n🔬 Research:")

    if isinstance(result["research"], list):

        for item in result["research"]:
            print("-", item.get("title"))

    else:
        print(result["research"])

    print("\n📰 News:")

    if isinstance(result["news"], list):

        for item in result["news"]:
            print("-", item.get("title"))

    else:
        print(result["news"])