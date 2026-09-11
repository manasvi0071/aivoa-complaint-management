from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routers import complaints, ai_agent

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AIVOA Complaint Management System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(complaints.router)
app.include_router(ai_agent.router)


@app.get("/")
def root():
    return {"status": "ok", "service": "AIVOA Complaint Management API"}