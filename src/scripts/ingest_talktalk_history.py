import os
import json
from src.services.naver_talktalk_service import NaverTalkTalkService
from src.utils.masking import mask_pii
from src.services.embedding_service import EmbeddingService
from src.services.pinecone_manager import PineconeManager
import uuid
import time
from tqdm import tqdm

def ingest_all_talktalk_history():
    """
    네이버 톡톡의 모든 상담 내역을 가져와서 마스킹 후 지식 베이스에 저장합니다.
    """
    print("--- Starting Full Naver TalkTalk History Ingestion ---")
    
    tt_service = NaverTalkTalkService()
    embedder = EmbeddingService()
    pc_manager = PineconeManager()
    
    # 1. 모든 카테고리의 대화방 목록 수집
    categories = ["대기", "진행중", "보류", "완료", "차단", "스팸함"]
    all_chats = []
    for cat in categories:
        chats = tt_service.get_chat_list(category=cat)
        all_chats.extend(chats)
    
    print(f"Found {len(all_chats)} chats across all categories.")
    
    vectors_to_upsert = []
    
    # 2. 각 대화방의 메시지 수집 및 마스킹
    for chat in tqdm(all_chats, desc="Processing Chats"):
        messages = tt_service.get_messages(chat['chatId'])
        
        # QA 쌍 생성 (간단히 모든 메시지를 하나의 지식으로 묶거나 개별 처리)
        # 여기서는 대화 전체를 하나의 컨텍스트로 묶어 지식화
        full_context = f"Chat ID: {chat['chatId']} | Category: {chat['category']}\n"
        for msg in messages:
            masked_content = mask_pii(msg['content'])
            full_context += f"[{msg['sender']}]: {masked_content}\n"
            
        # 임베딩 생성
        embedding = embedder.get_embedding(full_context)
        
        vector_id = f"tt_hist_{chat['chatId']}"
        vectors_to_upsert.append({
            "id": vector_id,
            "values": embedding,
            "metadata": {
                "platform": "naver_talktalk_history",
                "chat_id": chat['chatId'],
                "category": chat['category'],
                "content": full_context,
                "timestamp": str(time.time())
            }
        })
        
        # 배치 업서트
        if len(vectors_to_upsert) >= 50:
            pc_manager.upsert_vectors(vectors_to_upsert)
            vectors_to_upsert = []

    if vectors_to_upsert:
        pc_manager.upsert_vectors(vectors_to_upsert)
        
    print(f"Ingestion complete. Updated knowledge base with historical data.")

if __name__ == "__main__":
    ingest_all_talktalk_history()
