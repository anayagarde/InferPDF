# RAG-data-extraction


https://github.com/user-attachments/assets/35ad00e8-cb42-4ffe-ab0d-b859fcee1da7


- Used Streamlit to build Chatbot UI
- Load PDFs using PyPDF2's PdfReader function
- Split the documents in small chunks using LangChain's RecursiveCharacterTextSplitter method
- Create vector embeddings for each chunk using HuggingFaceEmbeddings
- Add vector embeddings to vector store database - FAISS
- Used ConversationBufferMemory to store chat history in memory
- Generate Response using Cohere LLM model

![image](https://github.com/user-attachments/assets/08a3844e-4975-405c-9b82-7e0dafbdb5a2)

