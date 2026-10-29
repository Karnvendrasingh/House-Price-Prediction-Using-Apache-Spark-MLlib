"""
Unit Tests: Multi-Country Registry & Validation Guardrails
INT315 - Cluster Computing Project
"""

import pytest
from backend.app.services.registry_service import registry_service


def test_list_regions():
    regions = registry_service.list_regions()
    assert len(regions) >= 3, "Expected at least USA, UK, and Germany in registry"
    country_codes = [r["country_code"] for r in regions]
    assert "USA" in country_codes
    assert "GBR" in country_codes
    assert "DEU" in country_codes


def test_usa_is_active():
    usa = registry_service.get_region("USA")
    assert usa is not None
    assert usa["support_status"] == "ACTIVE"
    assert len(usa["feature_schema"]) == 8


def test_unsupported_region_rejection():
    # Predicting on GBR (UK) must fail with clear explanation
    is_valid, msg, reg = registry_service.validate_prediction_request("GBR", {"PropertyType": "Detached"})
    assert not is_valid
    assert "Model not available" in msg
    assert "PLANNED_FUTURE" in msg


def test_missing_features_validation():
    # Incomplete USA features must fail validation
    is_valid, msg, reg = registry_service.validate_prediction_request("USA", {"MedInc": 8.0})
    assert not is_valid
    assert "Missing required features" in msg


def test_valid_features_validation():
    features = {
        "MedInc": 8.32,
        "HouseAge": 41.0,
        "AveRooms": 6.98,
        "AveBedrms": 1.02,
        "Population": 322.0,
        "AveOccup": 2.55,
        "Latitude": 37.88,
        "Longitude": -122.23
    }
    is_valid, msg, reg = registry_service.validate_prediction_request("USA", features)
    assert is_valid
    assert msg is None

