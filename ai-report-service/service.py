import time
import logging
import os

from sqlalchemy import text
from openai import OpenAI

from database import SessionLocal


# ================================
# LOGGER
# ================================
logger = logging.getLogger(__name__)


# ================================
# OPENROUTER CLIENT
# ================================
client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

MODEL_NAME = "meta-llama/llama-3-8b-instruct"


# ================================
# GET TRANSACTIONS
# ================================
def get_transactions(user_id: str):

    db = SessionLocal()

    try:

        result = db.execute(
            text(
                """
                SELECT amount, category, status
                FROM transactions
                WHERE user_id = :uid
                """
            ),
            {"uid": user_id}
        )

        data = [dict(row._mapping) for row in result]

        logger.info(f"Transactions fetched: {len(data)}")

        return data

    finally:
        db.close()


# ================================
# PREPROCESS
# ================================
def preprocess(data):

    if not data:
        return {"message": "No transaction data available"}

    total = sum(float(item["amount"]) for item in data)

    category_map = {}

    for item in data:

        category = item["category"]

        category_map[category] = (
            category_map.get(category, 0)
            + float(item["amount"])
        )

    return {
        "total_spending": total,
        "category_breakdown": category_map,
        "sample_records": data[:10]
    }


# ================================
# ASK AI
# ================================
def ask_ai(prompt):

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content


# ================================
# SUMMARY
# ================================
def generate_summary(data):

    start_time = time.time()

    structured_data = preprocess(data)

    prompt = f"""
    Analyze this financial transaction data
    and provide a proper financial summary.

    Data:
    {structured_data}

    Provide:
    - total spending
    - major spending categories
    - spending behavior
    - useful financial suggestions
    """

    result = ask_ai(prompt)

    latency = round(time.time() - start_time, 2)

    logger.info(
        f"AI Summary generated in {latency} seconds"
    )

    return result


# ================================
# CATEGORY INSIGHTS
# ================================
def generate_category_insights(data):

    start_time = time.time()

    structured_data = preprocess(data)

    prompt = f"""
    Analyze category wise spending.

    Data:
    {structured_data}

    Provide:
    - highest spending category
    - lowest spending category
    - category comparison
    - useful insights
    """

    result = ask_ai(prompt)

    latency = round(time.time() - start_time, 2)

    logger.info(
        f"Category insights generated in {latency} seconds"
    )

    return result


# ================================
# TREND ANALYSIS
# ================================
def generate_trend_analysis(data):

    start_time = time.time()

    structured_data = preprocess(data)

    prompt = f"""
    Analyze spending trends.

    Data:
    {structured_data}

    Provide:
    - spending patterns
    - unusual behavior
    - trend observations
    - recommendations
    """

    result = ask_ai(prompt)

    latency = round(time.time() - start_time, 2)

    logger.info(
        f"Trend analysis generated in {latency} seconds"
    )

    return result


# ================================
# FAILURE ANALYSIS
# ================================
def generate_failure_analysis(data):

    start_time = time.time()

    if not data:
        return "No transaction data available."

    failed = [
        item for item in data
        if item["status"].lower() == "failed"
    ]

    if not failed:
        return "No failed transactions found."

    prompt = f"""
    Analyze failed transactions.

    Failed Transactions:
    {failed}

    Provide:
    - possible reasons
    - patterns
    - recommendations
    """

    result = ask_ai(prompt)

    latency = round(time.time() - start_time, 2)

    logger.info(
        f"Failure analysis generated in {latency} seconds"
    )

    return result
