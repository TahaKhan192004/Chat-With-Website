import os
import chromadb
from chromadb.utils import embedding_functions
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")
embedder = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.Client()
collection = client.get_or_create_collection("web_docs")

def index_documents(pages):
    if collection.count() != 0:
        collection.delete(where={}) 
    for url, content in pages.items():
        chunks = chunk_text(content)
        for i, chunk in enumerate(chunks):
            collection.add(
                documents=[chunk],
                ids=[f"{url}_{i}"],
                metadatas=[{"source": url}]
            )

def chunk_text(text, chunk_size=500):
    words = text.split()
    return [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]

def query_rag(question):
    embedded_query = embedder.encode(question).tolist()
    results = collection.query(query_embeddings=[embedded_query], n_results=5)
    context = "\n\n".join(results["documents"][0])
    return ask_gemini(question, context)

def ask_gemini(query, context):
    prompt = f"""Answer the question based on the context below:

Context:
{context}

Question:
{query}
"""
    response = model.generate_content(prompt)
    return response.text.strip()
