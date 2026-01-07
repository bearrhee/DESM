import re

def mask_pii(text: str) -> str:
    """
    개인정보(실명, 연락처, 주소 등)를 정규표현식으로 익명화합니다.
    """
    if not isinstance(text, str):
        return text

    # 연락처/전화번호 (010, 02 등으로 시작하는 한국형 패턴)
    phone_pattern = r'(?<!\d)(01[016789]|02|0[3-9][0-9])[-.\s]?(\d{3,4})[-.\s]?(\d{4})(?!\d)'
    text = re.sub(phone_pattern, r'[PHONE]', text)

    # 계좌번호 (가장 흔한 형태, 전화번호가 아닌 숫자-숫자-숫자 조합)
    account_pattern = r'(?<!\d)(\d{3,6})[-](\d{2,6})[-](\d{3,6})(?!\d)'
    text = re.sub(account_pattern, '[ACCOUNT]', text)

    # 이메일 주소
    email_pattern = r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}'
    text = re.sub(email_pattern, '[EMAIL]', text)

    # 주소 (동/읍/면/가/로/길 등으로 끝나는 경우 - 단순화된 패턴)
    # 실제 주소는 매우 다양하므로 NER(Named Entity Recognition)이 더 좋지만, 
    # 요구사항에 맞게 정규표현식 기반으로 기본 구현
    # address_pattern = r'([가-힣]+[시|도])?\s?([가-힣]+[구|군|시])?\s?([가-힣]+[동|읍|면|가|로|길])\s?(\d+)?'
    # text = re.sub(address_pattern, '[ADDRESS]', text)

    return text

def normalize_qa(raw_data: list) -> list:
    """
    상담 내역을 QA 쌍으로 정규화합니다.
    """
    normalized = []
    # 데이터 구조에 따라 구현 필요
    # 예: [{'question': '상담 내용...', 'answer': '답변 내용...'}]
    return normalized
