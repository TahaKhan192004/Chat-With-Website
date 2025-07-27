



# Chat With Website 🔍🤖

This project is a **Retrieval-Augmented Generation (RAG)** system built with **Google Gemini**, **ChromaDB**, and **Streamlit**. It allows users to **crawl any website**, index its content, and then **ask natural language questions** based on the scraped content — all through a clean Streamlit UI.

---

## 🚀 Features

- 🌐 Crawl and scrape any website (up to a user-defined page limit)
- 📄 Extract clean, readable text (removes scripts/styles)
- 🧠 Index documents into a vector store using Sentence Transformers
- 🔍 Query top-matching chunks from the vector store
- 🤖 Get answers using Gemini (via `gemini-1.5-flash`)
- 🖥️ Simple, interactive Streamlit interface

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| `requests` | Download webpage content |
| `BeautifulSoup` | Parse and clean HTML/XML |
| `ChromaDB` | Lightweight vector store |
| `SentenceTransformers` | Embed text chunks for retrieval |
| `Google Generative AI` | Gemini for answering user queries |
| `Streamlit` | Web-based UI |

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/gemini-rag-web-crawler.git
cd gemini-rag-web-crawler
````

### 2. Set up a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure your Gemini API key

Create a `.env` file in the root directory:

```
GEMINI_API_KEY=your_gemini_api_key_here
```

You can get your API key from the [Google AI Studio](https://makersuite.google.com/app/apikey).

---

## ▶️ Running the App

```bash
streamlit run app.py
```

---

## 🧠 How It Works

### 🔎 Crawling (`crawler.py`)

* Starts from a root URL and crawls internal pages (BFS).
* Filters out non-text elements (like `<script>` or `<style>`).
* Stops after a user-specified number of pages.

### 📚 Indexing (`rag.py`)

* Splits text into manageable chunks (\~500 words).
* Embeds them using `all-MiniLM-L6-v2`.
* Stores them in a local ChromaDB collection (`web_docs`).

### ❓ Question Answering (`rag.py`)

* Takes a natural language query.
* Retrieves top 5 relevant chunks from the vector DB.
* Sends the query and context to Gemini to generate an answer.

### 🖥️ Frontend (`app.py`)

* User enters the URL and page limit.
* Clicks "Crawl Website" to begin indexing.
* Then types a question and gets answers from Gemini based on the crawled content.

---

## 🧪 Example Use Case

* URL: `https://scikit-learn.org`
* Question: *"What is GridSearchCV used for?"*
* Gemini responds with a summarized answer based on the actual content of the website.

---

## ✅ Tips for Best Results

* Use websites with clear navigation and accessible content (no login required).
* Set a reasonable `max_pages` limit (e.g., 5–20) to keep things responsive.
* Ask specific, contextual questions after crawling.

---

## 📁 Project Structure

```
.
├── app.py             # Streamlit frontend
├── crawler.py         # BFS website crawler
├── rag.py             # Embedding + Gemini query logic
├── .env               # Gemini API key (not committed)
├── requirements.txt   # Python dependencies
└── README.md          # Project documentation
```
