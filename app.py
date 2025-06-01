import os
os.environ["STREAMLIT_WATCHER_TYPE"] = "none"

import streamlit as st    # Streamlit for GUI
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.llms import HuggingFacePipeline
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from transformers import pipeline
from langchain_community.llms import Cohere


def main():
    load_dotenv() # set api keys
    st.set_page_config(page_title="Chat with multiple PDFs", page_icon=":books:")

    st.header("Chat with multiple PDFs :books:")
    st.text_input("Ask a question about your documemts:")

    # side bar to upload pdf documents
    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader("Upload your PDFs here and click on Process", accept_multiple_files=True)
        if st.button("Process"):
          # process info here if user clicks on Process
            with st.spinner("Processing"):
                # Get the PDF text
                raw_text = get_pdf_text(pdf_docs)
                # st.write(raw_text)

                # Get the text chunks
                text_chunks = get_text_chunks(raw_text)
                st.write(text_chunks)

                # Create vector store
                vectorstore = get_vectorstore(text_chunks)

                # Create conversation chain
                convo = get_conversation_chain(vectorstore)



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




if __name__ == '__main__':
    main()