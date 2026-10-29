"""
GlobalEstate AI - Dataset Exploration Endpoints
INT315 - Cluster Computing Project
"""

from typing import Optional
from fastapi import APIRouter, HTTPException, Query

from backend.app.schemas.dataset import (
    DatasetSummaryResponse,
    DatasetPreviewResponse,
    DatasetCorrelationResponse,
)
from backend.app.services.dataset_service import dataset_service

router = APIRouter(prefix="/datasets", tags=["Datasets"])


@router.get("/{dataset_id}/summary", response_model=DatasetSummaryResponse)
def get_dataset_summary(dataset_id: str):
    """Retrieves dataset summary statistics, column descriptions, and distributions."""
    try:
        return dataset_service.get_summary(dataset_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch dataset summary: {str(e)}")


@router.get("/{dataset_id}/preview", response_model=DatasetPreviewResponse)
def get_dataset_preview(
    dataset_id: str,
    page: int = Query(default=1, ge=1, description="Page number"),
    page_size: int = Query(default=20, ge=1, le=100, description="Records per page"),
    sort_by: Optional[str] = Query(default=None, description="Column name to sort by"),
    sort_desc: bool = Query(default=False, description="Sort descending")
):
    """Returns paginated dataset slice for client-side table explorer."""
    try:
        return dataset_service.get_preview(
            dataset_id=dataset_id,
            page=page,
            page_size=page_size,
            sort_by=sort_by,
            sort_desc=sort_desc
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch dataset preview: {str(e)}")


@router.get("/{dataset_id}/correlation", response_model=DatasetCorrelationResponse)
def get_dataset_correlation(dataset_id: str):
    """Returns Pearson correlation matrix for numerical features and the target variable."""
    try:
        return dataset_service.get_correlation(dataset_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch correlation matrix: {str(e)}")

