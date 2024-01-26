"""Streamlit start file."""
import time
import streamlit as st

from knowledge_gpt.components.sidebar import sidebar

from knowledge_gpt.ui import is_query_valid


from knowledge_gpt.core.caching import bootstrap_caching

from knowledge_gpt.core.qa import query_folder
from knowledge_gpt.core.utils import get_llm


# Uncomment to enable debug mode
# MODEL_LIST.insert(0, "debug")

st.set_page_config(page_title="BlackPeakTechGPT", page_icon="📖", layout="wide")
st.header("📖Black Peak Technologies")

# Enable caching for expensive functions
bootstrap_caching()

chunked_file, model, folder_index = sidebar()
openai_api_key = st.session_state.get("OPENAI_API_KEY")
llm = get_llm(model=model, openai_api_key=openai_api_key, temperature=0)

if not openai_api_key:
    st.warning(
        "Enter your OpenAI API key in the sidebar. You can get a key at"
        " https://platform.openai.com/account/api-keys."
    )

RETURN_ALL_CHUNKS = False

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant",
                                  "content": "Hi Human! " +
                                             "I am Innovaway smart AI. " +
                                             "How can I help you today!"}]

for message in st.session_state.messages:
    if message["role"] == 'assistant':
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    else:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("Ask me anything?"):
    if not is_query_valid(prompt):
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        FULL_RESPONSE = ""

        result = query_folder(folder_index=folder_index,
                              query=prompt,
                              return_all=RETURN_ALL_CHUNKS,
                              llm=llm,
                              )

        for chunk in result.answer.split():
            FULL_RESPONSE += chunk + " "
            time.sleep(0.05)
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(FULL_RESPONSE + "▌")
        # message_placeholder.markdown(FULL_RESPONSE)

    st.session_state.messages.append({"role": "assistant",
                                      "content": FULL_RESPONSE})
