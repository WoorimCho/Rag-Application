import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredPDFLoader
from werkzeug.utils import secure_filename
from datetime import datetime
# from app.aims.api.vector.get_vector_db import get_vector_db
from app.aims import AGENT_CONFIG
from app.aims.langchain.vdb_adapter import OllamaEmbedding
from app.aims.langchain.vdb_adapter import VdbAdapter
from pathlib import Path

import zipfile
import shutil
import time


 
TEMP_FOLDER = os.getenv('TEMP_FOLDER', './_temp')
EMBEDDING_TYPE = os.getenv("EMBEDDING_TYPE", 'none')
EXTRACT_FOLDER = TEMP_FOLDER + "/_extractions/"

class EmbeddingHandler():
    db = None
    
    def __init__(self, input_file):
        global db
        self.file = input_file
        self.filename = input_file.filename
        db = VdbAdapter(AGENT_CONFIG).get_vector_db()
        
    def allowed_file(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'pdf', 'docx', 'txt'}

    def save_file(self, file):  #better with "file" maybe?
        ct = datetime.now()
        ts = ct.timestamp()
        filename = str(ts) + "_" + secure_filename(file.filename)
        file_path = os.path.join(TEMP_FOLDER, filename)
        file.save(file_path)
        return file_path
    
    def save_file_z(self, file):  #better with "file" maybe?
        print("\n\n\t Saving zipped files\n")
        ct = datetime.now()
        ts = ct.timestamp()
        # orig_path   = Path(file.name)
        # basename    = orig_path.name
        og_file_name = secure_filename(getattr(file, 'filename', getattr(file, 'name', 'uploaded_file')))
        filename = str(ts) + "_" + og_file_name
        file_path = os.path.join(TEMP_FOLDER, filename)
        print("\n\t File Name: " + og_file_name)
        print("\t Temp FOlder: " + TEMP_FOLDER)
        print("\t File Path: " + file_path)

        if hasattr(file, 'save'):
            file.save(file_path)
        else:
            file.seek(0)
            # with file_path.open("wb") as out_f:
            with open(file_path, "xb") as out_f:
                shutil.copyfileobj(file, out_f)

        return file_path

    def run(self):
        # Check if file is a folder
        if ".zip" in self.filename:
            return self.zip_extract(self.filename, self.file)
        if os.path.isdir(self.filename):
            return self.dir_loop(self.filename)  
        else:
            return self.embed(self.filename, self.file, True)
        
        
        
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
                    # filename = entry.filename                            #MUST CHECK THIS LOGIC!!!!!!
                    with open(path, 'rb') as f:
                        result = self.embed(entry, f, False)        #MUST CHECK THIS LOGIC!!!!!!
                if not result:
                    print("[-] failed to embed" + entry)
                time.sleep(1)
            except Exception as e:
                print(f"Error: {str(e)}")
            
        return True
        
    def zip_extract(self, folder, file):
        """
            Read folder
            loop through folder
            for each file
                if file, embed
                if folder, call dir_loop
                
            catch any errors, print them, and continue to loop
        """
        print("\n\n\t Extracting\n" )
        with zipfile.ZipFile(file, 'r') as zip_ref:
            # Iterate through the files in the ZIP
            for file in zip_ref.namelist():
                zip_ref.extract(file, EXTRACT_FOLDER)
        
        print("\n\n\t Looping extracted\n" )
        self.dir_loop(EXTRACT_FOLDER)

        for file in EXTRACT_FOLDER:
            os.remove(file)




        # with zipfile.ZipFile(file, 'r') as zip_file:
        #     root = Path(zip_file, '/')
        #     for entry in root.iterdir(): 
        #         if entry.is_dir():
        #             with entry.open('r') as fp:
        #                 contents = fp.read()
        #                 self.dir_loop(contents)
        #         else:
        #             with entry.open('r') as fp:
        #                 contents = fp.read()
        #                 self.embed(entry.filename, entry) 


            #  for item in zip_file.infolist():
            #     if item.is_dir():
            #         with zip_file.open(item) as file:
            #             self.dir_loop(file)
            #     else:
            #         filename = item                         #MUST CHECK THIS LOGIC!!!!!!
            #         with zip_file.open(item) as file:
            #             self.embed(filename, file)              #MUST CHECK THIS LOGIC!!!!!!
        
        
        """for entry in os.listdir(folder):
            try:
                if os.path.isdir(filename):
                    self.dir_loop(filename)     
                print("[+] " + entry)
                filename = entry                            #MUST CHECK THIS LOGIC!!!!!!
                result = self.embed(filename, entry)        #MUST CHECK THIS LOGIC!!!!!!
                if not result:
                    print("[-] failed to embed" + entry)
            except Exception as e:
                print(f"Error: {str(e)}")"""
        return True
        
    """
        Replace the variable --- none_zip ---with a better named one
    """
    def embed(self, filename, file, none_zip):
        if self.allowed_file(filename):
            if none_zip:
                path = self.save_file(file)
            else:
                path = self.save_file_z(file)

            try:
                chunks = self.load_and_split_data(path)
                db.add_documents(chunks)        ## Mistral Error Here
                os.remove(path)
                return True
            except Exception as e:
                print("\n\t[%] " + str(e)+"\n")
        return False


    def load_and_split_data(self, file_path):
        print("\n\n\tFile Path: " + file_path)
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

