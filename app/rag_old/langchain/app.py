import os
from dotenv import load_dotenv
load_dotenv()
from flask import Flask, request, jsonify, render_template
from .embed import embed
from .query import query
from ...aims.api.vector.get_vector_db import get_vector_db

TEMP_FOLDER = os.getenv('TEMP_FOLDER', './_temp')
os.makedirs(TEMP_FOLDER, exist_ok=True)

app = Flask(__name__)

@app.route('/')
def route_home():
    return render_template('chat.html')


@app.route('/embed', methods=['POST'])
def route_embed():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    embedded = embed(file)

    if embedded:
        return jsonify({"message": "File embedded successfully"}), 200

    return jsonify({"error": "File embedded unsuccessfully"}), 400

@app.route('/query', methods=['POST'])
def route_query():
    data = request.get_json()
    response = query(data.get('query'))

    if response:
        return jsonify({"message": response}), 200

    return jsonify({"error": "Something went wrong"}), 400

@app.route('/list', methods=['GET'])
def route_list():
    db = get_vector_db()
    coll = db.get()  # dict_keys(['ids', 'embeddings', 'documents', 'metadatas'])
    list = []

    for idx in range(len(coll['ids'])):
        id = coll['ids'][idx]
        metadatas = coll['metadatas'][idx]
        list.append({"id": id, "metadatas": metadatas})

    return jsonify(list)

@app.route('/delete/<id>', methods=['DELETE'])
def route_delete(id):
    db = get_vector_db()
    db.delete(id)
    return jsonify({"message": "Document deleted successfully"}), 200


def main():
    port = int(os.getenv('FLASK_RUN_PORT', '60011'))
    #app.config['SERVER_NAME'] = f'localhost:{port}'
    #app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'False').lower()
    app.run(host="0.0.0.0", port=port, debug=False)


if __name__ == '__main__':
    import sys
    sys.exit(main())