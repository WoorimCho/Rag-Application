# .venv\Scripts\activate 

import os
from dotenv import load_dotenv

from app.aims.langchain.llm_adapter import LlmAdapter
load_dotenv()
from flask import Flask, request, jsonify, render_template
from app.aims.langchain.vdb_adapter import VdbAdapter

from app.aims.api.query.query_handler import Query_Handler
from app.aims.api.embedding.embedding_handler import EmbeddingHandler

from app.aims.api.web.chat_history import Chat_History
from app.aims.api.web.embedding_history import Embedding_History

from app.aims import agentConfig




TEMP_FOLDER = os.getenv('TEMP_FOLDER', './_temp')
os.makedirs(TEMP_FOLDER, exist_ok=True)

#llm_provider = AGENT_CONFIG.llm_provider            # os.getenv("LLM_PROVIDER")
#embedding_model = AGENT_CONFIG.embedding_model      # os.getenv("TEXT_EMBEDDING_MODEL")
#vdb_type = AGENT_CONFIG.vdb_type

app = Flask(__name__)
c_history = None
e_history = None 

@app.route('/')
def route_home():
    return render_template('chat.html')


@app.route('/embed', methods=['POST'])
def route_embed():
    if 'file' not in request.files:
        e_history.add("Upload Fail", "None Uploaded")
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        e_history.add("Selection Fail", "None Selected")
        return jsonify({"error": "No selected file"}), 400

    # embedded = EmbeddingHandler(file).run()
    embedded = None
    try:
        embedded = EmbeddingHandler(file).run()
        print("\n\n\t\tEmbedding status:" + str(embedded) +"\n")
    except Exception as e:
        print("\n\n\tException Found:\t" + str(e) + "\n\n")
        e_history.add("Embedding Failed due to: " + str(e), file.filename)
        return jsonify({"error": "File embedded unsuccessfully"}), 400
    finally:
        print("\n\n\tEmbedding status:\t" + str(embedded) +"\n")
        if embedded:
            e_history.add("Embedding Successful", file.filename)
            return jsonify({"message": "File embedded successfully"}), 200
        e_history.add("Embedding Failed", file.filename)
        return jsonify({"error": "File embedded unsuccessfully"}), 400

@app.route('/query', methods=['POST'])
def route_query():
    data = request.get_json()
    c_history.add(user = "User", message=data.get('query')[6:])
    response = None

    #response = Query_Handler(data.get('query')).run()
    # vdb = VdbAdapter(agentConfig).get_vector_db()
    # llm = LlmAdapter(agentConfig).get_llm(vdb=vdb)
    # text = data.get('query')
    # print(f"Query: {text}")
    # response = llm.query(data.get('query'))



    try:            
        response = Query_Handler(data.get('query')).run()
        
    except Exception as e:
        c_history.add(user = "*****System*****", message=str(e))
        return jsonify({"error": "Something went wrong"}), 400
    finally:
        if response:
            # c_history.add(user = "User", message=data.get('query'))
            c_history.add(user = "Chat: "+ str(agentConfig.llm_provider)[12:], message=response)       # May need to ensure that the output is a string
            return jsonify({"message": response}), 200
        c_history.add(user = "Chat: "+ str(agentConfig.llm_provider)[12:], message="Failed, Something went wrong")
        return jsonify({"error": "Something went wrong"}), 400

@app.route('/list', methods=['GET'])
def route_list():
    db = VdbAdapter(agentConfig).get_vector_db()
    coll = db.get() # dict_keys(['ids', 'embeddings', 'documents', 'metadatas'])
    list = []

    for idx in range(len(coll['ids'])):
        id = coll['ids'][idx]
        metadatas = coll['metadatas'][idx]
        list.append({"id": id, "metadatas": metadatas})

    return jsonify(list)

@app.route('/delete/<id>', methods=['DELETE'])
def route_delete(id):
    db = VdbAdapter(agentConfig).get_vector_db()
    db.delete(id)
    return jsonify({"message": "Document deleted successfully"}), 200


def main():
    global c_history, e_history   
    c_history = Chat_History()
    e_history = Embedding_History(c_history.getHistoryFile(), c_history.getLogFile())
    port = int(os.getenv('FLASK_RUN_PORT', '60011'))
    #app.config['SERVER_NAME'] = f'localhost:{port}'
    #app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'False').lower()
    print(f"FLASK_RUN_PORT={port}")
    app.run(host="0.0.0.0", port=port, debug=False)



if __name__ == '__main__':
    import sys
    sys.exit(main())