import streamlit as st
from pathlib import Path
from dotenv import load_dotenv
from main import build_agent, read_context_files

load_dotenv()

st.set_page_config(page_title="Weather Agent AI", page_icon="🌤️", layout="wide")

st.title("🌤️ 🧠 DevPilot")
st.markdown("Ask me anything! I can get weather, search web, or analyze files.")

# Sidebar
with st.sidebar:
    st.header("📁 Upload Files")
    uploaded_files = st.file_uploader(
        "Upload context files", accept_multiple_files=True, type=["txt", "py", "md"]
    )
    st.markdown("### 💡 Examples\n- Weather in Delhi?\n- Explain Python isinstance")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Handle files
    file_content = ""
    if uploaded_files:
        temp_dir = Path("temp_uploads")
        temp_dir.mkdir(exist_ok=True)
        file_paths = []
        for f in uploaded_files:
            path = temp_dir / f.name
            with open(path, "wb") as fp:
                fp.write(f.getbuffer())
            file_paths.append(str(path))
        file_content = read_context_files(file_paths)

    # Get response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                agent = build_agent()
                system_instruction = "You are an assistant. For weather queries, use weather_api tool. For other info, use web_search tool."
                user_message = f"{system_instruction}\n\nQuery: {prompt}\n\nFiles: {file_content}\n\nAnswer using tools when needed."
                result = agent.invoke({"messages": [("user", user_message)]})
                response = result["messages"][-1].content
                st.markdown(response)
                st.session_state.messages.append(
                    {"role": "assistant", "content": response}
                )
            except Exception as e:
                st.error(f"Error: {str(e)}")

if st.sidebar.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    st.rerun()
