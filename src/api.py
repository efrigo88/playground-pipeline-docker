from fastapi import FastAPI, HTTPException
from logger import get_logger
from pipeline import run_pipeline

logger = get_logger(__name__)

app = FastAPI()


@app.post("/trigger-pipeline")
def trigger_pipeline():
    """Trigger the data processing pipeline."""
    try:
        run_pipeline()
        return {
            "status": "success",
            "message": "Pipeline completed successfully",
        }
    except Exception as e:
        logger.error("Pipeline failed: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e)) from e
