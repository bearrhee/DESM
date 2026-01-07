import os
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv

load_dotenv()

class PineconeManager:
    def __init__(self, index_name: str = "deas-knowledge-base"):
        self.pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        self.index_name = index_name
        self.index = self.setup_index()

    def setup_index(self):
        """
        인덱스가 없으면 생성하고, 있으면 연결합니다.
        """
        if self.index_name not in self.pc.list_indexes().names():
            self.pc.create_index(
                name=self.index_name,
                dimension=1536, # text-embedding-3-small default
                metric='cosine',
                spec=ServerlessSpec(
                    cloud='aws',
                    region='us-east-1' # 적절한 리전으로 변경 필요
                )
            )
        return self.pc.Index(self.index_name)

    def upsert_vectors(self, vectors: list):
        """
        벡터 데이터를 업서트합니다.
        vectors format: [{"id": "...", "values": [...], "metadata": {...}}]
        """
        return self.index.upsert(vectors=vectors)

    def query_vectors(self, vector: list, top_k: int = 5, filter: dict = None):
        """
        유사한 벡터를 검색합니다.
        """
        return self.index.query(
            vector=vector,
            top_k=top_k,
            include_metadata=True,
            filter=filter
        )
