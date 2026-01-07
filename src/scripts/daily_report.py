import os
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
from src.utils.notifications import send_slack_notification

from src.services.naver_api_service import NaverCommerceAPI

def generate_report():
    """
    주문 및 재고 데이터를 시각화하고 리포트를 생성합니다.
    """
    api = NaverCommerceAPI()
    
    # 1. 데이터 수집 (REAL API 연동)
    orders = api.get_orders("2026-01-07T00:00:00Z", "2026-01-07T23:59:59Z")
    inventory = api.get_inventory()

    # 데이터 시각화를 위한 가공
    order_count = len(orders)
    low_stock_items = [item['productName'] for item in inventory if item['stockQuantity'] < 3]

    # 시각화 데이터 생성 (최근 7일 트렌드 시뮬레이션)
    dates = pd.date_range(end=datetime.now(), periods=7)
    order_trends = [120, 150, 180, 140, 200, 250, order_count] # 마지막 값만 실제 데이터 반영
    
    # 2. 시각화
    plt.figure(figsize=(10, 6))
    plt.plot(dates, order_trends, marker='o', label='Daily Orders')
    plt.title('Daily E-commerce Order Trend')
    plt.xlabel('Date')
    plt.ylabel('Order Count')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    report_image_path = f'data/processed/report_{datetime.now().strftime("%Y%m%d")}.png'
    os.makedirs('data/processed', exist_ok=True)
    plt.savefig(report_image_path)
    plt.close()

    # 3. 리포트 텍스트 생성
    report_text = f"""
[돈쭐 DEAS 실시간 리포트 - {datetime.now().strftime('%Y-%m-%d')}]
✅ 어제 총 주문 건수: {order_count}건
⚠️ 재고 관리 주의 품목 (3개 미만): {', '.join(low_stock_items) if low_stock_items else '없음'}
🚀 상세 주문 현황:
"""
    for order in orders:
        report_text += f"- {order['productName']} ({order['quantity']}개)\n"

    # 4. 슬랙 전송
    send_slack_notification(report_text)
    print(f"Report generated and sent. Image: {report_image_path}")

if __name__ == "__main__":
    generate_report()
