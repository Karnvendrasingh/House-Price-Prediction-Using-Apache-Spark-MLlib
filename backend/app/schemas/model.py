"""
GlobalEstate AI - Model Management Schemas
INT315 - Cluster Computing Project
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class ModelTrainRequest(BaseModel):
    dataset_id: str = Field(default="usa_california", description="Dataset identifier to train on")
    train_ratio: float = Field(default=0.8, ge=0.5, le=0.95, description="Train set ratio")
    seed: int = Field(default=42, description="Random seed for train/test splitting")


class ModelMetrics(BaseModel):
    rmse: Optional[float] = None
    mae: Optional[float] = None
    r2: Optional[float] = None
    rmse_usd: Optional[int] = None
    mae_usd: Optional[int] = None


class ModelStatusResponse(BaseModel):
    model_id: str
    status: str
    algorithm: Optional[str] = None
    framework: Optional[str] = None
    trained_at: Optional[str] = None
    dataset_id: Optional[str] = None
    metrics: Optional[ModelMetrics] = None
    message: Optional[str] = None


class ResidualPoint(BaseModel):
    actual: float
    predicted: float
    actual_usd: int
    predicted_usd: int
    residual: float


class ModelMetricsResponse(BaseModel):
    model_id: str
    status: str
    algorithm: str
    framework: str
    dataset_id: str
    trained_at: str
    dataset_provenance: str
    train_test_split: Dict[str, Any]
    metrics: ModelMetrics
    timing_seconds: Dict[str, float]
    model_parameters: Dict[str, Any]
    residuals_sample: List[ResidualPoint]
    partition_count: int
    execution_master: str

