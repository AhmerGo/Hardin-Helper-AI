from langchain_community.embeddings import LlamaCppEmbeddings
from langchain_community.llms import GPT4All
from langchain.vectorstores.faiss import FAISS
from langchain.chains import ConversationalRetrievalChain


class HSU:
    @staticmethod
    def rag(question):
        model_path = "../LLM/Models/wizardlm-13b-v1.2.Q4_0.gguf"
        index_path = "../LLM/HSU_index"
        embeddings = LlamaCppEmbeddings(model_path=model_path)
        index = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)
        llm = GPT4All(model=model_path, device='gpu')
        qa = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=index.as_retriever(),
            chain_type="stuff",
            verbose=True,
            max_tokens_limit=10000,
            pooling_type='mean'  # Hypothetical parameter
        )


        # Chatbot loop
        chat_history = []
        result = qa({"question": question, "chat_history": chat_history})
        return result
