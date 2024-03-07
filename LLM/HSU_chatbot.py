from langchain_community.embeddings import LlamaCppEmbeddings
from langchain_community.llms import GPT4All
from langchain.vectorstores.faiss import FAISS
from langchain.chains import ConversationalRetrievalChain
import torch

model_path = "../LLM/Models/mistral-7b-openorca.Q4_0.gguf"
index_path = "../LLM/HSU_index"


# Functions
def initialize_embeddings(device: str) -> LlamaCppEmbeddings:
    return LlamaCppEmbeddings(model_path=model_path, device=device)


def main():
    # Main execution
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")
    
    llm = GPT4All(model=model_path, n_gpu_layers=20, device=device)
    embeddings = initialize_embeddings(device)
    index = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)
    
    qa = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=index.as_retriever(),
        chain_type="stuff",
        verbose=True,
        max_tokens_limit=1000,
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
