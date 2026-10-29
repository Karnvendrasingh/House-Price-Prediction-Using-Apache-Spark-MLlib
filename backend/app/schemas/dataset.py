"""
GlobalEstate AI - Dataset Schemas
INT315 - Cluster Computing Project
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel


class FeatureStat(BaseModel):
    count: int
    mean: float
    std: float
    min: float
    p25: float
    p50_median: float
    p75: float
    max: float
    missing: int


class DatasetSummaryResponse(BaseModel):
    dataset_name: str
    source: str
    reference_url: str
    region: str
    currency: str
    target_column: str
    target_unit: str
    total_records: int
    total_features: int
    feature_names: List[str]
    feature_descriptions: Dict[str, str]
    statistics: Dict[str, FeatureStat]
    correlation_with_target: Dict[str, float]
    full_correlation_matrix: Dict[str, Dict[str, float]]


class DatasetPreviewResponse(BaseModel):
    dataset_id: str
    page: int
    page_size: int
    total_records: int
    total_pages: int
    columns: List[str]
    records: List[Dict[str, Any]]


class DatasetCorrelationResponse(BaseModel):
    dataset_id: str
    target_column: str
    correlation_with_target: Dict[str, float]
    full_matrix: Dict[str, Dict[str, float]]

