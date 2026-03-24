from langchain_astradb import AstraDBVectorStore
from flipkart.data_converter import DataConverter
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from flipkart.config import Config

class DataIngestor:
    def __init__(self, file_path="data/flipkart_products.csv"):
        self.file_path = file_path
        self.embedding = HuggingFaceEndpointEmbeddings(model=Config.EMBEDDING_MODEL)
        self.vstore = AstraDBVectorStore(
            embedding=self.embedding,
            collection_name="flipkart_database",
            api_endpoint=Config.ASTRA_DB_API_ENDPOINT,
            token=Config.ASTRA_DB_APPLICATION_TOKEN,
        )

    def ingest(self, load_existing=True):
        if load_existing:
            return self.vstore

        docs = DataConverter(self.file_path).convert()

        self.vstore.add_documents(docs)
        return self.vstore
        


