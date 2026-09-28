import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from tools import (
    check_loan_status,
    get_customer_details,
    calculate_emi,
    get_loan_balance
)


load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")


# Gemini model
llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    temperature=0,
    google_api_key=gemini_api_key
)


# Available tools
tools = [
    check_loan_status,
    get_customer_details,
    calculate_emi,
    get_loan_balance
]


# Create a dictionary so we can find a tool by name
tool_map = {
    tool.name: tool
    for tool in tools
}


# Give tools to Gemini
llm_with_tools = llm.bind_tools(tools)


def run_agent(user_question):
    """
    Process a customer question using Gemini
    and available tools.
    """

    messages = [
        (
            "system",
            """
You are a helpful customer support AI assistant.

You help customers with banking and loan-related questions.

You have access to tools that can:

- Check loan status
- Get customer details
- Calculate EMI
- Get loan balance

Use a tool whenever the user's question requires
information that can be obtained from a tool.

Do not invent customer or loan information.

If the user asks a general question that does not
require a tool, answer normally.

Give the final response in a clear and customer-friendly way.
"""
        ),
        ("human", user_question)
    ]


    # First call: Gemini decides whether to use a tool
    response = llm_with_tools.invoke(messages)

    messages.append(response)


    # Check whether Gemini requested a tool
    if response.tool_calls:

        for tool_call in response.tool_calls:

            tool_name = tool_call["name"]
            tool_args = tool_call["args"]

            # Find the requested tool
            selected_tool = tool_map.get(tool_name)

            if selected_tool is None:
                return "Sorry, I could not find the requested tool."

            # Execute the tool
            tool_result = selected_tool.invoke(tool_args)

            # Add tool result to conversation
            messages.append(
                {
                    "role": "tool",
                    "content": str(tool_result),
                    "tool_call_id": tool_call["id"]
                }
            )


        # Second call: Gemini generates final answer
        final_response = llm_with_tools.invoke(messages)

        content=final_response.content

        if isinstance(content, list):
            return "".join(
                item.get("text","")
                for item in content
                if  isinstance(item,dict)
            )
        return content


    # No tool required
    return response.content

if __name__ == "__main__":
    question = "What is the loan status of customer CUST001?"

    answer = run_agent(question)

    print("\nAI Response:")
    print(answer)