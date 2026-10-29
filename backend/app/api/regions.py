"""
GlobalEstate AI - Regions & Multi-Country Registry Endpoints
INT315 - Cluster Computing Project
"""

from typing import List, Dict, Any
from fastapi import APIRouter, HTTPException

from backend.app.services.registry_service import registry_service

router = APIRouter(prefix="/regions", tags=["Regions & Registry"])


@router.get("", response_model=List[Dict[str, Any]])
def list_regions():
    """Returns list of registered global regions and datasets."""
    return registry_service.list_regions()


@router.get("/{country_code}", response_model=Dict[str, Any])
def get_region(country_code: str):
    """Retrieves specific region configuration, currency, feature schema, and model status."""
    region = registry_service.get_region(country_code)
    if not region:
        raise HTTPException(
            status_code=404,
            detail=f"Region '{country_code}' not found in GlobalEstate registry."
        )
    return region

