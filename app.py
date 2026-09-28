import streamlit as st

from agent import run_agent


st.set_page_config(
    page_title="Customer Support AI Agent",
    page_icon="🤖",
    layout="centered"
)


# -----------------------------
# Sidebar
# -----------------------------

with st.sidebar:

    st.title("🤖 Customer Support Agent")

    st.write(
        "AI-powered customer support assistant "
        "using Gemini tool calling."
    )

    st.divider()

    st.subheader("🛠️ Available Tools")

    st.write("• Check Loan Status")
    st.write("• Customer Details")
    st.write("• Calculate EMI")
    st.write("• Loan Balance")

    st.divider()

    st.subheader("🧪 Test Customer IDs")

    st.code("CUST001")
    st.code("CUST002")
    st.code("CUST003")

    st.divider()

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


# -----------------------------
# Main Page
# -----------------------------

st.title("🤖 Customer Support AI Agent")

st.write(
    "Ask questions about customers, loans, loan status, "
    "EMI calculations, and outstanding balances."
)


# -----------------------------
# Chat History
# -----------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# -----------------------------
# User Input
# -----------------------------

user_question = st.chat_input(
    "Ask a customer support question..."
)


if user_question:

    # Display user question
    with st.chat_message("user"):
        st.markdown(user_question)

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_question
        }
    )


    # Generate AI response
    with st.chat_message("assistant"):

        with st.spinner(
            "🤖 Thinking and selecting the right tool..."
        ):

            answer = run_agent(user_question)

        st.markdown(answer)


    # Save AI response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )