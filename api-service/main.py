from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
    UploadFile,
    File,
    APIRouter
)

from fastapi.responses import JSONResponse

from fastapi.exceptions import RequestValidationError

from starlette.exceptions import (
    HTTPException as StarletteHTTPException
)

from fastapi.security import (
    OAuth2PasswordRequestForm
)

from sqlalchemy.orm import Session

from prometheus_fastapi_instrumentator import (
    Instrumentator
)

import uuid

import models
import schemas
import crud

from database import SessionLocal, engine

from logger import logger

from auth import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user
)

from ai_client import (
    get_ai_summary,
    get_category_insights,
    get_trend_analysis,
    get_failure_analysis,
    query_document
)


# ================================
# CREATE TABLES
# ================================
models.Base.metadata.create_all(bind=engine)


# ================================
# FASTAPI APP
# ================================
app = FastAPI()


# ================================
# METRICS SETUP
# ================================
Instrumentator().instrument(app).expose(app)


# ================================
# STANDARD RESPONSE
# ================================
def success_response(
    data=None,
    message="Success"
):

    return {
        "status": "success",
        "message": message,
        "data": data
    }


# ================================
# GLOBAL ERROR HANDLERS
# ================================
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):

    logger.error(f"HTTP Error: {exc.detail}")

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "message": exc.detail
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request,
    exc
):

    logger.error(
        f"Validation Error: {exc.errors()}"
    )

    return JSONResponse(
        status_code=400,
        content={
            "status": "error",
            "message": "Validation failed",
            "details": exc.errors()
        },
    )


@app.exception_handler(Exception)
async def generic_exception_handler(
    request,
    exc
):

    logger.error(
        f"Unexpected Error: {str(exc)}"
    )

    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "Internal server error",
            "details": str(exc)
        },
    )


# ================================
# ROUTER
# ================================
router = APIRouter(
    prefix="/api/v1"
)


# ================================
# DATABASE DEPENDENCY
# ================================
def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# ================================
# HEALTH CHECK
# ================================
@app.get("/")
def home():

    logger.info(
        "Health check API called"
    )

    return {
        "message": "API Service Running 🚀"
    }


# ================================
# REGISTER USER
# ================================
@router.post("/auth/register")
def register_user(
    data: schemas.UserRegister,
    db: Session = Depends(get_db)
):

    existing_user = db.query(
        models.User
    ).filter(
        models.User.username == data.username
    ).first()

    if existing_user:

        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    user = models.User(
        id=str(uuid.uuid4()),
        username=data.username,
        password=hash_password(data.password)
    )

    db.add(user)

    db.commit()

    return success_response(
        {"username": user.username},
        "User registered successfully"
    )


# ================================
# LOGIN USER
# ================================
@router.post("/auth/login")
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    user = db.query(
        models.User
    ).filter(
        models.User.username == form_data.username
    ).first()

    if not user:

        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    if not verify_password(
        form_data.password,
        user.password
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    access_token = create_access_token(
        data={
            "sub": user.username
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# ================================
# CREATE RECORD
# ================================
@router.post("/records")
def create(
    data: schemas.TransactionCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    logger.info(
        f"Creating record for user: {data.user_id}"
    )

    obj = crud.create_transaction(
        db,
        data
    )

    return success_response(
        obj,
        "Record created successfully"
    )


# ================================
# GET ALL RECORDS
# ================================
@router.get("/records")
def get_all_records(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    logger.info(
        "Fetching all records"
    )

    records = crud.get_all(db)

    return success_response(
        records,
        "Records fetched successfully"
    )


# ================================
# GET SINGLE RECORD
# ================================
@router.get("/records/{id}")
def get_record(
    id: str,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    logger.info(
        f"Fetching record ID: {id}"
    )

    obj = crud.get_one(db, id)

    if not obj:

        logger.error(
            f"Record not found: {id}"
        )

        raise HTTPException(
            status_code=404,
            detail="Record not found"
        )

    return success_response(
        obj,
        "Record fetched successfully"
    )


# ================================
# UPDATE RECORD
# ================================
@router.put("/records/{id}")
def update_record(
    id: str,
    data: schemas.TransactionCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    logger.info(
        f"Updating record ID: {id}"
    )

    obj = crud.update_transaction(
        db,
        id,
        data
    )

    if not obj:

        logger.error(
            f"Record not found for update: {id}"
        )

        raise HTTPException(
            status_code=404,
            detail="Record not found"
        )

    return success_response(
        obj,
        "Record updated successfully"
    )


# ================================
# DELETE RECORD
# ================================
@router.delete("/records/{id}")
def delete_record(
    id: str,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    logger.info(
        f"Deleting record ID: {id}"
    )

    obj = crud.delete_transaction(
        db,
        id
    )

    if not obj:

        logger.error(
            f"Record not found for delete: {id}"
        )

        raise HTTPException(
            status_code=404,
            detail="Record not found"
        )

    return success_response(
        {"deleted": True},
        "Record deleted successfully"
    )


# ================================
# AI SUMMARY
# ================================
@router.get("/ai-summary/{user_id}")
def ai_summary(
    user_id: str,
    current_user: models.User = Depends(get_current_user)
):

    logger.info(
        f"AI Summary requested for user: {user_id}"
    )

    result = get_ai_summary(user_id)

    return success_response(
        result,
        "AI summary generated"
    )


# ================================
# CATEGORY INSIGHTS
# ================================
@router.get("/ai-category-insights/{user_id}")
def category_insights(
    user_id: str,
    current_user: models.User = Depends(get_current_user)
):

    logger.info(
        f"Category insights requested for user: {user_id}"
    )

    result = get_category_insights(user_id)

    return success_response(
        result,
        "Category insights generated"
    )


# ================================
# TREND ANALYSIS
# ================================
@router.get("/ai-trend/{user_id}")
def ai_trend(
    user_id: str,
    current_user: models.User = Depends(get_current_user)
):

    logger.info(
        f"Trend analysis requested for user: {user_id}"
    )

    result = get_trend_analysis(user_id)

    return success_response(
        result,
        "Trend analysis generated"
    )


# ================================
# FAILURE ANALYSIS
# ================================
@router.get("/ai-failures/{user_id}")
def ai_failures(
    user_id: str,
    current_user: models.User = Depends(get_current_user)
):

    logger.info(
        f"Failure analysis requested for user: {user_id}"
    )

    result = get_failure_analysis(user_id)

    return success_response(
        result,
        "Failure analysis generated"
    )


# ================================
# RAG QUERY
# ================================
@router.get("/query-doc")
def query_doc(
    query: str,
    current_user: models.User = Depends(get_current_user)
):

    logger.info(
        f"RAG query received: {query}"
    )

    result = query_document(query)

    return success_response(
        result,
        "Query result generated"
    )


# ================================
# DOCUMENT UPLOAD
# ================================
@router.post("/upload-doc")
def upload_doc(
    current_user: models.User = Depends(get_current_user),
    file: UploadFile = File(...)
):

    logger.info(
        f"Uploading file: {file.filename}"
    )

    file_path = f"temp_{file.filename}"

    with open(file_path, "wb") as buffer:

        buffer.write(
            file.file.read()
        )

    logger.info(
        f"File uploaded successfully: {file.filename}"
    )

    return success_response(
        {"file": file.filename},
        "File uploaded successfully"
    )


# ================================
# INCLUDE ROUTER
# ================================
app.include_router(router)