"""____________________________________________________________________________"""
# import os
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_community.document_loaders import UnstructuredPDFLoader
# from werkzeug.utils import secure_filename
# from datetime import datetime
# # from app.aims.api.vector.get_vector_db import get_vector_db
# from app.aims import AGENT_CONFIG
# from app.aims.langchain.vdb_adapter import OllamaEmbedding
# from app.aims.langchain.vdb_adapter import VdbAdapter
# from pathlib import Path

# TEMP_FOLDER = os.getenv('TEMP_FOLDER', './_temp')
# EMBEDDING_TYPE = os.getenv("EMBEDDING_TYPE", 'none')

# class EmbeddingHandler():
    
#     file = None
#     file_path = None
#     chunks = None
#     db = None
#     filename = None

#     def vdb_select(self):
#         # llm_provider = AGENT_CONFIG.llm_provider            # os.getenv("LLM_PROVIDER")
#         # embedding_model = AGENT_CONFIG.embedding_model      # os.getenv("TEXT_EMBEDDING_MODEL")
#         # vdb_type = AGENT_CONFIG.vdb_type
#         # return VdbAdapter(llm_provider,embedding_model,vdb_type).get_vector_db()
#         return VdbAdapter(AGENT_CONFIG).get_vector_db()
        

#     def allowed_file(self):
#         return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'pdf', 'docx', 'txt'}

#     def save_file(self):
#         global filename, file_path
#         ct = datetime.now()
#         ts = ct.timestamp()
#         filename = str(ts) + "_" + secure_filename(file.filename)
#         file_path = os.path.join(TEMP_FOLDER, filename)
#         file.save(file_path)

#     def load_and_split_data(self):
#         global chunks
#         ext = file_path.rsplit('.', 1)[1].lower()
#         if ext == 'pdf':
#             from langchain_community.document_loaders import UnstructuredPDFLoader
#             loader = UnstructuredPDFLoader(file_path=file_path)
#         elif ext == 'docx':
#             from langchain_community.document_loaders import UnstructuredWordDocumentLoader
#             loader = UnstructuredWordDocumentLoader(file_path=file_path)
#         elif ext == 'txt':
#             from langchain_community.document_loaders import UnstructuredFileLoader
#             loader = UnstructuredFileLoader(file_path=file_path)
#         else:
#             raise ValueError('Unsupported file type')
#         data = loader.load()
#         text_splitter = RecursiveCharacterTextSplitter(chunk_size=7500, chunk_overlap=100)
#         chunks = text_splitter.split_documents(data)

#     def __init__(self, input_file):
#         global file, filename
#         file = input_file
#         filename = file.filename
    
#     def run(self):
#         global filename
#         try:
#             if os.path.isdir(filename):
#                 directory = filename
#                 for name in os.listdir(directory):
#                     print("[+] " + name)
#                     filename = name 
#                     result = self.embed()
#                     # if not result:
#                     #     return False
#             else:
#                 result = self.embed()
#                 if not result:
#                     return False
#             return True
#         except Exception as e:
#             print(f"Error: {str(e)}")
#             return False
        
#     def embed(self):
#         global db
#         if self.allowed_file():    
#             match EMBEDDING_TYPE.lower():
#                 case "huggingface":
#                     print("huggingface")
                    
#                 case "huggingface_a":
#                     print("hugginface_a")

#                 case _:
#                     self.save_file()
#                     self.load_and_split_data()
#                     # db = get_vector_db()
#                     db = self.vdb_select()
#                     db.add_documents(chunks)
#                     os.remove(file_path)
#             return True
#         else:
#             return False
    
#     def dir_loop(self):
#         global filename
#         try:
#             if os.path.isdir(filename):
#                 directory = filename
#                 for name in os.listdir(directory):
#                     print("[+] " + name)
#                     filename = name 
#                     result = self.embed()
#                     # if not result:
#                     #     return False
#             else:
#                 result = self.embed()
#                 if not result:
#                     return False
#             return True
#         except Exception as e:
#             print(f"Error: {str(e)}")
#             return False

