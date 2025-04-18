import uvicorn

from api import app
from logger import get_logger

logger = get_logger(__name__)

if __name__ == "__main__":
    # Start API server
    uvicorn.run(app, host="0.0.0.0", port=8000)
