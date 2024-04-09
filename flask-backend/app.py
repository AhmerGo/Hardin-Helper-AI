import logging
import threading
from flask import Flask, request, jsonify
from flask_cors import CORS
import sys

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
sys.path.insert(1, '../LLM/')
from HSU import HSU
app = Flask(__name__)
CORS(app, resources={r"/chat": {"origins": "*"}})
hsu_instance = HSU()
lock = threading.Lock()


@app.route('/')
def index():
    return jsonify({'message': 'API is running'})


@app.route('/chat', methods=['POST'])
def chat():
    try:
        logging.info("Received request at /chat endpoint")

        data = request.get_json()
        user_input = data.get('user_input')
        session_id = data.get('session_id')

        if not user_input:
            logging.warning("User input is missing")
            return jsonify({'error': 'No user_input provided'}), 400

        with lock:
            logging.info(session_id)
            output = hsu_instance.rag(user_input, session_id)
            test = output.get('answer')
            logging.info(f"Generated response: {test}")
            return jsonify({'reply': test})

    except Exception as e:
        logging.exception(f"An error occurred during chat processing: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500


@app.route('/save_chat', methods=['POST'])
def save_chat():
    with app.app_context():
        data = request.get_json()
        user_inputs = data.get('user_inputs', [])
        bot_inputs = data.get('bot_inputs', [])
        if not user_inputs or not bot_inputs:
            return jsonify({'error': 'Missing required parameters'}), 400
        try:
            db_connection = Connection()
            db_connection.connect("admin", "Stevencantremember", "admin")

            chat_log = ''
            for user_input, bot_input in zip(user_inputs, bot_inputs):
                chat_log += f'User: {user_input}\nBot: {bot_input}\n\n'

            print(chat_log)
            user_id = 1
            response_flag_1 = 0
            response_flag_2 = 0
            response_flag_3 = 0
            save_flag = 1
            db_connection.insert_chat_log(user_id, chat_log, response_flag_1, response_flag_2, response_flag_3, save_flag)
            db_connection.close()
            return jsonify({'message': 'Chat log saved successfully'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
