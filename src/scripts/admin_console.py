import os
import sys
from src.scripts.learn_url import learn_from_url
from src.services.embedding_service import EmbeddingService
from src.services.pinecone_manager import PineconeManager
import uuid
import time

def print_menu():
    print("\n--- DEAS Admin Knowledge Console ---")
    print("1. [URL] 웹페이지 URL에서 상품 정보 학습하기")
    print("2. [QA] 수동으로 질문-답변(QA) 지식 추가하기")
    print("3. [SYNC] 구글 시트 데이터 동기화 실행")
    print("4. [EXIT] 프로그램 종료")
    print("-----------------------------------")

def add_manual_qa():
    question = input("질문(Question)을 입력하세요: ")
    answer = input("답변(Answer)을 입력하세요: ")
    
    if not question or not answer:
        print("질문과 답변을 모두 입력해야 합니다.")
        return

    embedder = EmbeddingService()
    pc_manager = PineconeManager()
    
    content = f"Q: {question}\nA: {answer}"
    embedding = embedder.get_embedding(content)
    
    vector_id = f"manual_{uuid.uuid4().hex[:8]}"
    pc_manager.upsert_vectors([{
        "id": vector_id,
        "values": embedding,
        "metadata": {
            "platform": "manual_admin",
            "content": content,
            "sender": "admin",
            "timestamp": str(time.time()),
            "category": "manual_kb"
        }
    }])
    print("성공적으로 지식이 추가되었습니다.")

def run_admin_console():
    while True:
        print_menu()
        choice = input("원하는 작업 번호를 선택하세요: ")
        
        if choice == '1':
            url = input("학습할 URL을 입력하세요: ")
            if url.startswith("http"):
                learn_from_url(url)
            else:
                print("유효한 URL이 아닙니다.")
        
        elif choice == '2':
            add_manual_qa()
            
        elif choice == '3':
            print("구글 시트 동기화를 시작합니다...")
            # sync_sheets.main() # 연동 시 호출
            os.system('python src/scripts/sync_sheets.py')
            
        elif choice == '4':
            print("관리자 모드를 종료합니다.")
            break
        else:
            print("잘못된 선택입니다. 다시 입력해주세요.")

if __name__ == "__main__":
    run_admin_console()
