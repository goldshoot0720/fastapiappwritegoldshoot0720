import os

# 僅本地測試時載入 .env 檔案
if os.getenv("APPWRITE_LOCAL_TEST") == "1":
    from dotenv import load_dotenv
    load_dotenv()

from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.query import Query

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse


# 建立 Appwrite Client
def create_appwrite_client():
    client = Client()
    client.set_endpoint(os.getenv("APPWRITE_ENDPOINT", "https://fra.cloud.appwrite.io/v1"))
    client.set_project(os.getenv("APPWRITE_PROJECT_ID"))
    client.set_key(os.getenv("APPWRITE_API_KEY"))
    return client


client = create_appwrite_client()
databases = Databases(client)


# 查詢資料函式
def get_subscription_documents():
    database_id = os.getenv("APPWRITE_DATABASE_ID")
    collection_id = os.getenv("APPWRITE_COLLECTION_ID_SUBSCRIPTION")
    print(f"DEBUG: database_id={database_id}, collection_id={collection_id}")
    return databases.list_documents(
        database_id=database_id, collection_id=collection_id, queries=[]
    )


# FastAPI app 初始化
app = FastAPI()

# CORS 設定
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")  # 例如 "https://railway.com,https://你的前端網域"
if allowed_origins == ["*"]:
    allow_origins = ["*"]
else:
    allow_origins = [origin.strip() for origin in allowed_origins]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,  # 允許的來源清單
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
      <head>
        <title>Hello FastAPI & Appwrite</title>
        <style>
          body { font-family: sans-serif; background: #f0f4f8; padding: 2rem; }
          h1 { color: #0078d7; }
          nav a {
            color: white; background-color: #0078d7;
            padding: 10px 20px; border-radius: 5px; font-weight: bold;
            text-decoration: none; transition: background-color 0.3s ease;
          }
          nav a:hover { background-color: #005fa3; }
          footer { margin-top: 40px; font-size: 0.9rem; color: #666; }
        </style>
      </head>
      <body>
        <h1>Hello, FastAPI & Appwrite!</h1>
        <nav>
          <a href="/subscription">Go to subscription</a>
          <a href="/subscription/appwrite">Go to subscription about appwrite</a>
        </nav>
        <footer>Powered by FastAPI & Appwrite</footer>
      </body>
    </html>
    """


@app.get("/subscription")
async def subscription():
    try:
        return get_subscription_documents()
    except Exception as e:
        return {"error": str(e)}


@app.get("/subscription/{name}")
async def subscription_by_name(name: str):
    try:
        database_id = os.getenv("APPWRITE_DATABASE_ID")
        collection_id = os.getenv("APPWRITE_COLLECTION_ID_SUBSCRIPTION")
        result = databases.list_documents(
            database_id=database_id,
            collection_id=collection_id,
            queries=[Query.equal("name", name)],
        )
        return result
    except Exception as e:
        return {"error": str(e)}


# 本地測試執行用
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
