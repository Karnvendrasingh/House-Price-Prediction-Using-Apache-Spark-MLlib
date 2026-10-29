"""
Unit & Integration Tests: FastAPI Endpoints & Logic
INT315 - Cluster Computing Project
"""

import pytest
from backend.app.main import health_check
from backend.app.api.regions import list_regions, get_region
from backend.app.api.datasets import get_dataset_summary, get_dataset_preview, get_dataset_correlation
from backend.app.api.models import get_model_status
from backend.app.schemas.prediction import PredictionRequest
from backend.app.api.predict import predict_housing_value
from fastapi import HTTPException


def test_health_check_function():
    data = health_check()
    assert data["status"] == "HEALTHY"
    assert "subsystems" in data
    assert data["subsystems"]["dataset"]["cached"] is True
    assert data["subsystems"]["registered_regions_count"] >= 3


def test_list_regions_function():
    regions = list_regions()
    assert isinstance(regions, list)
    codes = [r["country_code"] for r in regions]
    assert "USA" in codes
    assert "GBR" in codes


def test_get_region_usa():
    usa = get_region("USA")
    assert usa["country_code"] == "USA"
    assert usa["support_status"] == "ACTIVE"


def test_get_dataset_summary_endpoint():
    summary = get_dataset_summary("usa_california")
    assert summary["total_records"] == 20640
    assert summary["target_column"] == "MedHouseVal"
    assert "statistics" in summary


def test_get_dataset_preview_endpoint():
    preview = get_dataset_preview(dataset_id="usa_california", page=1, page_size=10)
    assert preview["page"] == 1
    assert len(preview["records"]) == 10
    assert "EstimatedUSD" in preview["records"][0]


def test_get_dataset_correlation_endpoint():
    corr = get_dataset_correlation("usa_california")
    assert "correlation_with_target" in corr
    assert "MedInc" in corr["correlation_with_target"]
    assert corr["correlation_with_target"]["MedInc"] > 0.5


def test_model_status_endpoint():
    status = get_model_status("usa_california_lr")
    assert status.model_id == "usa_california_lr"
    assert status.status in ("TRAINED", "NOT_TRAINED", "UNINITIALIZED", "TRAINING")


def test_predict_unsupported_region_raises_400():
    req = PredictionRequest(region_code="GBR", features={"PropertyType": 1.0})
    with pytest.raises(HTTPException) as exc_info:
        predict_housing_value(req)
    assert exc_info.value.status_code == 400
    assert "Model not available" in exc_info.value.detail
