from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routes import router

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="A FastAPI service for BPO lead submissions with email notifications via Brevo SMTP",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this based on your needs in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(router, tags=["Leads"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to BPO Acceptor Lead Service",
        "docs": "/docs",
        "health": "/health",
        "submit_lead": "/bpo-acceptor-lead"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="localhost", port=8001, reload=settings.DEBUG)
