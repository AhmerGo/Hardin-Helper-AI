# SCRIPT INFO: This script allows you to create an embeddings and vector store from multiple documents.
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.embeddings import LlamaCppEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.callbacks.base import BaseCallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.vectorstores.faiss import FAISS


# Setup
llama_path = './Models/wizardlm-13b-v1.2.Q4_0.gguf'
# llama_path = './Models/mistral-7b-openorca.Q4_0.gguf'

callback_manager = BaseCallbackManager([StreamingStdOutCallbackHandler()])
loader = DirectoryLoader('./Dataset', show_progress=True)

embeddings = LlamaCppEmbeddings(
    model_path=llama_path,
    n_gpu_layers=41,   # Need more context, different models have different num of layers, load entire model into GPU if it fits
    n_ctx=int(32768),  # Need to use the same context size as the model
    verbose=True,
)


# Split text
def split_chunks(sources):
    chunks = []
    splitter = RecursiveCharacterTextSplitter(chunk_size=575, chunk_overlap=58)
    for chunk in splitter.split_documents(sources):
        # print(chunk)
        chunks.append(chunk)
    return chunks


# Indexing
def create_index(chunks):
    texts = [doc.page_content for doc in chunks]
    metadatas = [doc.metadata for doc in chunks]

    search_index = FAISS.from_texts(texts, embeddings, metadatas=metadatas)

    return search_index


def main():
    # Create Index
    docs = loader.load()
    chunks = split_chunks(docs)
    index = create_index(chunks)
    # Save Index (use this to save the index for later use)
    index.save_local("HSU_index")


if __name__ == "__main__":
    main()
