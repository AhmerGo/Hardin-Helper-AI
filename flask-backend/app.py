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
from HSU import HSU  # Import the HSU class

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
        output = HSU.rag(user_input)
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

@app.route('/save_chat', methods=['POST'])
def save_chat():
    try:
        data = request.get_json()
        user_inputs = data.get('user_inputs')
        bot_inputs = data.get('bot_inputs')

        if not user_inputs or not bot_inputs:
            logging.warning('User inputs or bot inputs missing')
            return jsonify({'error': 'User inputs or bot inputs missing'}), 400

        db_connection = Connection()
        db_connection.connect("admin", "Stevencantremember", "admin")

        logging.info('Saving chat data')

        # Save user inputs
        for user_input in user_inputs:
            db_connection.create("chatbot", "user_inputs", {
                "user_id": "user_id",  # Replace with appropriate user ID
                "message": user_input
            })

        # Save bot inputs
        for bot_input in bot_inputs:
            db_connection.create("chatbot", "bot_inputs", {
                "user_id": "user_id",  # Replace with appropriate user ID
                "message": bot_input
            })

        db_connection.close()

        logging.info('Chat saved successfully')
        return jsonify({'message': 'Chat saved successfully'}), 200
    except Exception as e:
        logging.error(f'Failed to save chat: {e}', exc_info=True)
        return jsonify({'error': 'Failed to save chat'}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
