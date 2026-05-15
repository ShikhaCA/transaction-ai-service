from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


# ================================
# DATABASE URL
# ================================
#DATABASE_URL = "mysql+pymysql://root:1234@host.docker.internal:3306/transactions_db"
DATABASE_URL = "mysql+pymysql://root:root@mysql:3306/transaction_db"

# ================================
# ENGINE
# ================================
engine = create_engine(DATABASE_URL)


# ================================
# SESSION
# ================================
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)


# ================================
# BASE
# ================================
Base = declarative_base()
