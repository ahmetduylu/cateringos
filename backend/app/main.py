from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.database import Base, engine
from app.routers import auth, leads, reports
from app.routers.apify import router as apify_router
from app.models import user, lead, lead_log

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up...")
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created/verified")
    except Exception as e:
        logger.error(f"Database connection error: {e}")
    yield
    logger.info("Shutting down...")


app = FastAPI(
    title="LocalCateringOS API",
    description="Yerel Catering Firması için CRM & Lead Yönetim Sistemi",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(leads.router)
app.include_router(reports.router)
app.include_router(apify_router)


@app.get("/", tags=["health"])
def root():
    return {"status": "ok", "service": "LocalCateringOS API", "version": "1.0.0"}


@app.get("/health", tags=["health"])
def health():
    return {"status": "healthy"}
