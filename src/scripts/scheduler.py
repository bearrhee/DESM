from apscheduler.schedulers.blocking import BlockingScheduler
from src.scripts.daily_report import generate_report
from src.scripts.sync_sheets import sync_sheets_to_pinecone
import os
from dotenv import load_dotenv

load_dotenv()

def job_daily_report():
    print("Running Daily Report Job...")
    try:
        generate_report()
    except Exception as e:
        print(f"Error in Daily Report Job: {e}")

def job_sync_knowledge():
    print("Running Knowledge Sync Job (Google Sheets)...")
    spreadsheet_id = os.getenv("SPREADSHEET_ID")
    if spreadsheet_id:
        try:
            sync_sheets_to_pinecone(spreadsheet_id, 'Sheet1!A1:B')
        except Exception as e:
            print(f"Error in Knowledge Sync Job: {e}")
    else:
        print("SPREADSHEET_ID not set in .env. Skipping knowledge sync.")

def start_scheduler():
    scheduler = BlockingScheduler()

    # 1. 매일 아침 8시에 리포트 생성 및 전송
    scheduler.add_job(job_daily_report, 'cron', hour=8, minute=0)
    
    # 2. 매 시간마다 구글 시트 지식 동기화
    scheduler.add_job(job_sync_knowledge, 'interval', hours=1)

    print("DEAS Scheduler started. Press Ctrl+C to exit.")
    print("Scheduled Jobs:")
    print("- Daily Report: Every day at 08:00")
    print("- Knowledge Sync: Every 1 hour")
    
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass

if __name__ == "__main__":
    start_scheduler()
