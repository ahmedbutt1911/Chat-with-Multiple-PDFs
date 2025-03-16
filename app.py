import streamlit as st



def main():
    st.set_page_config(page_title="Chat with Multiple PDFs", page_icon="📚", layout="wide")
    st.header("Chat with Multiple PDFs 📚")
    st.text_input("Ask a Quetion about your documents:")

    with st.sidebar:
        st.subheader("Your Documents")
        st.file_uploader("Upload your PDFs Here and click on 'Process'")
        st.button("Process")
        





if __name__=='__main__':
    main()