def create_plan(task):
    """
    Creates a high-level plan for the user's goal.
    """

    task_lower = task.lower()

    plan = []

    # Always understand the goal first
    plan.append("Understand the user's goal")

    # Research-related task
    if any(word in task_lower for word in [
        "research",
        "paper",
        "publication",
        "scientific"
    ]):
        plan.append("Search relevant research information")

    # Competitor-related task
    if any(word in task_lower for word in [
        "competitor",
        "competitors",
        "company",
        "startup"
    ]):
        plan.append("Track competitor activities")

    # News-related task
    if any(word in task_lower for word in [
        "news",
        "latest",
        "recent",
        "update",
        "development"
    ]):
        plan.append("Search recent industry developments")

    # Always analyze findings
    plan.append("Analyze and compare collected information")

    # Identify intelligence
    plan.append("Identify important trends, risks and opportunities")

    # Final output
    plan.append("Generate actionable recommendations")

    return plan


if __name__ == "__main__":

    task = input("Enter your task: ")

    plan = create_plan(task)

    print("\n🧠 AGENT PLAN:")

    for i, step in enumerate(plan, 1):
        print(f"{i}. {step}")