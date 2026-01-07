import os
import requests
import json
from dotenv import load_dotenv
from src.api.db_manager import DBManager

load_dotenv()

class NaverTalkTalkService:
    def __init__(self):
        # 네이버 톡톡 파트너 API 가이드 기준
        self.access_token = os.getenv("NAVER_TALKTALK_ACCESS_TOKEN")
        self.partner_id = os.getenv("NAVER_TALKTALK_PARTNER_ID")
        self.base_url = "https://gw.talk.naver.com/v2"
        self.db = DBManager()

    def get_chat_list(self, category: str = "전체"):
        """
        로컬 DB에서 상담 목록을 가져옵니다.
        """
        chats = self.db.get_chats(category)
        
        # 만약 DB가 비어있다면 (첫 실행 등), MOCK 데이터로 초기화하거나 실시간 API 호출 시도 가능
        if not chats and not (self.access_token and self.partner_id):
            # MOCK 데이터를 DB에 초기화 (테스트용)
            mock_chats = [
                ("CHAT_001", "user_A", "배송 언제 되나요? (Initial)", "대기"),
                ("CHAT_002", "user_B", "환불하고 싶어요. (Initial)", "진행중"),
                ("CHAT_003", "user_C", "감사합니다! (Initial)", "완료")
            ]
            for c_id, u_id, msg, cat in mock_chats:
                self.db.upsert_chat(c_id, u_id, msg, cat)
            chats = self.db.get_chats(category)
            
        return chats

    def get_messages(self, chat_id: str):
        """
        로컬 DB에서 특정 대화방의 메시지 내역을 가져옵니다.
        """
        messages = self.db.get_messages(chat_id)
        
        # MOCK 데이터 초기화
        if not messages and chat_id.startswith("CHAT_"):
            mock_msgs = [
                ("user", "안녕하세요, 문의드립니다.", None),
                ("partner", "네, 도와드리겠습니다.", None)
            ]
            for s, c, t in mock_msgs:
                self.db.add_message(chat_id, s, c, t)
            messages = self.db.get_messages(chat_id)
            
        return messages

    def handle_webhook(self, event_data: dict):
        """
        네이버 톡톡 Webhook 이벤트를 처리하여 DB에 저장합니다.
        사진, 동영상, 파일, URL 포함
        """
        event_type = event_data.get("event")
        user_id = event_data.get("user")
        chat_id = user_id # user_id를 chat_id로 활용
        
        if event_type == "send":
            content = ""
            msg_type = "text"
            media_url = None
            file_name = None
            
            # 1. 텍스트 메시지
            if "textContent" in event_data:
                content = event_data["textContent"].get("text", "")
                msg_type = "text"
            
            # 2. 이미지 메시지
            elif "imageContent" in event_data:
                media_url = event_data["imageContent"].get("imageUrl", "")
                content = "[이미지 수신]"
                msg_type = "image"
                
            # 3. 파일/동영상 메시지 (가이드 기준 또는 유추)
            elif "fileContent" in event_data:
                media_url = event_data["fileContent"].get("fileUrl", "")
                file_name = event_data["fileContent"].get("fileName", "file")
                content = f"[파일 수신: {file_name}]"
                msg_type = "file"
                
            # 4. 복합 메시지 (카드뷰 등)
            elif "compositeContent" in event_data:
                comp = event_data["compositeContent"]
                title = comp.get("title", "")
                desc = comp.get("description", "")
                content = f"{title}\n{desc}"
                msg_type = "composite"
                if "image" in comp:
                    media_url = comp["image"].get("imageUrl")

            # DB 업데이트
            self.db.upsert_chat(chat_id, user_id, content, "대기")
            self.db.add_message(
                chat_id=chat_id, 
                sender="user", 
                content=content, 
                msg_type=msg_type, 
                media_url=media_url, 
                file_name=file_name
            )
            
            return {"status": "success", "processed": msg_type}
            
        elif event_type == "open":
            return {"status": "success", "processed": "room_open"}
            
        return {"status": "success", "processed": "ignored_event"}

if __name__ == "__main__":
    service = NaverTalkTalkService()
    # print(service.get_chat_list())
