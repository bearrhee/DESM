import re

def mask_pii(text: str) -> str:
    """
    개인정보(실명, 연락처, 주소 등)를 정규표현식으로 익명화합니다.
    """
    if not isinstance(text, str):
        return text

    # 1. 계좌번호 (가장 흔한 형태, 세부 패턴이 다양하므로 전화번호보다 먼저 처리)
    account_pattern = r'(?<!\d)(\d{3,6})[-](\d{2,6})[-](\d{3,6})(?!\d)'
    text = re.sub(account_pattern, '[ACCOUNT]', text)

    # 2. 연락처/전화번호 (010, 02 등으로 시작하는 한국형 패턴)
    phone_pattern = r'(?<!\d)(01[016789]|02|0[3-9][0-9])[-.\s]?(\d{3,4})[-.\s]?(\d{4})(?!\d)'
    text = re.sub(phone_pattern, r'[PHONE]', text)

    # 3. 이메일 주소
    email_pattern = r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}'
    text = re.sub(email_pattern, '[EMAIL]', text)

    # 4. 주소 (기본적인 한국 주소 패턴 보완)
    address_pattern = r'[가-힣]+([시|도])\s+[가-힣]+([구|군|시])\s+[가-힣\d]+([동|읍|면|가|로|길])'
    text = re.sub(address_pattern, '[ADDRESS]', text)

    return text

def normalize_qa(raw_data: list) -> list:
    """
    상담 내역을 QA 쌍으로 정규화합니다.
    """
    normalized = []
    # 데이터 구조에 따라 구현 필요
    # 예: [{'question': '상담 내용...', 'answer': '답변 내용...'}]
    return normalized
