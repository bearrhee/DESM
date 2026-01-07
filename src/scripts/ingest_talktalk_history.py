import os
import pandas as pd
from src.services.naver_talktalk_service import NaverTalkTalkService
from src.api.db_manager import DBManager
from src.utils.masking import mask_pii
from src.services.embedding_service import EmbeddingService
from src.services.pinecone_manager import PineconeManager
import uuid
import time
from tqdm import tqdm

def ingest_from_excel(file_path: str):
    """
    네이버 톡톡 상담 내역 엑셀 파일을 읽어 DB와 Pinecone에 저장합니다.
    """
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    print(f"--- Ingesting from Excel: {file_path} ---")
    
    # pandas로 엑셀 읽기
    df = pd.read_excel(file_path)
    
    db = DBManager()
    embedder = EmbeddingService()
    pc_manager = PineconeManager()
    
    vectors_to_upsert = []
    
    for _, row in tqdm(df.iterrows(), total=len(df), desc="Processing Rows"):
        # 엑셀 컬럼명은 네이버 톡톡 다운로드 양식에 맞춰야 하지만, 
        # 여기서는 일반적인 필드명으로 가정 (필요시 수정)
        user_id = str(row.get('사용자ID', row.get('userId', uuid.uuid4().hex[:8])))
        chat_id = str(row.get('대화방ID', row.get('chatId', user_id)))
        content = str(row.get('메시지내용', row.get('content', '')))
        category = str(row.get('카테고리', row.get('category', '완료'))) # 기본값 완료
        sender = str(row.get('발신자', row.get('sender', 'user')))
        timestamp = str(row.get('일시', row.get('timestamp', datetime.now().isoformat() if 'datetime' in globals() else time.time())))

        # 1. 마스킹 처리
        masked_content = mask_pii(content)
        
        # 2. 로컬 DB 저장
        db.upsert_chat(chat_id, user_id, masked_content, category)
        db.add_message(chat_id, sender, masked_content, timestamp)
        
        # 3. Pinecone 지식화 (RAG용)
        # 상담 전체 흐름을 위해선 chat_id별로 묶는 게 좋지만, 
        # 대량 임포트시엔 메시지 단위 또는 세션 단위로 임베딩
        full_text = f"Category: {category} | Chat: {chat_id}\n[{sender}]: {masked_content}"
        embedding = embedder.get_embedding(full_text)
        
        vector_id = f"excel_{chat_id}_{uuid.uuid4().hex[:4]}"
        vectors_to_upsert.append({
            "id": vector_id,
            "values": embedding,
            "metadata": {
                "platform": "excel_import",
                "chat_id": chat_id,
                "category": category,
                "content": full_text,
                "timestamp": str(timestamp)
            }
        })
        
        if len(vectors_to_upsert) >= 50:
            pc_manager.upsert_vectors(vectors_to_upsert)
            vectors_to_upsert = []

    if vectors_to_upsert:
        pc_manager.upsert_vectors(vectors_to_upsert)
        
    print("Excel ingestion complete.")

if __name__ == "__main__":
    import sys
    from datetime import datetime
    
    # 기본 경로 또는 인자로 받은 경로 처리
    target = "data/raw/naver_talktalk_mock.xlsx"
    if len(sys.argv) > 1:
        target = sys.argv[1]
        
    ingest_from_excel(target)
