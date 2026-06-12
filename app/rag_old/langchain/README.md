# Local RAG PDF Querier

## Description
This project is a Retrieval Augmented Generation (RAG) application that allows users to upload PDF documents and ask questions about their content. It utilizes local Large Language Models (LLMs) for embedding and text generation, and a local vector database for storing and retrieving document chunks. This enables private and offline document querying capabilities.

## Features
- **Upload PDF Documents**: Users can upload PDF files through a web interface. These documents are then processed, chunked, and embedded into a vector database.
- **Query Documents**: Ask questions in natural language through a chat interface to retrieve information from the uploaded PDFs.
- **Local LLMs**: Leverages locally running Ollama models for both embedding documents and generating answers, ensuring data privacy.
- **Vector Database**: Uses ChromaDB to store document embeddings locally.
- **Document Management**: Provides functionality to list and delete documents from the vector store.
- **Web Interface**: Simple chat interface for easy interaction.
- **API Endpoints**: Offers API access for embedding, querying, listing, and deleting documents.

## Technology Stack
- **Backend**: Python, Flask
- **LLM Orchestration**: Langchain
- **LLMs**: Ollama
    - Embedding Model: `nomic-embed-text` (default, configurable)
    - Generation Model: `mistral` (default, configurable)
- **Vector Database**: ChromaDB
- **PDF Processing**: `UnstructuredPDFLoader` (via Langchain)
- **Frontend**: HTML, JavaScript (via Flask templates)
- **Environment Management**: `python-dotenv`

