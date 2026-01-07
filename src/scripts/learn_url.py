import sys
import os
from src.services.scraper_service import ScraperService
from src.services.embedding_service import EmbeddingService
from src.services.pinecone_manager import PineconeManager
import uuid
import time

def learn_from_url(url: str):
    """
    URL을 스크래핑하여 지식 베이스에 추가합니다.
    """
    print(f"Starting to learn from: {url}")
    
    # 1. 스크래핑
    scraper = ScraperService()
    scraped_data = scraper.scrape_url(url)
    
    if not scraped_data:
        print("Failed to scrape the URL.")
        return

    # 2. 임베딩 생성 (내용이 길 경우 분할 필요, 여기선 단순 구현)
    embedder = EmbeddingService()
    pc_manager = PineconeManager()
    
    # 텍스트가 너무 길면 청킹(Chunking) - 간단히 1000자 단위
    content = scraped_data['content']
    chunks = [content[i:i+1000] for i in range(0, len(content), 1000)]
    
    vectors_to_upsert = []
    
    for i, chunk in enumerate(chunks):
        print(f"Processing chunk {i+1}/{len(chunks)}...")
        text_to_embed = f"URL: {url}\nTitle: {scraped_data['title']}\nContent: {chunk}"
        embedding = embedder.get_embedding(text_to_embed)
        
        vector_id = f"url_{uuid.uuid4().hex[:8]}"
        vectors_to_upsert.append({
            "id": vector_id,
            "values": embedding,
            "metadata": {
                "platform": "web_learning",
                "source_url": url,
                "title": scraped_data['title'],
                "content": chunk,
                "last_updated": str(time.time()),
                "category": "product_info"
            }
        })

    # 3. Pinecone 업서트
    if vectors_to_upsert:
        pc_manager.upsert_vectors(vectors_to_upsert)
        print(f"Successfully learned from {url}. {len(vectors_to_upsert)} chunks added.")
    else:
        print("No content to upsert.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        target_url = sys.argv[1]
        learn_from_url(target_url)
    else:
        print("Usage: python src/scripts/learn_url.py <URL>")
