from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from src.ai_workspace.document_loaders import TopicDocumentLoader

# For documentation for working with the database see https://python.langchain.com/docs/integrations/vectorstores/faiss/#add-items-to-vector-store


def main(path_to_save: str):
    filepath = r"src/data/topic_data_description.json"
    loader = TopicDocumentLoader(filepath=filepath)
    docs = loader.load()
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    vectorstore = FAISS.from_documents(docs, embeddings)

    vectorstore.save_local(path_to_save)


if __name__ == "__main__":
    print("Generating Vector Store")
    main(path_to_save="src/ai_workspace/vectorstores/topic_index")
