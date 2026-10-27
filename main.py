import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from databricks.sdk import WorkspaceClient

# Load environment variables from .env file
load_dotenv()

app = FastAPI(title="Databricks FastAPI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class EchoMessage(BaseModel):
    message: str


@app.get("/api/health")
def health_check():
    return {"status": "healthy", "mode": "M2M Backend Active"}


@app.get("/api/secure-data")
def get_secure_data(request: Request):
    """
    Example of using the Databricks WorkspaceClient configured via
    environment variables (DATABRICKS_HOST, DATABRICKS_CLIENT_ID & DATABRICKS_CLIENT_SECRET)
    """
    try:
        # WorkspaceClient initializes using the environment variables
        w = WorkspaceClient(
            host=os.getenv("DATABRICKS_HOST"),
            client_id=os.getenv("DATABRICKS_CLIENT_ID"),
            client_secret=os.getenv("DATABRICKS_CLIENT_SECRET")
        )

        # Perform an M2M operation, querying the service principal/user info
        current_user = w.current_user.me()

        return {
            "m2m_status": "Success",
            "service_principal": current_user.user_name,
            "data": [
                {"id": 1, "item": "Secure Delta Lake Metric", "value": 99.1},
                {"id": 2, "item": "Secure MLflow Registry", "value": 0.98}
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/echo")
def echo_message(payload: EchoMessage):
    return {"received_message": payload.message, "status": "processed_via_m2m"}