import os
from dotenv import load_dotenv
from src.services.embedding_service import EmbeddingService
from src.services.model_selector import ModelSelector
from src.services.pinecone_manager import PineconeManager
from src.utils.notifications import send_slack_notification

load_dotenv()

def verify_all():
    print("--- DEAS Integration Verification ---")
    
    # 1. OpenRouter Embedding
    try:
        print("\n1. Testing OpenRouter Embedding...")
        key = os.getenv("OPENROUTER_API_KEY")
        print(f"DEBUG: Key starts with: {key[:10] if key else 'None'}")
        embedder = EmbeddingService()
        emb = embedder.get_embedding("Verify connection")
        print(f"✅ Success! Embedding length: {len(emb)}")
    except Exception as e:
        print(f"❌ OpenRouter Embedding failed: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"DEBUG: Response text: {e.response.text}")

    # 2. OpenRouter Chat (Model Selector)
    try:
        print("\n2. Testing OpenRouter Chat Completion...")
        selector = ModelSelector()
        response = selector.get_completion("Hello", task_type="simple")
        if "오류" in response:
             print(f"❌ Chat failed (Fallback returned).")
        else:
             print(f"✅ Success! Model Response: {response[:100]}...")
    except Exception as e:
        print(f"❌ OpenRouter Chat failed Exception: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"DEBUG Chat Response: {e.response.text}")

    # 3. Pinecone
    try:
        print("\n3. Testing Pinecone Connection...")
        pc_manager = PineconeManager()
        # index.describe_index_stats() 
        print(f"✅ Success! Connected to index: {pc_manager.index_name}")
    except Exception as e:
        print(f"❌ Pinecone failed: {e}")

    # 4. Slack
    try:
        print("\n4. Testing Slack Notification...")
        send_slack_notification("DEAS: Integration Verification System Started! 🚀")
        print(f"✅ Success! Slack message triggered.")
    except Exception as e:
        print(f"❌ Slack failed: {e}")

if __name__ == "__main__":
    verify_all()
