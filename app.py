import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from sentence_transformers import SentenceTransformer
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_community.llms import HuggingFaceHub
from htmlTemplates import css, bot_template, user_template

def get_pdf_text(pdf_docs):
    Text=""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            Text+=page.extract_text()
    return Text

def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len)

    chunks = text_splitter.split_text(text)
    return chunks
        
def get_vectorestore(text_chunks):
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore

def get_conversation_chain(vectorstore):
    # The token will be loaded from environment variables
    llm = HuggingFaceHub(
        repo_id="google/flan-t5-large", 
        model_kwargs={"temperature": 0.5, "max_length": 512, "device": "cpu"}
    )
    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain

def handle_userinput(user_question):
    if st.session_state.conversation is None:
        st.error("Please upload your PDFs and click on 'Process'")
        return

    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i , message in enumerate(st.session_state.chat_history):
        if i%2==0:
            st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)

def main():
    load_dotenv()
    st.set_page_config(page_title="Chat with Multiple PDFs", page_icon="📚")
    st.markdown(css, unsafe_allow_html=True)

    # Initialize session state variables
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None
    
    st.header("Chat with Multiple PDFs 📚")
    user_question=   st.text_input("Ask a Question about your documents:")

    if user_question:
        handle_userinput(user_question)

    with st.sidebar:
        st.subheader("Your Documents")
        pdf_docs = st.file_uploader(
            "Upload your PDFs Here and click on 'Process'", accept_multiple_files=True)
        if st.button("Process"):  
            with st.spinner("Processing..."):            
                # GET PDFs Text
                raw_text = get_pdf_text(pdf_docs)
                
                # GET THE TEXT CHUNKS

                text_chunks = get_text_chunks(raw_text)

                #CREATE VECTOR STORE
                vectorstore = get_vectorestore(text_chunks)
                #CREATE CONVERSATION CHAIN
                st.session_state.conversation = get_conversation_chain(vectorstore)
              
if __name__=='__main__':
    main()