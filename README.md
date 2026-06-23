# RAG Application

A powerful Retrieval-Augmented Generation (RAG) application that combines document embedding, vector database operations, and large language models to create an intelligent document querying system.

## 📋 Overview

This RAG Application enables you to:
- **Embed Documents**: Convert documents into vector embeddings using state-of-the-art embedding models
- **Store & Retrieve**: Manage embeddings in vector databases (Chroma or FAISS)
- **Query Intelligently**: Ask questions about your documents and get contextual answers powered by LLMs
- **Web Interface**: Access a user-friendly chat interface for document interaction

### Key Features

- **Multi-Model Support**: Compatible with multiple LLM providers (Ollama, Hugging Face)
- **Flexible Embeddings**: Support for both Hugging Face embeddings and Ollama embeddings
- **Vector Database Options**: Seamless integration with Chroma and FAISS databases
- **REST API**: Complete API endpoints for embedding, querying, and document management
- **Chat History**: Automatic tracking of conversations and embedding operations
- **Document Management**: List, delete, and manage documents in your vector database

## 🏗️ Project Structure

```
Rag-Application/
├── app/
│   └── aims/
│       ├── agent/              # AI agent implementations
│       ├── api/
│       │   ├── embedding/      # Document embedding handlers
│       │   ├── query/          # Query processing handlers
│       │   └── web/            # Web history tracking
│       ├── data_load/          # Data loading utilities
│       ├── langchain/          # LLM and vector DB adapters
│       ├── rag_old/            # Legacy RAG implementations
│       ├── test/               # Test modules
│       ├── ai_agent.py         # CLI agent interface
│       └── web_api.py          # Flask web API
├── cmd/
│   ├── web.cmd                 # Windows command-line interface
│   └── TestFiles/              # Test documents and PDFs
├── docs/                       # Documentation
├── env.template                # Environment configuration template
└── .gitignore

```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip or conda
- Ollama (for local LLM inference) or Hugging Face account
- curl (for CLI operations)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/WoorimCho/Rag-Application.git
   cd Rag-Application
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/Scripts/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Configure environment variables**
   ```bash
   cp env.template .env
   ```
   
   Edit `.env` and set your configuration:
   ```env
   # Database paths
   TEMP_FOLDER=./_temp
   CHROMA_PATH=chroma
   FAISS_PATH=faiss
   COLLECTION_NAME=local-rag

   # Embedding model (choose one)
   HF_EMBEDDING_MODEL=sentence-transformers/all-mpnet-base-v2
   # OR
   OLLAMA_EMBEDDING_MODEL=nomic-embed-text

   # LLM model (choose one)
   HF_LLM_MODEL=meta-llama/Llama-3.2-3B-Instruct
   # OR
   OLLAMA_LLM_MODEL=llama3.2:3b

   # API endpoints
   OLLAMA_API_URL=http://localhost:11434
   FLASK_RUN_PORT=60011

   # Optional: Hugging Face authentication
   HUGGINGFACE_TOKEN=your-token-here
   DB_HF_PATH=your-huggingface-path
   ```

### Running the Application

#### **Web API Server**

Start the Flask web API:
```bash
python -m app.aims.web_api
```

The API will be available at `http://localhost:60011` (default port)

#### **Web Interface**

Open your browser and navigate to:
```
http://localhost:60011/
```

A chat interface will load where you can interact with your documents.

#### **CLI Interface (Windows)**

Use the provided batch script:
```bash
cd cmd
web.cmd embed path/to/document.pdf    # Embed a document
web.cmd query "Your question here"    # Query documents
web.cmd list                          # List all documents
web.cmd delete document_id            # Delete a document
```

#### **Python CLI Agent**

Run the AI agent with CLI options:
```bash
python -m app.aims.ai_agent --run
python -m app.aims.ai_agent --load=path/to/documents/
python -m app.aims.ai_agent --help
```

## 📡 API Endpoints

### Embed Document
**POST** `/embed`
- Upload a document for embedding
- **Parameters**: File upload (multipart/form-data)
- **Response**: Success/error message

### Query Vector Database
**POST** `/query`
- Query the embedded documents
- **Body**: `{"query": "Your question here"}`
- **Response**: Relevant answer from LLM

### List Documents
**GET** `/list`
- Retrieve all embedded documents
- **Response**: Array of document metadata and IDs

### Delete Document
**DELETE** `/delete/<document_id>`
- Remove a document from the database
- **Response**: Deletion confirmation

