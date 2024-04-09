import logging
import threading
from langchain_community.embeddings import LlamaCppEmbeddings
from langchain_community.llms import GPT4All
from langchain.vectorstores.faiss import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

logging.basicConfig(filename='chatbot.log', filemode='a', level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class HSU:
    def __init__(self):
        self.model_path = "../LLM/Models/wizardlm-13b-v1.2.Q4_0.gguf"
        self.index_path = "../LLM/HSU_index"
        self.embeddings = LlamaCppEmbeddings(model_path=self.model_path)
        self.index = FAISS.load_local(self.index_path, self.embeddings, allow_dangerous_deserialization=True)
        self.memory = ConversationBufferMemory(input_key="question")
        self.device = "gpu"
        self.llm = GPT4All(model=self.model_path, device=self.device)
        self.qa = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.index.as_retriever(),
            chain_type="stuff",
            verbose=True,
            max_tokens_limit=4096,
            memory=self.memory
        )
        self.session_histories = {}  # Dictionary to store chat histories for each session
        self.lock = threading.Lock()

    def rag(self, question, session_id):
        try:
            with self.lock:
                # Ensure a separate chat history for each session
                if session_id not in self.session_histories:
                    self.session_histories[session_id] = []  # Initialize a new chat history for the session

                # Retrieve the session-specific chat history
                chat_history = self.session_histories[session_id]

                # Process the question
                result = self.qa.invoke({"question": question, "chat_history": chat_history})

                # Update the session-specific chat history
                chat_history.append((question, result['answer']))

                # Log the updated chat history for debugging
                logging.info(f"Chat History Updated for Session {session_id}: {chat_history}")

                # Return the result
                return result
        except Exception as e:
            logging.error("An error occurred during the question-answering process.", exc_info=True)

