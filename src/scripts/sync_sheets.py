import os
import time
from src.services.google_sheets_service import GoogleSheetsService
from src.scripts.upsert_to_pinecone import run_upsert_pipeline
import json

def sync_sheets_to_pinecone(spreadsheet_id: str, range_name: str):
    """
    구글 시트의 데이터를 감지하여 Pinecone과 동기화합니다.
    (단순화된 버전: 매번 전체 데이터를 체크하거나 변경 사항을 비교)
    """
    sheets_service = GoogleSheetsService(spreadsheet_id)
    
    # 마지막 동기화 시점의 데이터 해시 등을 저장하여 변경 감지 가능 (생략)
    print("Fetching data from Google Sheets...")
    rows = sheets_service.get_sheet_data(range_name)
    
    if not rows:
        print("No data found in sheets.")
        return

    # 가져온 데이터를 정규화하여 JSON으로 임시 저장 후 파이프라인 실행
    # (실제로는 메모리 상에서 바로 처리하는 것이 좋음)
    knowledge_data = []
    for i, row in enumerate(rows[1:], start=1): # 헤더 제외
        if len(row) >= 2:
            knowledge_data.append({
                "original_id": f"sheet_{i}",
                "content": f"Q: {row[0]}\nA: {row[1]}",
                "sender": "admin",
                "timestamp": str(time.time())
            })

    with open('data/processed/sheet_knowledge.json', 'w', encoding='utf-8') as f:
        json.dump(knowledge_data, f, ensure_ascii=False, indent=4)

    print("Syncing sheet data to Pinecone...")
    run_upsert_pipeline('data/processed/sheet_knowledge.json')

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    ss_id = os.getenv("SPREADSHEET_ID")
    if ss_id:
        sync_sheets_to_pinecone(ss_id, 'Sheet1!A1:B')
    else:
        print("SPREADSHEET_ID not set in .env")
