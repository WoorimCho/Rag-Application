from langchain.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings

from huggingface_hub import login
from langchain_huggingface import HuggingFaceEmbeddings

from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings

import os
import shutil


CHROMA_PATH = os.getenv('CHROMA_PATH', 'chroma')
COLLECTION_NAME = os.getenv('COLLECTION_NAME', 'local-rag')
TEXT_EMBEDDING_MODEL = os.getenv('TEXT_EMBEDDING_MODEL', 'nomic-embed-text')


# login(HF_TOKEN)

DB_HF_PATH = os.getenv("DB_HF_PATH")
db_name = DB_HF_PATH
hf_embeddings = HuggingFaceEmbeddings(model="sentence-transformers/all-MiniLM-L6-v2")
#How to change the embeddings...^^^



class Vector_Handler():
    vectorstore = None

    def __init__(self):
        HF_TOKEN = os.getenv("HUGGINGFACE_TOKEN")
        login(HF_TOKEN)

        db = self.get_vector_db()
    
    def vector_summary():
        total_vectors = vectorstore.index.ntotal
        dimensions = vectorstore.index.d
        print(f"There are {total_vectors} vectors with {dimensions:,} dimensions in this FAISS vector store.")

    # Any way to actively choose the chunks? Are the chunks just refering to the raw document?
    def get_vector_db(self, chunks):
        global vectorstore
        if os.path.exists(DB_HF_PATH): # or use DB_HF_PATH
            print("FAISS vectorstore already exists. Delete FAISS vectorstore from directory.")
            shutil.rmtree(DB_HF_PATH)

        vectorstore = FAISS.from_documents(
            documents=chunks,  # your chunked documents
            embedding=hf_embeddings
        )

        # Save the FAISS vectorstore manually
        vectorstore.save_local(DB_HF_PATH)

        return vectorstore
    
    # sampling_vector(vectorstore=vectorstore, vector_index=0)

    def sampling_vector(vectorstore: FAISS, vector_index: int) -> None:
        # Get document ID linked to vector index
        doc_id = vectorstore.index_to_docstore_id[vector_index]
        
        # Search in docstore using the ID
        document = vectorstore.docstore.search(doc_id)  # contains page_content & metadata
        print(f"Vector:\n{document}\n\n")
        
        # Retrieve the actual vector values (embedding)
        sample_vector = vectorstore.index.reconstruct(vector_index)
        print(f"This vector has {len(sample_vector)} dimensions:\n{sample_vector[:25]}")  # show first 25 dims
        
        return(document, sample_vector)


