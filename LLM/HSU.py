from langchain_community.embeddings import LlamaCppEmbeddings
from langchain_community.llms import GPT4All
from langchain.vectorstores.faiss import FAISS
from langchain.chains import ConversationalRetrievalChain



class HSU:
    def rag(question):
        
        model_path = "../LLM/Models/mistral-7b-openorca.Q4_0.gguf"
        index_path = "../LLM/HSU_index"
        
        embeddings = LlamaCppEmbeddings(model_path=model_path)
        index = FAISS.load_from_disk(index_path, embeddings)
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