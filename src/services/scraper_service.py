import requests
from bs4 import BeautifulSoup
import re

class ScraperService:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    def scrape_url(self, url: str) -> dict:
        """
        URL에서 텍스트 콘텐츠를 추출합니다.
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            # 인코딩 처리 (특히 한국어 사이트)
            response.encoding = response.apparent_encoding if response.apparent_encoding else 'utf-8'
            
            soup = BeautifulSoup(response.text, 'lxml')
            
            # 불필요한 태그 제거
            for script_or_style in soup(["script", "style", "nav", "footer", "header"]):
                script_or_style.decompose()

            # 제목 추출
            title = soup.title.string if soup.title else "No Title"
            
            # 본문 텍스트 추출 및 정제
            text = soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            clean_text = '\n'.join(chunk for chunk in chunks if chunk)

            # 너무 긴 텍스트는 지식 베이스용으로 적절히 분할 필요 (추후 구현)
            return {
                "url": url,
                "title": title.strip(),
                "content": clean_text[:5000] # 일단 상위 5000자만 추출
            }
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            return None

if __name__ == "__main__":
    scraper = ScraperService()
    # result = scraper.scrape_url("https://www.google.com")
    # print(result['title'])
