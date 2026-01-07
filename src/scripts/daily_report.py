import os
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
from src.utils.notifications import send_slack_notification

def generate_report():
    """
    주문 및 재고 데이터를 시각화하고 리포트를 생성합니다.
    (네이버 API 연동 부분은 목데이터로 대체)
    """
    # 1. 데이터 수집 (Mock)
    data = {
        'Date': pd.date_range(start='2026-01-01', periods=7),
        'Orders': [120, 150, 180, 140, 200, 250, 230],
        'StockOut': [2, 1, 0, 3, 2, 5, 4]
    }
    df = pd.DataFrame(data)

    # 2. 시각화
    plt.figure(figsize=(10, 6))
    plt.plot(df['Date'], df['Orders'], marker='o', label='Daily Orders')
    plt.bar(df['Date'], df['StockOut'] * 20, alpha=0.3, color='red', label='Stock Out Items (Scaled)')
    plt.title('Daily E-commerce Performance')
    plt.xlabel('Date')
    plt.ylabel('Count')
    plt.legend()
    
    report_image_path = f'data/processed/report_{datetime.now().strftime("%Y%m%d")}.png'
    plt.savefig(report_image_path)
    plt.close()

    # 3. 리포트 텍스트 생성
    latest_orders = df['Orders'].iloc[-1]
    total_stock_out = df['StockOut'].sum()
    
    report_text = f"""
[돈쭐 DEAS 일일 리포트 - {datetime.now().strftime('%Y-%m-%d')}]
✅ 어제 총 주문 건수: {latest_orders}건
⚠️ 현재 재고 부족 품목: {total_stock_out}건 (관리자 확인 필요)
🚀 전일 대비 주문 추이는 그래프를 확인해주세요.
"""

    # 4. 슬랙 전송 (이미지 전송은 추가 API 설정 필요, 여기서는 텍스트 우선)
    send_slack_notification(report_text)
    print(f"Report generated and sent. Image: {report_image_path}")

if __name__ == "__main__":
    generate_report()
