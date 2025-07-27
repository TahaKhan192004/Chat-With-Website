import streamlit as st
from crawler import crawl_site
from rag import index_documents, query_rag

st.set_page_config(page_title="Gemini RAG App")
st.title("🔍 Website Q&A with AI")

url = st.text_input("Enter the website URL:")
max_pages=st.number_input("Enter the number of subpages you want to scrape")
crawl_btn = st.button("Crawl Website")

if crawl_btn and url:
    with st.spinner("Crawling website..."):
        pages = crawl_site(url,max_pages)
        index_documents(pages)
    st.success(f"Indexed {len(pages)} pages from {url}")

st.markdown("---")

question = st.text_input("Ask a question based on the website content:")

if st.button("Get Answer") and question:
    with st.spinner("Querying..."):
        answer = query_rag(question)
    st.markdown("### Answer")
    st.write(answer)
