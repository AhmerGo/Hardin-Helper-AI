from flask import Flask, request, jsonify, render_template, url_for
from flask_cors import CORS
from gpt4all import GPT4All


app = Flask(__name__)
CORS(app, resources={r"/chat": {"origins": "*"}})

model = GPT4All("orca-mini-3b-gguf2-q4_0.gguf")



@app.route('/')
def index():
    return jsonify({'message': 'API is running'})


@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_input = data.get('user_input')  # Using .get is safer

        if not user_input:
            return jsonify({'error': 'No user_input provided'}), 400

        output = model.generate(prompt=user_input, max_tokens=100)
        return jsonify({'reply': output})
    except Exception as e:
        # Log the error and return a generic error message
        print(e)  # For development only, use logging in production
        return jsonify({'error': 'Internal Server Error'}), 500

#u_in = input("Enter something: ")
#chat(u_in)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
