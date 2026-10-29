"""
GlobalEstate AI - Model Management Endpoints
INT315 - Cluster Computing Project
"""

import threading
from typing import Dict, Any, Optional
from fastapi import APIRouter, HTTPException, BackgroundTasks

from backend.app.schemas.model import (
    ModelTrainRequest,
    ModelStatusResponse,
    ModelMetricsResponse,
)
from backend.app.services.model_service import model_service

router = APIRouter(prefix="/models", tags=["Models"])

# Lock to prevent overlapping training runs
_training_lock = threading.Lock()
_training_state = {
    "is_training": False,
    "progress_message": "Idle",
    "last_error": None
}


def _run_training_job(dataset_id: str, train_ratio: float, seed: int):
    global _training_state
    try:
        _training_state["is_training"] = True
        _training_state["progress_message"] = "Initializing Spark MLlib Pipeline training..."
        _training_state["last_error"] = None
        model_service.train_model(dataset_id=dataset_id, train_ratio=train_ratio, seed=seed)
        _training_state["progress_message"] = "Training completed successfully."
    except Exception as e:
        _training_state["last_error"] = str(e)
        _training_state["progress_message"] = f"Training failed: {str(e)}"
    finally:
        _training_state["is_training"] = False


@router.get("/{model_id}/status", response_model=ModelStatusResponse)
def get_model_status(model_id: str):
    """Retrieves operational status and summary metrics for a given model."""
    meta = model_service.get_metadata(model_id)
    status_str = "TRAINING" if _training_state["is_training"] else meta.get("status", "UNINITIALIZED")
    
    return ModelStatusResponse(
        model_id=model_id,
        status=status_str,
        algorithm=meta.get("algorithm"),
        framework=meta.get("framework"),
        trained_at=meta.get("trained_at"),
        dataset_id=meta.get("dataset_id"),
        metrics=meta.get("metrics"),
        message=_training_state["progress_message"] if _training_state["is_training"] else meta.get("message")
    )


@router.get("/{model_id}/metrics", response_model=ModelMetricsResponse)
def get_model_metrics(model_id: str):
    """Returns genuine evaluation metrics (RMSE, MAE, R²), timings, weights, and residual scatter data."""
    if not model_service.is_model_trained(model_id):
        raise HTTPException(
            status_code=404,
            detail=f"Model '{model_id}' is not trained yet. Train it first via POST /api/models/{model_id}/train"
        )
    meta = model_service.get_metadata(model_id)
    return meta


@router.post("/{model_id}/train")
def trigger_training(
    model_id: str,
    payload: ModelTrainRequest,
    background_tasks: BackgroundTasks
):
    """Triggers asynchronous Spark MLlib model training in a non-blocking background thread."""
    global _training_state
    if _training_state["is_training"]:
        return {
            "status": "ALREADY_IN_PROGRESS",
            "message": "A model training job is currently running on the Spark engine."
        }

    background_tasks.add_task(
        _run_training_job,
        dataset_id=payload.dataset_id,
        train_ratio=payload.train_ratio,
        seed=payload.seed
    )

    return {
        "status": "QUEUED",
        "model_id": model_id,
        "message": "Model training task submitted to Spark engine background executor.",
        "parameters": payload.dict()
    }

