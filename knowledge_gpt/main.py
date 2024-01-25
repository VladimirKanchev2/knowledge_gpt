import random
import streamlit as st
import time

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

return_all_chunks = False
show_full_doc = False
full_response = ""


if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant",
                                "content": "Hi User! I am Innovaway assistant and I am ready to help!"}]

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
   
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
       
        result = query_folder(folder_index=folder_index,
            query=prompt,
            return_all=return_all_chunks,
            llm=llm,
        )
       
        for chunk in result.answer.split():
            full_response += chunk + " "
            time.sleep(0.05)
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
        #message_placeholder.markdown(full_response)
        #   message_placeholder.markdown(full_response)
       
st.session_state.messages.append({"role": "assistant", "content": full_response})
