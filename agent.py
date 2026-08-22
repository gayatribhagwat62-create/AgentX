import os
import json

from dotenv import load_dotenv
from openai import OpenAI

from tools.calculator import calculate
from tools.knowledge import search_knowledge

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)


# -----------------------------
# TOOLS AVAILABLE TO THE AGENT
# -----------------------------

tools = [

    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Use this tool for mathematical calculations.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Mathematical expression."
                    }
                },
                "required": ["expression"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "search_knowledge",
            "description": "Use this tool to find information about Python, DSA, Agentic AI and Machine Learning.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Topic or question to search."
                    }
                },
                "required": ["query"]
            }
        }
    }
]


# -----------------------------
# AGENT
# -----------------------------

def run_agent(task):

    messages = [

        {
            "role": "system",
            "content": """
You are an intelligent AI agent.

Understand the user's goal and decide whether you need a tool.

Available tools:

1. Calculator
   Use for mathematical calculations.

2. Knowledge Search
   Use for questions about Python, DSA, Agentic AI
   and Machine Learning.

If a tool is useful, call it.
After receiving the tool result, provide a clear final answer.
"""
        },

        {
            "role": "user",
            "content": task
        }

    ]


    # First AI decision
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )

    message = response.choices[0].message


    # -----------------------------
    # TOOL CALL
    # -----------------------------

    if message.tool_calls:

        messages.append(message)

        for tool_call in message.tool_calls:

            tool_name = tool_call.function.name

            arguments = json.loads(
                tool_call.function.arguments
            )


            # Calculator
            if tool_name == "calculate":

                expression = arguments["expression"]

                print("\n🔧 Tool selected: Calculator")
                print(f"🧮 Expression: {expression}")

                result = calculate(expression)


            # Knowledge
            elif tool_name == "search_knowledge":

                query = arguments["query"]

                print("\n🔧 Tool selected: Knowledge Search")
                print(f"🔎 Query: {query}")

                result = search_knowledge(query)


            else:

                result = "Unknown tool"


            print(f"📊 Tool result: {result}")


            # Send result back to AI
            messages.append({

                "role": "tool",

                "tool_call_id": tool_call.id,

                "content": str(result)

            })


        # -----------------------------
        # FINAL AI RESPONSE
        # -----------------------------

        final_response = client.chat.completions.create(

            model="openrouter/free",

            messages=messages,

            tools=tools

        )

        return final_response.choices[0].message.content


    # No tool needed
    return message.content


# -----------------------------
# MAIN
# -----------------------------

if __name__ == "__main__":

    print("🤖 AgentX Multi-Tool Agent")

    task = input("\nEnter your task: ")

    result = run_agent(task)

    print("\n🤖 FINAL ANSWER:")
    print(result)