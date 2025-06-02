import os
os.environ["STREAMLIT_WATCHER_TYPE"] = "none"

import streamlit as st    # Streamlit for GUI
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain_community.llms import HuggingFacePipeline
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from transformers import pipeline
from langchain_community.llms import Cohere
from chatTemplate import css, bot_template, user_template, typing_template


def main():
    load_dotenv() # set api keys
    st.set_page_config(page_title="InferPDF", page_icon=":books:")

    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.markdown("""
    <h1 style='text-align: center;
               font-size: 3.2rem;
               background: -webkit-linear-gradient(45deg, #a855f7, #6366f1);
               -webkit-background-clip: text;
               -webkit-text-fill-color: transparent;
               margin-bottom: 0.2rem;'>
       Turn PDFs into Conversations
    </h1>
    <p style='text-align: center;
              font-size: 1.15rem;
              color: #d1d5db;
              margin-top: 0;'>
        Upload any document. Ask anything. Get answers instantly.
    </p>
""", unsafe_allow_html=True)
    
    st.markdown("""
    <style>
    div.stButton > button:first-child {
        border: 2px solid #22c55e;        
        background-color: transparent;
        border-radius: 8px;
        padding: 0.6em 1.2em;
        font-size: 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    div.stButton > button:first-child:hover {
        color: white;
        transform: scale(1.03);
        cursor: pointer;
    }
    </style>
""", unsafe_allow_html=True)


    st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
    user_question = st.text_input("Ask anything about your uploaded PDF…")
    if user_question:
        typing_placeholder = st.empty()
        if st.session_state.conversation:
            typing_placeholder.write(typing_template, unsafe_allow_html=True)
            handle_userinput(user_question, typing_placeholder)
        else:
            st.warning("Please upload and process PDF documents first.")
       

    # st.write(user_template.replace("{{MSG}}", "hello robot"), unsafe_allow_html=True)
    # st.write(bot_template.replace("{{MSG}}", "hello human"), unsafe_allow_html=True)


    # side bar to upload pdf documents
    with st.sidebar:
        st.subheader("Documents :books:")
        pdf_docs = st.file_uploader("Upload your PDFs and click on Analyze", accept_multiple_files=True)
        if st.button("Analyze"):
          # process info here if user clicks on Process
            with st.spinner("Analyzing 🔍 ..."):
                # Get the PDF text
                raw_text = get_pdf_text(pdf_docs)
                # st.write(raw_text)

                # Get the text chunks
                text_chunks = get_text_chunks(raw_text)

                # Create vector store
                vectorstore = get_vectorstore(text_chunks)

                # Create conversation chain
                st.session_state.conversation = get_conversation_chain(vectorstore)
            
            st.success("✅ Documents processed! Start asking questions.")

    
    # st.session_state.conversation -> session state can be used anywhere in application (variable persistent suring entire lifecycle of your application)



def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", ".", " ", ""],
        chunk_size=1000, # 1000 characters in each chunk
        chunk_overlap=200, # overlap of 200 characters for every next new chunk
        length_function=len
    )

    chunks = text_splitter.split_text(text)
    return chunks


def get_vectorstore(chunk):
    embed_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = FAISS.from_texts(texts=chunk, embedding=embed_model)
    return vectorstore


def get_conversation_chain(vectorstore):
    # hf_pipeline = pipeline(
    #     "text2text-generation",
    #     model="google/flan-t5-base",
    #     max_length=512,
    #     temperature=0.3
    # )
    # llm = HuggingFacePipeline(pipeline=hf_pipeline)

    llm = Cohere(model="command-r-plus", temperature=0.3, max_tokens=512)

    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )

    return conversation_chain


def handle_userinput(question, typing_placeholder):
    response = st.session_state.conversation({'question': question})
    st.session_state.chat_history = response['chat_history']
    typing_placeholder.empty()

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)



if __name__ == '__main__':
    main()