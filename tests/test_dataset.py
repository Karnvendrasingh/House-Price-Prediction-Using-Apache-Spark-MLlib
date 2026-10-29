"""
Unit Tests: Dataset Acquisition & Schema Validation
INT315 - Cluster Computing Project
"""

import pytest
import pandas as pd
from pathlib import Path
from backend.app.core.config import settings
from backend.app.services.dataset_service import dataset_service


def test_dataset_file_exists():
    assert dataset_service.csv_path.exists(), "California housing CSV must exist in data directory"


def test_dataset_row_and_column_counts():
    df = dataset_service.get_dataframe()
    assert len(df) == 20640, f"Expected 20,640 rows, got {len(df)}"
    assert len(df.columns) == 9, f"Expected 9 columns (8 features + 1 target), got {len(df.columns)}"


def test_expected_columns_present():
    df = dataset_service.get_dataframe()
    expected = [
        "MedInc", "HouseAge", "AveRooms", "AveBedrms",
        "Population", "AveOccup", "Latitude", "Longitude", "MedHouseVal"
    ]
    for col in expected:
        assert col in df.columns, f"Column '{col}' must be present in dataset"


def test_no_null_values():
    df = dataset_service.get_dataframe()
    total_nulls = df.isnull().sum().sum()
    assert total_nulls == 0, f"Expected 0 null values, found {total_nulls}"


def test_dataset_summary_statistics():
    summary = dataset_service.get_summary()
    assert summary["total_records"] == 20640
    assert summary["target_column"] == "MedHouseVal"
    assert "statistics" in summary
    stats = summary["statistics"]
    assert "MedInc" in stats
    assert stats["MedInc"]["mean"] > 0
    assert stats["MedHouseVal"]["mean"] > 0

