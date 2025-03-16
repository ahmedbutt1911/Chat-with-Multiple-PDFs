import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter




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
    



def main():
    load_dotenv()
    st.set_page_config(page_title="Chat with Multiple PDFs", page_icon="📚", layout="wide")
    st.header("Chat with Multiple PDFs 📚")
    st.text_input("Ask a Quetion about your documents:")

    with st.sidebar:
        st.subheader("Your Documents")
        pdf_docs =st.file_uploader(
            "Upload your PDFs Here and click on 'Process'", accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("Processing..."):
            
                # GET PDFs Text
                raw_text= get_pdf_text(pdf_docs)

                # GET THE TEXT CHUNKS

                text_chunks = get_text_chunks(raw_text)
                st.write(text_chunks)

                #CREATE VECTOR STORE
            

        





if __name__=='__main__':
    main()