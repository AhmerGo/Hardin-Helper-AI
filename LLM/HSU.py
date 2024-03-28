import logging
import torch
from langchain_community.embeddings import LlamaCppEmbeddings
from langchain_community.llms import GPT4All
from langchain.vectorstores.faiss import FAISS
from langchain.chains import ConversationalRetrievalChain


class HSU:
    logging.basicConfig(filename='chatbot.log', level=logging.DEBUG, format='%(asctime)s : %(levelname)s : %(message)s')

    @staticmethod
    def rag(question):
        model_path = "./Models/wizardlm-13b-v1.2.Q4_0.gguf"
        index_path = "./HSU_index"
        embeddings = LlamaCppEmbeddings(model_path=model_path)
        index = FAISS.load_local(index_path, embeddings)
        device = "gpu" if torch.cuda.is_available() else "cpu"
        try:
            llm = GPT4All(model=model_path, device=device)
        except Exception as e:
            logging.error(e, exc_info=True)
            llm = GPT4All(model=model_path)
        # llm = GPT4All(model=model_path, device='gpu')
        qa = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=index.as_retriever(),
            chain_type="stuff",
            verbose=True,
            max_tokens_limit=1000,
        )

        # Chatbot loop
        chat_history = []
        try:
            result = qa({"question": question, "chat_history": chat_history})
            return result
        except Exception as e:
            logging.error(e, exc_info=True)
        # return result
