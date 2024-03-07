from flask import Flask, request, jsonify
from flask_cors import CORS
# Import your newly required modules
from langchain_community.embeddings import LlamaCppEmbeddings
from langchain_community.llms import GPT4All
from langchain.vectorstores.faiss import FAISS
from langchain.chains import ConversationalRetrievalChain
from database_helper import Connection
import logging



# Modify the system path to be able to import HSU from a different directory
import sys
sys.path.insert(1, '../LLM/')  # Add the directory above to the sys.path
from HSU import rag  # Now you can import the HSU class

app = Flask(__name__)
CORS(app, resources={r"/chat": {"origins": "*"}})

# The HSU class is now imported from "../LLM/HSU.py", so we don't define it here



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
        
        # Use the HSU class for response generation
        output = rag(user_input)
        test = output.get('answer')
        logging.info(f"Generated response: {test}")
        return jsonify({'reply': test})

    except Exception as e:
        logging.exception(f"An error occurred during chat processing: {e}")
        
        return jsonify({'error': 'Internal Server Error'}), 500

#Database interaction
#initiate connection
#db_connection = Connection()
#db_connection.connect("admin", "Stevencantremember", "admin")

@app.route('/find_users', methods=['GET'])
def find_users():
    db_connection = Connection()
    db_connection.connect("admin", "Stevencantremember", "admin")

    users = db_connection.read("chatbot", "users")

    db_connection.close()

    if users:
        return jsonify({'users': users}), 200
    return jsonify({'error': 'User not found'}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
