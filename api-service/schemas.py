from pydantic import BaseModel, field_validator

from datetime import datetime


# ================================
# TRANSACTION CREATE
# ================================
class TransactionCreate(BaseModel):

    id: str
    user_id: str
    amount: float
    category: str
    status: str

    @field_validator("user_id")
    @classmethod
    def validate_user_id(cls, v):

        if not v or v.strip() == "":
            raise ValueError("user_id cannot be empty")

        return v

    @field_validator("amount")
    @classmethod
    def validate_amount(cls, v):

        if v <= 0:
            raise ValueError("amount must be greater than 0")

        return v

    @field_validator("category")
    @classmethod
    def validate_category(cls, v):

        if not v or v.strip() == "":
            raise ValueError("category cannot be empty")

        return v

    @field_validator("status")
    @classmethod
    def validate_status(cls, v):

        allowed = ["success", "failed"]

        if v.lower() not in allowed:
            raise ValueError(
                "status must be success or failed"
            )

        return v.lower()


# ================================
# TRANSACTION RESPONSE
# ================================
class TransactionResponse(BaseModel):

    id: str
    user_id: str
    amount: float
    category: str
    timestamp: datetime
    status: str

    class Config:
        from_attributes = True


# ================================
# USER REGISTER
# ================================
class UserRegister(BaseModel):

    id: str
    username: str
    password: str


# ================================
# USER LOGIN
# ================================
class UserLogin(BaseModel):

    username: str
    password: str


# ================================
# TOKEN RESPONSE
# ================================
class TokenResponse(BaseModel):

    access_token: str
    token_type: str