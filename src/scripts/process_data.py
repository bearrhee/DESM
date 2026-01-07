import pandas as pd
import json
import os
from src.utils.masking import mask_pii

def process_talktalk_excel(file_path: str, output_path: str):
    """
    네이버 톡톡 상담 엑셀 파일을 읽어 처리합니다.
    """
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return

    # 엑셀 파일 로드 (시트 구조에 따라 조정 필요)
    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        print(f"Error reading excel: {e}")
        return

    # 데이터 정제 및 마스킹
    # 예: '메시지내용' 컬럼이 있다고 가정
    processed_data = []
    
    # QA 쌍을 추출하는 로직 (질문과 답변이 번갈아 나오는 등의 구조 분석 필요)
    # 여기서는 단순 예시로 전체 텍스트 마스킹 처리
    for _, row in df.iterrows():
        content = str(row.get('메시지', ''))
        masked_content = mask_pii(content)
        processed_data.append({
            "original_id": row.get('번호', ''),
            "content": masked_content,
            "sender": row.get('보낸사람', ''),
            "timestamp": str(row.get('시간', ''))
        })

    # JSON으로 저장
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(processed_data, f, ensure_ascii=False, indent=4)
    
    print(f"Processed data saved to {output_path}")

if __name__ == "__main__":
    # 실행 예시
    raw_excel = 'data/raw/naver_talktalk_mock.xlsx'
    processed_json = 'data/processed/talktalk_qa.json'
    
    if os.path.exists(raw_excel):
        process_talktalk_excel(raw_excel, processed_json)
    else:
        print(f"Mock file not found at {raw_excel}")
