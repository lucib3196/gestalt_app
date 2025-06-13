from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from src.ai_workspace.document_loaders import ModuleDocumentLoaderCSV


def main(path_to_save: str):
    filepath = r"src\data\QuestionDataV2_06122025_classified.csv"
    loader = ModuleDocumentLoaderCSV(filepath)
    docs = loader.load()
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    vectorstore = FAISS.from_documents(docs, embeddings)
    vectorstore.save_local(path_to_save)


if __name__ == "__main__":
    print("Generating Vector Store")
    main(path_to_save="src/ai_workspace/vectorstores/module_vectorstore_csv")
