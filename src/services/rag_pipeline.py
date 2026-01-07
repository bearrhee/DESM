from src.services.embedding_service import EmbeddingService
from src.services.pinecone_manager import PineconeManager
from src.services.model_selector import ModelSelector

class RAGPipeline:
    def __init__(self):
        self.embedder = EmbeddingService()
        self.pc_manager = PineconeManager()
        self.model_selector = ModelSelector()

    def run(self, user_query: str):
        """
        사용자 질문에 대해 RAG 파이프라인을 실행합니다.
        """
        # 1. 질문 임베딩
        query_vector = self.embedder.get_embedding(user_query)
        
        # 2. 관련 정보 검색 (Pinecone)
        search_results = self.pc_manager.query_vectors(query_vector, top_k=3)
        
        context = ""
        for match in search_results['matches']:
            context += f"Information: {match['metadata']['content']}\n"

        # 3. 모델 선택 및 답변 생성
        prompt = f"""
당신은 '돈쭐' 쇼핑몰의 전문 상담 에이전트입니다. 
아래 제공된 [Context]를 바탕으로 사용자의 [Question]에 친절하게 답변해주세요.
이미지에 대한 질문이나 복잡한 계산이 필요하면 전문가에게 연결하겠다고 안내하세요.

[Context]
{context}

[Question]
{user_query}

답변:
"""
        # 질문의 복잡도에 따라 모델 선택 (여기선 예시로 context 유무로 판단)
        task_type = "simple" if len(context) < 500 else "complex"
        
        answer = self.model_selector.get_completion(prompt, task_type)
        
        return answer

if __name__ == "__main__":
    pipeline = RAGPipeline()
    # print(pipeline.run("배송 기간이 얼마나 걸리나요?"))
    pass
