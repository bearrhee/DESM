import json
import os
from src.services.embedding_service import EmbeddingService
from src.services.pinecone_manager import PineconeManager
from tqdm import tqdm

def run_upsert_pipeline(input_json: str):
    """
    정제된 JSON 데이터를 읽어 벡터화한 후 Pinecone에 업서트합니다.
    """
    if not os.path.exists(input_json):
        print(f"File not found: {input_json}")
        return

    with open(input_json, 'r', encoding='utf-8') as f:
        data = json.load(f)

    embedder = EmbeddingService()
    pc_manager = PineconeManager()

    vectors_to_upsert = []
    
    for item in tqdm(data, desc="Vectorizing and Upserting"):
        text_to_embed = f"Content: {item['content']}\nSender: {item['sender']}"
        embedding = embedder.get_embedding(text_to_embed)
        
        vectors_to_upsert.append({
            "id": f"talktalk_{item['original_id']}",
            "values": embedding,
            "metadata": {
                "platform": "naver_talktalk",
                "content": item['content'],
                "sender": item['sender'],
                "timestamp": item['timestamp'],
                "category": "customer_inquiry" # 필요시 분류 로직 추가
            }
        })
        
        # 100건씩 배치 처리
        if len(vectors_to_upsert) >= 100:
            pc_manager.upsert_vectors(vectors_to_upsert)
            vectors_to_upsert = []

    # 잔여 데이터 처리
    if vectors_to_upsert:
        pc_manager.upsert_vectors(vectors_to_upsert)

    print("Upsert pipeline finished.")

if __name__ == "__main__":
    raw_json = 'data/processed/talktalk_qa.json'
    if os.path.exists(raw_json):
        run_upsert_pipeline(raw_json)
    else:
        print(f"Error: Processed data not found at {raw_json}")
