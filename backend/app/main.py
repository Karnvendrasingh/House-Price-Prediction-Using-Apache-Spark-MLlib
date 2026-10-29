"""
GlobalEstate AI - FastAPI Application Entry Point
INT315 - Cluster Computing Project
"""

import time
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.app.core.config import settings
from backend.app.services.spark_service import get_spark_status
from backend.app.services.dataset_service import dataset_service
from backend.app.services.model_service import model_service
from backend.app.services.registry_service import registry_service

# Routers
from backend.app.api.regions import router as regions_router
from backend.app.api.datasets import router as datasets_router
from backend.app.api.models import router as models_router
from backend.app.api.predict import router as predict_router
from backend.app.api.benchmarks import router as benchmarks_router

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("GlobalEstate.API")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Configuration for Next.js Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Sub-Routers under /api
app.include_router(regions_router, prefix=settings.API_PREFIX)
app.include_router(datasets_router, prefix=settings.API_PREFIX)
app.include_router(models_router, prefix=settings.API_PREFIX)
app.include_router(predict_router, prefix=settings.API_PREFIX)
app.include_router(benchmarks_router, prefix=settings.API_PREFIX)


@app.get(f"{settings.API_PREFIX}/health")
def health_check():
    """
    System health, runtime environment, Spark cluster simulation status,
    dataset availability, and model status.
    """
    dataset_ready = dataset_service.csv_path.exists()
    model_ready = model_service.is_model_trained()
    spark_info = get_spark_status()

    return {
        "status": "HEALTHY",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "subsystems": {
            "dataset": {
                "id": settings.DEFAULT_DATASET_ID,
                "cached": dataset_ready,
                "path": str(dataset_service.csv_path.resolve()) if dataset_ready else None
            },
            "model": {
                "id": settings.DEFAULT_MODEL_ID,
                "trained": model_ready,
                "path": str(model_service.model_path.resolve()) if model_ready else None
            },
            "spark_runtime": spark_info,
            "registered_regions_count": len(registry_service.list_regions())
        }
    }


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception processing {request.url.path}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "InternalServerError",
            "message": str(exc),
            "path": request.url.path
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)