## Prerequisites
- **Python**: Version 3.9 or higher is recommended.
- **Ollama**: Ensure Ollama is installed and running on your system. You can download it from [https://ollama.com/](https://ollama.com/).
- **Ollama Models**: The application requires specific models to be available in your Ollama instance. By default, these are:
    - `nomic-embed-text` (for text embeddings)
    - `mistral` (for generating answers)
  You will be guided to pull these during the setup if they are not already present.
- **Git**: For cloning the repository.

## Installation and Setup
1.  **Clone the Repository**:
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```
    *(Replace `<repository-url>` with the actual URL of this repository and `<repository-directory>` with the name of the cloned folder.)*

2.  **Create a Virtual Environment** (Recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install Dependencies**:
    The `requirements.txt` file contains a list of necessary Python packages.
    ```bash
    pip install -r requirements.txt
    ```
    *Note: The `requirements.txt` file in this project has a UTF-16 encoding with a BOM. If you encounter issues, ensure your pip version can handle it or try re-encoding the file to UTF-8.*

4.  **Set up Environment Variables**:
    Create a `.env` file in the root of the project by copying the example or creating it manually. This file will store configuration variables.
    ```bash
    cp .env.example .env  # If you create an .env.example file later
    ```
    Or, create a `.env` file and add the following (adjust paths and model names as needed):
    ```env
    TEMP_FOLDER=./_temp
    CHROMA_PATH=chroma
    COLLECTION_NAME=local-rag
    TEXT_EMBEDDING_MODEL=nomic-embed-text
    LLM_MODEL=mistral
    # FLASK_RUN_PORT=8080 # Optional: if you want to change the default port
    # FLASK_DEBUG=True # Optional: for development
    ```

5.  **Pull Ollama Models**:
    Ensure your Ollama application is running. Then, pull the required models if you haven't already:
    ```bash
    ollama pull nomic-embed-text
    ollama pull mistral
    ```
    If you've configured different models in your `.env` file, pull those instead.

## Running the Application
1.  **Ensure Ollama is Running**:
    Before starting the Flask application, make sure your Ollama application is running and the necessary models (e.g., `nomic-embed-text`, `mistral`) are accessible.

2.  **Start the Flask Server**:
    Navigate to the project's root directory (where `app.py` is located) in your terminal. If you created a virtual environment, ensure it's activated.
    ```bash
    python app.py
    ```

3.  **Access the Application**:
    Once the server is running, you can access the application by opening your web browser and navigating to:
    [http://localhost:8080](http://localhost:8080) (or the port you configured in your `.env` file).

## Usage

### Web Interface

Once the application is running and accessible in your browser:

1.  **Uploading a PDF**:
    *   On the main page, you'll see an option to "Choose File".
    *   Click it, select a PDF document from your local system, and click "Upload" (or "Embed", check the actual button text in `templates/chat.html`).
    *   The system will process the PDF, embed its content, and store it in the vector database. A success or error message will be displayed.

2.  **Asking Questions**:
    *   After embedding a document (or if documents are already present), type your question into the chat input field at the bottom of the page.
    *   Press Enter or click the "Send" button.
    *   The application will retrieve relevant information from the document(s) and generate an answer using the local LLM. The answer will appear in the chat window.

### API Endpoints

The application provides several API endpoints for programmatic interaction:

*   **`POST /embed`**:
    *   **Description**: Uploads and embeds a PDF file.
    *   **Request**: `multipart/form-data` with a `file` part containing the PDF.
    *   **Responses**:
        *   `200 OK`: `{"message": "File embedded successfully"}`
        *   `400 Bad Request`: `{"error": "No file part"}` or `{"error": "No selected file"}` or `{"error": "File embedded unsuccessfully"}` (e.g. if not a PDF)

*   **`POST /query`**:
    *   **Description**: Submits a query and returns an answer based on the embedded documents.
    *   **Request**: `application/json` with a body like `{"query": "Your question here"}`.
    *   **Responses**:
        *   `200 OK`: `{"message": "The answer to your query..."}`
        *   `400 Bad Request`: `{"error": "Something went wrong"}`

*   **`GET /list`**:
    *   **Description**: Lists all documents currently in the vector database.
    *   **Request**: None
    *   **Responses**:
        *   `200 OK`: `[{"id": "document_id_1", "metadatas": {"source": "/path/to/doc1.pdf", ...}}, ...]`

*   **`DELETE /delete/<id>`**:
    *   **Description**: Deletes a specific document from the vector database by its ID.
    *   **Request**: None (ID is part of the URL path).
    *   **Responses**:
        *   `200 OK`: `{"message": "Document deleted successfully"}`

## Configuration
The application uses environment variables for configuration. These can be set in a `.env` file in the project root.

-   `TEMP_FOLDER`:
    -   **Description**: The directory where uploaded PDF files are temporarily stored before processing.
    -   **Default**: `./_temp`

-   `CHROMA_PATH`:
    -   **Description**: The directory where ChromaDB will persist its data.
    -   **Default**: `chroma`

-   `COLLECTION_NAME`:
    -   **Description**: The name of the collection within ChromaDB where document embeddings are stored.
    -   **Default**: `local-rag`

-   `TEXT_EMBEDDING_MODEL`:
    -   **Description**: The name of the Ollama model used for generating text embeddings. This model must be available in your Ollama instance.
    -   **Default**: `nomic-embed-text`

-   `LLM_MODEL`:
    -   **Description**: The name of the Ollama model used for generating answers to queries. This model must be available in your Ollama instance.
    -   **Default**: `mistral`

-   `FLASK_RUN_PORT` (Optional):
    -   **Description**: The port on which the Flask development server will run.
    -   **Default**: Flask's default is `5000`, but `app.py` sets it to `8080`.

-   `FLASK_DEBUG` (Optional):
    -   **Description**: Set to `True` to run Flask in debug mode (useful for development).
    -   **Default**: `True` in `app.py` when run directly.

**Example `.env` file content:**
```env
TEMP_FOLDER=./_temp_custom
CHROMA_PATH=./chroma_data
COLLECTION_NAME=my_documents_collection
TEXT_EMBEDDING_MODEL=mxbai-embed-large
LLM_MODEL=llama3
FLASK_RUN_PORT=8888
```
Make sure to restart the application after changing any environment variables.
