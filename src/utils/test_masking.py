from src.utils.masking import mask_pii

def test_mask_pii():
    test_cases = [
        ("제 전화번호는 010-1234-5678입니다.", "제 전화번호는 [PHONE]입니다."),
        ("이메일은 test@example.com입니다.", "이메일은 [EMAIL]입니다."),
        ("계좌번호는 110-123-456789입니다.", "계좌번호는 [ACCOUNT]입니다."),
    ]
    
    for input_text, expected_output in test_cases:
        result = mask_pii(input_text)
        print(f"Input: {input_text}")
        print(f"Result: {result}")
        assert result == expected_output
        print("Test passed!")

if __name__ == "__main__":
    test_mask_pii()
