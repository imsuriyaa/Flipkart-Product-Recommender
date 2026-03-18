from langchain_astradb import AstraDBVectorStore
from flipkart.data_converter import DataConverter
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from flipkart.config import Config

class DataIngestion:
    def __init__(self, file_path):
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
        

if __name__ == "__main__":
    ingest = DataIngestion("/Users/suriyaa/Documents/Projects/LLMOps/Flipkart Product Recommender/data/flipkart_product_review.csv")
    ingest.ingest(False)
        

