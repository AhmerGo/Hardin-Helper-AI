from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain_community.embeddings import LlamaCppEmbeddings
from langchain_community.llms import GPT4All
from langchain.vectorstores.faiss import FAISS
from langchain.chains import ConversationalRetrievalChain
from database_helper import Connection
import logging
from bson import json_util
import json
import sys
sys.path.insert(1, '../LLM/')
from HSU import HSU

app = Flask(__name__)
CORS(app, resources={r"/chat": {"origins": "*"}})

@app.route('/')
def index():
    return jsonify({'message': 'API is running'})

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_input = data.get('user_input')
        if not user_input:
            logging.warning("User input is missing")
            return jsonify({'error': 'No user_input provided'}), 400
        output = HSU.rag(user_input)
        test = output.get('answer')
        logging.info(f"Generated response: {test}")
        return jsonify({'reply': test})
    except Exception as e:
        logging.exception(f"An error occurred during chat processing: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/save_chat', methods=['POST'])
def save_chat():
    data = request.get_json()
    user_inputs = data.get('user_inputs', [])
    bot_inputs = data.get('bot_inputs', [])
    if not user_inputs or not bot_inputs:
        return jsonify({'error': 'Missing required parameters'}), 400
    try:
        connection = Connection()
        chat_log = ''
        for user_input, bot_input in zip(user_inputs, bot_inputs):
            chat_log += f'User: {user_input}\nBot: {bot_input}\n\n'
        user_id = 1
        response_flag_1 = 0
        response_flag_2 = 0
        response_flag_3 = 0
        save_flag = 1
        connection.insert_chat_log(user_id, chat_log, response_flag_1, response_flag_2, response_flag_3, save_flag)
        return jsonify({'message': 'Chat log saved successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/find_users', methods=['GET'])
def find_users():
    db_connection = Connection()
    db_connection.connect("admin", "Stevencantremember", "admin")
    with app.app_context():
        users = db_connection.read("chatbot", "users")
        db_connection.close()
        if users:
            users_json = json_util.dumps(users)
            parsed_data = json.loads(users_json)
            return jsonify({'users': parsed_data})
        return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)