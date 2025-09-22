import os
import logging
from dotenv import load_dotenv
from fastapi import FastAPI
from views import router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv(override=True)

openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    logger.warning("OPENAI_API_KEY is not set in the environment variables.")
else:
    logger.info("OPENAI_API_KEY is available in the environment variables.")

app = FastAPI(title="Network Bot API", version="0.1.0")
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
