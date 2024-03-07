import os
from langchain_community.embeddings import LlamaCppEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.llms import GPT4All

class HSU:
    @staticmethod
    def rag(question):
        
        app_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(app_dir, "../LLM/Models/mistral-7b-openorca.Q4_0.gguf")
        index_path = os.path.join(app_dir, "../LLM/HSU_index")
        
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
        # Chatbot loop
        chat_history = []
        result = qa({"question": question, "chat_history": chat_history})
        return result