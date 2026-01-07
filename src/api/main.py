from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
import json
from src.services.naver_talktalk_service import NaverTalkTalkService
from src.services.rag_pipeline import RAGPipeline
from src.scripts.learn_url import learn_from_url
from src.services.embedding_service import EmbeddingService
from src.services.pinecone_manager import PineconeManager
import uuid
import time

app = FastAPI(title="DEAS Admin API")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class KnowledgeItem(BaseModel):
    question: str
    answer: str

class URLItem(BaseModel):
    url: str

class QueryItem(BaseModel):
    query: str

@app.get("/api/chats")
async def get_chats():
    """상담 내역을 가져옵니다."""
    tt_service = NaverTalkTalkService()
    try:
        chats = tt_service.get_chat_list()
        for chat in chats:
            chat['messages'] = tt_service.get_messages(chat['chatId'])
        return chats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/knowledge/manual")
async def add_manual_knowledge(item: KnowledgeItem):
    """수동으로 QA 지식을 추가합니다."""
    try:
        embedder = EmbeddingService()
        pc_manager = PineconeManager()
        content = f"Q: {item.question}\nA: {item.answer}"
        embedding = embedder.get_embedding(content)
        vector_id = f"manual_{uuid.uuid4().hex[:8]}"
        pc_manager.upsert_vectors([{
            "id": vector_id,
            "values": embedding,
            "metadata": {
                "platform": "dashboard_admin",
                "content": content,
                "sender": "admin",
                "timestamp": str(time.time()),
                "category": "manual_kb"
            }
        }])
        return {"status": "success", "id": vector_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/knowledge/url")
async def add_url_knowledge(item: URLItem):
    """URL에서 지식을 학습합니다."""
    try:
        learn_from_url(item.url)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/query")
async def query_agent(item: QueryItem):
    """에이전트에게 질문합니다 (RAG)."""
    try:
        pipeline = RAGPipeline()
        answer = pipeline.run(item.query)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 정적 파일 서빙 (Dashboard)
@app.get("/favicon.ico")
async def favicon():
    return FileResponse("dashboard/favicon.ico") if os.path.exists("dashboard/favicon.ico") else None

app.mount("/", StaticFiles(directory="dashboard", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
