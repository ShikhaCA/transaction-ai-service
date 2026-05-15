from celery import Celery

celery = Celery(
    "worker",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)


@celery.task
def process_document(file_path):

    return {
        "message": f"Task queued for {file_path}"
    }