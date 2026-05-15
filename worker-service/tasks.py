from celery import Celery
import requests


# ================================
# CELERY CONFIG
# ================================
celery = Celery(
    "worker",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)


# ================================
# DOCUMENT PROCESSING TASK
# ================================
@celery.task
def process_document(file_path):

    print(f"Processing started for: {file_path}")

    response = requests.post(
        "http://ai-report-service:8001/internal/process-document",
        json={
            "file_path": file_path
        }
    )

    print(response.json())

    return {
        "message": "Document processed successfully"
    }