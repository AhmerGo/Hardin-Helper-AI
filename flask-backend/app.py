from flask import Flask, request, jsonify
from flask_cors import CORS
# Import your newly required modules
from langchain_community.embeddings import LlamaCppEmbeddings
from langchain_community.llms import GPT4All
from langchain.vectorstores.faiss import FAISS
from langchain.chains import ConversationalRetrievalChain

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
            return jsonify({'error': 'No user_input provided'}), 400

        # Use the HSU class for response generation
        output = rag(user_input)
        test = output.get('answer')

        return jsonify({'reply': test})
    except Exception as e:
        print(e)  # For development only, use logging in production
        return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
