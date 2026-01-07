import os
import json
from src.services.naver_talktalk_service import NaverTalkTalkService
from src.utils.masking import mask_pii
from src.scripts.upsert_to_pinecone import run_upsert_pipeline
from src.services.rag_pipeline import RAGPipeline

def run_talktalk_integration_test():
    print("--- Naver TalkTalk Integration Test ---")
    
    # 1. 수집
    print("\n1. Fetching live chat data from Naver TalkTalk...")
    tt_service = NaverTalkTalkService()
    chats = tt_service.get_chat_list()
    
    all_processed_qa = []
    
    for chat in chats:
        print(f"Processing chat history for: {chat['chatId']}")
        messages = tt_service.get_messages(chat['chatId'])
        
        # 2. 마스킹 및 정제
        for msg in messages:
            masked_content = mask_pii(msg['content'])
            all_processed_qa.append({
                "original_id": f"{chat['chatId']}_{messages.index(msg)}",
                "content": masked_content,
                "sender": msg['sender'],
                "timestamp": msg['timestamp']
            })

    # 3. 저장
    output_path = 'data/processed/talktalk_integration_test.json'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(all_processed_qa, f, ensure_ascii=False, indent=4)
    print(f"Refined data saved to {output_path}")

    # 4. Pinecone에 학습 (업서트)
    print("\n2. Upserting TalkTalk knowledge to Pinecone...")
    run_upsert_pipeline(output_path)

    # 5. RAG 테스트 (실제 학습된 내용을 물어보기)
    print("\n3. Testing Agent with the newly learned TalkTalk knowledge...")
    pipeline = RAGPipeline()
    test_query = "사용자의 전화번호가 무엇인지 알고 있나요?" 
    # (주의: 에이전트는 [PHONE]으로 마스킹된 지식을 보게 됨)
    print(f"User Query: {test_query}")
    answer = pipeline.run(test_query)
    print(f"Agent Answer: {answer}")

if __name__ == "__main__":
    run_talktalk_integration_test()
