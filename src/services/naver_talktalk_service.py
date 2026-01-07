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

    def get_chat_list(self):
        """
        상담 목록(대화방)을 가져옵니다.
        """
        # 실제 API: GET /v2/partner/chat/list
        # headers = {"Authorization": f"Bearer {self.access_token}"}
        # response = requests.get(f"{self.base_url}/partner/chat/list", headers=headers)
        # return response.json()
        
        # MOCK/STUB for testing if no key
        return [
            {"chatId": "CHAT_001", "lastMessage": "배송 언제 되나요?", "userId": "user_A"},
            {"chatId": "CHAT_002", "lastMessage": "환불하고 싶어요.", "userId": "user_B"}
        ]

    def get_messages(self, chat_id: str):
        """
        특정 대화방의 메시지 내역을 가져옵니다.
        """
        # 실제 API: GET /v2/partner/chat/{chatId}/message/list
        return [
            {"sender": "user", "content": "안녕하세요, 상품 문의드립니다.", "timestamp": "2026-01-08 10:00:00"},
            {"sender": "partner", "content": "네, 어떤 상품이 궁금하신가요?", "timestamp": "2026-01-08 10:01:00"},
            {"sender": "user", "content": "이 티셔츠 사이즈가 어떻게 되나요? 제 번호는 010-1111-2222입니다.", "timestamp": "2026-01-08 10:02:00"}
        ]

if __name__ == "__main__":
    service = NaverTalkTalkService()
    # print(service.get_chat_list())
