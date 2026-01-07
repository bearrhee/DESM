import pandas as pd
import os

def create_mock_excel(file_path="data/raw/naver_talktalk_mock.xlsx"):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    data = {
        '사용자ID': ['user_1', 'user_1', 'user_2', 'user_3', 'user_4', 'user_5'],
        '대화방ID': ['CHAT_001', 'CHAT_001', 'CHAT_002', 'CHAT_003', 'CHAT_004', 'CHAT_005'],
        '메시지내용': [
            '안녕하세요, 배송 문의입니다.', '네, 운송장 번호 부탁드립니다.',
            '환불하고 싶어요.', '상품 정보가 궁금해요.', '광고입니다.', '교환 가능한가요?'
        ],
        '카테고리': ['대기', '대기', '진행중', '완료', '스팸함', '보류'],
        '발신자': ['user', 'partner', 'user', 'user', 'user', 'user'],
        '일시': ['2026-01-08 10:00:00', '2026-01-08 10:05:00', '2026-01-08 11:00:00', '2026-01-08 12:00:00', '2026-01-08 13:00:00', '2026-01-08 14:00:00']
    }
    df = pd.DataFrame(data)
    df.to_excel(file_path, index=False)
    print(f"Mock excel created at: {file_path}")

if __name__ == "__main__":
    create_mock_excel()
