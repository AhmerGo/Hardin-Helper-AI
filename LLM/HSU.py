# HSU.py
import asyncio
import logging
from langchain_community.embeddings import LlamaCppEmbeddings
from langchain_community.llms import GPT4All
from langchain.vectorstores.faiss import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

# Logging setup
logging.basicConfig(filename='chatbot.log', filemode='a', level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class HSU:
    def __init__(self, embeddings, index, device="gpu"):
        self.embeddings = embeddings
        self.index = index
        self.memory = ConversationBufferMemory(input_key="question")
        self.llm = GPT4All(model=self.embeddings.model_path, device=device)
        self.qa = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.index.as_retriever(),
            chain_type="stuff",
            verbose=True,
            max_tokens_limit=4096,
            memory=self.memory,
        )
        self.session_histories = {}
        self.lock = asyncio.Lock()

    async def rag(self, question, session_id):
        async with self.lock:
            if session_id not in self.session_histories:
                self.session_histories[session_id] = []

            chat_history = self.session_histories[session_id]

            try:
                loop = asyncio.get_running_loop()
                result = await loop.run_in_executor(
                    None,
                    lambda: self.qa.invoke({"question": question, "chat_history": chat_history})
                )

                if result is None or 'answer' not in result:
                    logging.error(f"No valid result for session {session_id} with question '{question}'")
                    return {"error": "Failed to process your question. Please try again."}

                chat_history.append((question, result['answer']))
                logging.info(f"Chat History Updated for Session {session_id}: {chat_history}")

                return result
            except Exception as e:
                logging.error(f"An error occurred during the question-answering process for session {session_id}: {e}",
                              exc_info=True)
                return {"error": str(e)}
