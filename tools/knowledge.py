KNOWLEDGE = {
    "python": """
Python is a high-level programming language.
It is widely used for web development, automation,
data science, artificial intelligence and machine learning.
""",

    "dsa": """
Data Structures and Algorithms help organize data
and solve computational problems efficiently.
Common data structures include arrays, linked lists,
stacks, queues, trees and graphs.
""",

    "agentic ai": """
Agentic AI refers to AI systems that can understand
a goal, make decisions, use tools, take actions,
observe results and continue working toward the goal.
""",

    "machine learning": """
Machine Learning is a branch of AI where systems learn
patterns from data and use those patterns to make
predictions or decisions.
"""
}


def search_knowledge(query):

    query = query.lower()

    for topic, information in KNOWLEDGE.items():

        if topic in query:
            return information

    return "I don't have information about that topic."
if __name__ == "__main__":
    print(search_knowledge("What is Agentic AI?"))