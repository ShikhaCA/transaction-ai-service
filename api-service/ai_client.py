import requests

# AI_SERVICE_URL = "http://127.0.0.1:8001"
# AI_SERVICE_URL = "http://host.docker.internal:8001"
AI_SERVICE_URL = "http://ai-report-service:8001"



# ================================
#  AI SUMMARY
# ================================
def get_ai_summary(user_id):
    try:
        response = requests.get(
            f"{AI_SERVICE_URL}/reports/ai-summary/{user_id}"
        )
        return response.json()
    except Exception as e:
        return {"error": str(e)}


# ================================
#  CATEGORY INSIGHTS
# ================================
def get_category_insights(user_id):
    try:
        response = requests.get(
            f"{AI_SERVICE_URL}/reports/ai-category-insights/{user_id}"
        )
        return response.json()
    except Exception as e:
        return {"error": str(e)}


# ================================
#  TREND ANALYSIS
# ================================
def get_trend_analysis(user_id):
    try:
        response = requests.get(
            f"{AI_SERVICE_URL}/reports/ai-trend/{user_id}"
        )
        return response.json()
    except Exception as e:
        return {"error": str(e)}


# ================================
#  FAILURE ANALYSIS (NEW)
# ================================
def get_failure_analysis(user_id):
    try:
        response = requests.get(
            f"{AI_SERVICE_URL}/reports/ai-failures/{user_id}"
        )
        return response.json()
    except Exception as e:
        return {"error": str(e)}


# ================================
#  RAG QUERY
# ================================
def query_document(query):
    try:
        response = requests.post(
            f"{AI_SERVICE_URL}/rag/query",
            params={"query": query}
        )
        return response.json()
    except Exception as e:
        return {"error": str(e)}


# ================================
#  RAG UPLOAD
# ================================
def upload_document(file):
    try:
        files = {"file": file}
        response = requests.post(
            f"{AI_SERVICE_URL}/rag/upload",
            files=files
        )
        return response.json()
    except Exception as e:
        return {"error": str(e)}