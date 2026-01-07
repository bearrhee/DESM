import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

class NaverTalkTalkService:
    def __init__(self):
        # 네이버 톡톡 파트너 API 가이드 기준
        self.access_token = os.getenv("NAVER_TALKTALK_ACCESS_TOKEN")
        self.partner_id = os.getenv("NAVER_TALKTALK_PARTNER_ID")
        self.base_url = "https://gw.talk.naver.com/v2"

    def get_chat_list(self, category: str = "전체"):
        """
        상담 목록(대화방)을 카테고리별로 가져옵니다.
        카테고리: 전체, 대기, 진행중, 보류, 완료, 차단, 스팸함
        """
        # 실제 API 호출 시 category 파라미터 필터링 로직 필요
        
        # MOCK/STUB: 카테고리별 데이터 시뮬레이션
        all_chats = [
            {"chatId": "CHAT_001", "lastMessage": "배송 언제 되나요?", "userId": "user_A", "category": "대기"},
            {"chatId": "CHAT_002", "lastMessage": "환불하고 싶어요.", "userId": "user_B", "category": "진행중"},
            {"chatId": "CHAT_003", "lastMessage": "감사합니다!", "userId": "user_C", "category": "완료"},
            {"chatId": "CHAT_004", "lastMessage": "광고성 스팸입니다.", "userId": "user_D", "category": "스팸함"},
            {"chatId": "CHAT_005", "lastMessage": "이거 교환 되나요?", "userId": "user_E", "category": "보류"},
            {"chatId": "CHAT_006", "lastMessage": "욕설 사용자.", "userId": "user_F", "category": "차단"},
        ]
        
        if category == "전체":
            return all_chats
        return [c for c in all_chats if c['category'] == category]

    def get_messages(self, chat_id: str):
        """
        특정 대화방의 메시지 내역을 가져옵니다.
        """
        # 실시간 데이터를 가져오면서 지식 베이스(Pinecone)에도 저장하는 로직을 통합할 수 있음
        return [
            {"sender": "user", "content": "안녕하세요, 상품 문의드립니다.", "timestamp": "2026-01-08 10:00:00"},
            {"sender": "partner", "content": "네, 어떤 상품이 궁금하신가요?", "timestamp": "2026-01-08 10:01:00"},
            {"sender": "user", "content": "이 티셔츠 사이즈가 어떻게 되나요?", "timestamp": "2026-01-08 10:02:00"}
        ]

if __name__ == "__main__":
    service = NaverTalkTalkService()
    # print(service.get_chat_list())
