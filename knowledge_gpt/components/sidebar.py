import os

import streamlit as st
from knowledge_gpt.components.faq import faq
from knowledge_gpt.ui import (
    is_file_valid,
    is_open_ai_key_valid,
    display_file_read_error,
)
from dotenv import load_dotenv


from knowledge_gpt.core.parsing import read_file
from knowledge_gpt.core.chunking import chunk_file
from knowledge_gpt.core.embedding import embed_files

MODEL_LIST = ["gpt-3.5-turbo", "gpt-4"]
EMBEDDING = "openai"
VECTOR_STORE = "faiss"

load_dotenv()


def sidebar():
    
    with st.sidebar:
        
        # st.markdown(
        #    "## How to use\n"
        #    "1. Enter your [OpenAI API key](https://platform.openai.com/account/api-keys) below🔑\n"  # noqa: E501
        #    "2. Upload a pdf, docx, or txt file📄\n"
        #    "3. Ask a question about the document💬\n"
        # )
        # api_key_input = st.text_input(
        #    "OpenAI API Key",
        #    type="password",
        #    placeholder="Paste your OpenAI API key here (sk-...)",
        #    help="You can get your API key from https://platform.openai.com/account/api-keys.",  # noqa: E501
        #    value=os.environ.get("OPENAI_API_KEY", None) or st.session_state.get("OPENAI_API_KEY", ""),
        #)
        #print(Path("/.env"))
        # st.session_state["OPENAI_API_KEY"] = load_dotenv(Path("/.env"))
        st.session_state["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
        #openai_api_key = st.session_state.get("OPENAI_API_KEY")
        st.markdown("---")

        uploaded_file = st.file_uploader(
            "Upload a pdf, docx, or txt file",
            type=["pdf", "docx", "txt"],
            help="Scanned documents are not supported yet!",
        )

        model: str = st.selectbox("Model", options=MODEL_LIST)  # type: ignore

        # with st.expander("Advanced Options"):
        #    return_all_chunks = st.checkbox("Show all chunks retrieved from vector search")
        #    show_full_doc = st.checkbox("Show parsed contents of the document")

        if not uploaded_file:
            st.stop()

        try:
            file = read_file(uploaded_file)
        except Exception as e:
            display_file_read_error(e, file_name=uploaded_file.name)

        chunked_file = chunk_file(file, chunk_size=300, chunk_overlap=0)
        
        st.markdown("---")
        st.markdown("# About")
        st.markdown(
            "📖BlackPeakTechGPT allows you to ask questions about your "
            "technical problems you have and give you an accurate answers. "
        )
        st.markdown(
            "This tool is a work in progress. "
            "Expect new add-ons coming. "  
            "We appreciate your feedback and suggestions.💡"
        )
        #st.markdown("Made by [mmz_001](https://twitter.com/mm_sasmitha)")
        st.markdown("---")
        #faq()

        if not is_file_valid(file):
            st.stop()

        if not is_open_ai_key_valid(st.session_state.get("OPENAI_API_KEY"), model):
            st.stop()
        print(type(model))
        with st.spinner("Indexing document... This may take a while⏳"):
            folder_index = embed_files(
                files=[chunked_file],
                embedding=EMBEDDING if model != "debug" else "debug",
                vector_store=VECTOR_STORE if model != "debug" else "debug",
                openai_api_key=st.session_state.get("OPENAI_API_KEY"),
                )

    return chunked_file, model, folder_index


    
