import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredPDFLoader
from werkzeug.utils import secure_filename
from datetime import datetime
from app.aims import AGENT_CONFIG
from app.aims.langchain.vdb_adapter import OllamaEmbedding
from app.aims.langchain.vdb_adapter import VdbAdapter
from pathlib import Path

import zipfile
import shutil
import time

"""
    Change from accepting a file to seraching for the file in the local system and proceeding from there

"""

 
TEMP_FOLDER = os.getenv('TEMP_FOLDER', './_temp')
EMBEDDING_TYPE = os.getenv("EMBEDDING_TYPE", 'none')
EXTRACT_FOLDER = TEMP_FOLDER + "/_extractions/"

class EmbeddingHandlerLocal():
    db = None
    
    """
        replace path_end with a better named variable
    """
    def __init__(self, path_to_file_or_directory=None):
        global db
        self.path = path_to_file_or_directory
        if "\\" in path_to_file_or_directory:
            self.path = self.path.replace("\\", "\\\\")
            self.path_end = path_to_file_or_directory.split('\\')[-1]
        else:
            self.path_end = path_to_file_or_directory.split('/')[-1]
        db = VdbAdapter(AGENT_CONFIG).get_vector_db()
        
    def allowed_file(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'pdf', 'docx', 'txt'}

    def save_file(self, path):
        print("Path: " + path)
        ct = datetime.now()
        ts = ct.timestamp()

        if "\\" in path:
            file = path.split('\\')[-1]
        else:
            file = path.split('/')[-1]
        filename = str(ts) + "_" + file
        file_path = os.path.join(TEMP_FOLDER, filename)
        print(f" Save file  {path} to {file_path}")
        shutil.copy2(path, file_path)
        return file_path

    def run(self):
        # Check if file is a folder
        if ".zip" in self.path:
            return self.zip_extract(self.path_end, self.path)
        if os.path.isdir(self.path):
            return self.dir_loop(self.path)  
        else:
            return self.embed(self.path_end, self.path)
        
        
        
    def dir_loop(self, folder):
        """
            Read folder
            loop through folder
            for each file
                if file, embed
                if folder, call dir_loop
                
            catch any errors, print them, and continue to loop
        """
        for entry in os.listdir(folder):                ### entry is a string
            try:
                path = os.path.join(folder, entry)

                if os.path.isdir(path):
                    self.dir_loop(path)
                    print("[+] " + entry)
                    continue     
                else:
                    print("[X] " + entry)
                    result = self.embed(entry, path)

                if not result:
                    print("[-] failed to embed" + entry)
            except Exception as e:
                print(f"Error: {str(e)}")
            
        return True
        

    def embed(self, path_end, path):
        if self.allowed_file(path_end):
            saved_path = self.save_file(path)
            try:
                chunks = self.load_and_split_data(saved_path)
                db.add_documents(chunks)        ## Mistral Error Here
                os.remove(saved_path)
                print("Removed:" + saved_path)
                return True
            except Exception as e:
                print("\n\t[%] " + str(e)+"\n")
        return False


    def load_and_split_data(self, file_path):
        print("split File Path: " + file_path)
        ext = file_path.rsplit('.', 1)[1].lower()
        if ext == 'pdf':
            from langchain_community.document_loaders import UnstructuredPDFLoader
            loader = UnstructuredPDFLoader(file_path=file_path)
        elif ext == 'docx':
            from langchain_community.document_loaders import UnstructuredWordDocumentLoader
            loader = UnstructuredWordDocumentLoader(file_path=file_path)
        elif ext == 'txt':
            from langchain_community.document_loaders import UnstructuredFileLoader
            loader = UnstructuredFileLoader(file_path=file_path)
        else:
            raise ValueError('Unsupported file type')
        data = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=7500, chunk_overlap=100)
        return text_splitter.split_documents(data)    