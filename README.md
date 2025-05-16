 PDF Question Answering System 
A full-stack Django application that allows users to upload PDF documents and ask questions based on the content. It uses Retrieval-Augmented Generation (RAG) to provide accurate, context-aware answers derived directly from the uploaded document.

🚀 Features
📁 Upload PDF files through a user-friendly interface.

🤖 Ask questions based on the uploaded content.

🧠 RAG-based architecture: combines retrieval of document chunks with language generation.

🔐 Session-based memory: questions and answers are stored per session.

💾 File-based caching of answers for improved performance.

🖥️ Full-stack Django application with clean UI.

🛠️ Tech Stack
Backend: Django, Langchain, FAISS / ChromaDB (or any vector DB)

Frontend: HTML, CSS, JavaScript (with Django templates)

PDF Parsing: PyMuPDF / pdfminer / PyPDF2

Embedding & Retrieval: OpenAI / Hugging Face Transformers + Vector Store

Language Model: OpenAI GPT / HuggingFace LLMs

🧠 How It Works (RAG Overview)
Document Upload: User uploads a PDF.

Chunking: PDF content is split into smaller chunks.

Embedding: Each chunk is converted into vector embeddings.

Storage: Embeddings are stored in a vector database (e.g., FAISS).

Question Input: User submits a question.

Retrieval: Top relevant chunks are retrieved based on similarity.

Answer Generation: Retrieved context is passed to a language model to generate a final answer.

