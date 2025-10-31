
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter


class DBService:
    def __init__(self, persist_directory="db"):
        self.vector_store = Chroma(
            embedding_function=OpenAIEmbeddings(),
            persist_directory=persist_directory
        )

    def is_initialized(self) -> bool:
        """Checks if the database is initialized and ready for use."""
        try:
            return self.vector_store._collection.count() > 0
        except Exception as e:
            print(f"\n❌ Error: Failed to check database initialization. Reason: {e}")
            return False

    def store_documents(self, docs):
        text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        texts = text_splitter.split_documents(docs)
        if self.vector_store._collection.count() == 0:
            self.vector_store.add_documents(texts)

    def retrieve_similar(self, query, k=5):
        return self.vector_store.similarity_search(query, k=k)