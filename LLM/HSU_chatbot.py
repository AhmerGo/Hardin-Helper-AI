import logging
from langchain_community.embeddings import LlamaCppEmbeddings
from langchain_community.llms import GPT4All
from langchain.vectorstores.faiss import FAISS
from langchain.chains import ConversationalRetrievalChain
import torch

# Constants
# model_path = "./Models/mistral-7b-openorca.Q4_0.gguf"
model_path = "./Models/wizardlm-13b-v1.2.Q4_0.gguf"
index_path = "./HSU_index"

logging.basicConfig(filename='chatbot.log', level=logging.DEBUG, format='%(asctime)s : %(levelname)s : %(message)s')


# Functions
def initialize_embeddings() -> LlamaCppEmbeddings:
    return LlamaCppEmbeddings(model_path=model_path, pooling="mean")


def main():
    # Main execution
    logging.info("Starting Main...")
    # device = "gpu" if torch.cuda.is_available() else "cpu"
    device = "gpu"
    print(f"Using device: {device}")
    llm = GPT4All(model=model_path, device=device)
    # try:
    #     llm = GPT4All(model=model_path, device=device)
    # except Exception as e:
    #     logging.error(e, exc_info=True)
    #     llm = GPT4All(model=model_path)
    embeddings = initialize_embeddings()
    index = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)

    qa = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=index.as_retriever(),
        chain_type="stuff",
        verbose=True,
        max_tokens_limit=10000,
    )

    # Chatbot loop
    chat_history = []
    print("Welcome to the Hardin-Simmons chatbot! Type 'exit' to stop.")
    while True:
        question = input("Please enter your question: ")

        if question.lower() == 'exit':
            break
        result = qa({"question": question, "chat_history": chat_history})

        print("Answer:", result['answer'])


if __name__ == "__main__":
    main()