### Home
**GET** `/`
- Serves the chat interface HTML

## 🔧 Configuration

### Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `TEMP_FOLDER` | Temporary storage location | `./_temp` |
| `CHROMA_PATH` | Chroma database path | `chroma` |
| `FAISS_PATH` | FAISS database path | `faiss` |
| `COLLECTION_NAME` | Vector collection name | `local-rag` |
| `HF_EMBEDDING_MODEL` | Hugging Face embedding model | `sentence-transformers/all-mpnet-base-v2` |
| `HF_LLM_MODEL` | Hugging Face LLM model | `meta-llama/Llama-3.2-3B-Instruct` |
| `OLLAMA_API_URL` | Ollama API endpoint | `http://localhost:11434` |
| `OLLAMA_EMBEDDING_MODEL` | Ollama embedding model | `nomic-embed-text` |
| `OLLAMA_LLM_MODEL` | Ollama LLM model | `llama3.2:3b` |
| `FLASK_RUN_PORT` | Flask server port | `60011` |
| `HUGGINGFACE_TOKEN` | Hugging Face API token | `hf_xxx...` |

## 🛠️ Technologies & Stack

- **Backend**: Python, Flask
- **LLM Integration**: LangChain, Ollama, Hugging Face Transformers
- **Vector Databases**: Chroma, FAISS
- **Embeddings**: Sentence Transformers, Nomic Embeddings
- **Frontend**: HTML/CSS/JavaScript (Chat Interface)
- **Environment Management**: python-dotenv

## 📚 Core Components

### LLM Adapter (`langchain/llm_adapter.py`)
Handles LLM provider initialization and management for both Ollama and Hugging Face models.

### Vector Database Adapter (`langchain/vdb_adapter.py`)
Manages interactions with vector databases (Chroma/FAISS) for storing and retrieving embeddings.

### Embedding Handler (`api/embedding/embedding_handler.py`)
Processes documents and converts them into vector embeddings using configured models.

### Query Handler (`api/query/query_handler.py`)
Processes user queries against the vector database and generates responses using the LLM.

### Chat History (`api/web/chat_history.py`)
Tracks conversation history and maintains logs of interactions.

## 📝 Usage Examples

### Embedding a Document
```bash
curl --request POST \
  --url http://localhost:60011/embed \
  --header 'Content-Type: multipart/form-data' \
  --form file=@document.pdf
```

### Querying Documents
```bash
curl --request POST \
  --url http://localhost:60011/query \
  --header 'Content-Type: application/json' \
  --data '{"query": "What is the main topic of the documents?"}'
```

### Listing Documents
```bash
curl --request GET \
  --url http://localhost:60011/list
```

### Deleting a Document
```bash
curl --request DELETE \
  --url http://localhost:60011/delete/document_id_here
```

## 🔌 Supported Models

### Embedding Models
- **Hugging Face**: `sentence-transformers/all-mpnet-base-v2`
- **Ollama**: `nomic-embed-text`

### LLM Models
- **Hugging Face**: `meta-llama/Llama-3.2-3B-Instruct`
- **Ollama**: `llama3.2:3b`, `mistral`, `deepseek-r1:8b`, and others

## ⚙️ System Requirements

- **RAM**: Minimum 8GB (16GB+ recommended for larger models)
- **Disk Space**: Varies based on model and database size
- **GPU**: Optional (recommended for faster embedding and inference)

## 🐛 Troubleshooting

### Common Issues

1. **"OLLAMA_API_URL connection refused"**
   - Ensure Ollama service is running: `ollama serve`
   - Verify the URL in `.env` matches your Ollama setup

2. **"Model not found"**
   - Pull the model first: `ollama pull llama3.2:3b`
   - Verify model name in `.env`

3. **"Port already in use"**
   - Change `FLASK_RUN_PORT` in `.env`
   - Or kill the process using the port

4. **Out of memory errors**
   - Use smaller models
   - Increase swap space
   - Process fewer documents at once

## 📄 License

This project is open source and available under the MIT License.

## 👤 Author

**WoorimCho** - [GitHub Profile](https://github.com/WoorimCho)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

## 📚 Additional Resources

- [LangChain Documentation](https://python.langchain.com/)
- [Chroma Vector DB](https://www.trychroma.com/)
- [FAISS Documentation](https://github.com/facebookresearch/faiss)
- [Ollama](https://ollama.ai/)
- [Hugging Face Hub](https://huggingface.co/)

---

**Last Updated**: June 2026
