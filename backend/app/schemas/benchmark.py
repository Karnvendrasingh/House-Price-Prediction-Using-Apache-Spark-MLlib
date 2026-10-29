"""
GlobalEstate AI - Scalability Benchmark Schemas
INT315 - Cluster Computing Project
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class BenchmarkRunRequest(BaseModel):
    fractions: List[float] = Field(default=[0.25, 0.50, 1.00], description="Subsample fractions to test")
    partitions: int = Field(default=4, ge=1, le=32, description="Spark RDD partition count")
    synthetic_scaling: bool = Field(default=False, description="Whether to include synthetic data scaling")


class BenchmarkRunItem(BaseModel):
    fraction: float
    percentage_label: str
    row_count: int
    train_row_count: int
    test_row_count: int
    partition_count: int
    preprocessing_duration_s: float
    training_duration_s: float
    prediction_duration_s: float
    total_duration_s: float
    inference_throughput_rps: float
    scaling_linearity: Optional[float] = None


class BenchmarkResponse(BaseModel):
    benchmark_id: str
    timestamp: str
    execution_environment: Dict[str, Any]
    dataset: Dict[str, Any]
    runs: List[BenchmarkRunItem]
    total_suite_duration_s: float

