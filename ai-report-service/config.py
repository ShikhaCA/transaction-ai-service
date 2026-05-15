import os
from dotenv import load_dotenv

# ================================
# LOAD ENV VARIABLES
# ================================
load_dotenv()


# ================================
# DATABASE CONFIG
# ================================
DB_USER = os.getenv("DB_USER", "root")

DB_PASSWORD = os.getenv("DB_PASSWORD", "root")

DB_HOST = os.getenv("DB_HOST", "mysql")

DB_PORT = os.getenv("DB_PORT", "3306")

DB_NAME = os.getenv("DB_NAME", "transaction_db")


# ================================
# DATABASE URL
# ================================
DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)


# ================================
# GROQ CONFIG
# ================================
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "llama3-8b-8192"
)
