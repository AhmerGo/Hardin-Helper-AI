from flask import Flask, request, jsonify
from flask_cors import CORS
# Import your newly required modules
from langchain_community.embeddings import LlamaCppEmbeddings
from langchain_community.llms import GPT4All
from langchain.vectorstores.faiss import FAISS
from langchain.chains import ConversationalRetrievalChain

app = Flask(__name__)
CORS(app, resources={r"/chat": {"origins": "*"}})

# Assuming you've set up your HSU class as provided
class HSU:
    @staticmethod
    def rag(question):
        model_path = "./Models/mistral-7b-openorca.Q4_0.gguf"
        index_path = "./HSU_index"
        embeddings = LlamaCppEmbeddings(model_path=model_path)
        index = FAISS.load_local(index_path, embeddings)
        llm = GPT4All(model=model_path)
        qa = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=index.as_retriever(),
            chain_type="stuff",
            verbose=True,
            max_tokens_limit=1000,
        )
        chat_history = []
        result = qa({"question": question, "chat_history": chat_history})
        return result

# Instantiate your HSU class
hsu = HSU()

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
        output = hsu.rag(user_input)
        return jsonify({'reply': output})
    except Exception as e:
        print(e)  # For development only, use logging in production
        return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
