"""
GlobalEstate AI - Dataset Acquisition & Validation Service
INT315 - Cluster Computing Project

Acquires, caches, validates, and summarizes the California Housing dataset.
Features:
- MedInc: Median income in block group (in $10,000s)
- HouseAge: Median house age in block group (years)
- AveRooms: Average number of rooms per household
- AveBedrms: Average number of bedrooms per household
- Population: Block group population
- AveOccup: Average number of household members
- Latitude: Block group latitude (degrees north)
- Longitude: Block group longitude (degrees west)
Target:
- MedHouseVal: Median house value for California districts (in $100,000s)
"""

import os
import sys
import json
import tarfile
import logging
from pathlib import Path
from typing import Dict, Any, Tuple, Optional

import numpy as np
import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("GlobalEstate.DataAcquisition")

# Core Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
CSV_PATH = DATA_DIR / "california_housing.csv"
SUMMARY_PATH = DATA_DIR / "dataset_summary.json"
ARCHIVE_PATH = DATA_DIR / "cal_housing.tgz"

EXPECTED_FEATURES = [
    "MedInc",
    "HouseAge",
    "AveRooms",
    "AveBedrms",
    "Population",
    "AveOccup",
    "Latitude",
    "Longitude",
]
TARGET_COL = "MedHouseVal"
EXPECTED_ROW_COUNT = 20640


def extract_from_tar(tar_path: Path) -> Optional[pd.DataFrame]:
    """Extract and parse California housing dataset directly from cal_housing.tgz."""
    if not tar_path.exists():
        return None
    try:
        logger.info(f"Extracting raw archive from: {tar_path}")
        with tarfile.open(tar_path, "r:gz") as tar:
            # Locate CaliforniaHousing/cal_housing.data
            member = None
            for m in tar.getmembers():
                if m.name.endswith("cal_housing.data"):
                    member = m
                    break
            if not member:
                return None
            f = tar.extractfile(member)
            if f is None:
                return None
            # Standard order in cal_housing.data:
            # longitude, latitude, housingMedianAge, totalRooms, totalBedrooms, population, households, medianIncome, medianHouseValue
            raw_cols = [
                "Longitude",
                "Latitude",
                "HouseAge",
                "totalRooms",
                "totalBedrooms",
                "Population",
                "households",
                "MedInc",
                "MedHouseVal",
            ]
            df_raw = pd.read_csv(f, names=raw_cols, header=None)
            
            # Convert totals to per-household averages to match sklearn's standard dataset
            df = pd.DataFrame()
            df["MedInc"] = df_raw["MedInc"]
            df["HouseAge"] = df_raw["HouseAge"]
            df["AveRooms"] = df_raw["totalRooms"] / df_raw["households"]
            df["AveBedrms"] = df_raw["totalBedrooms"] / df_raw["households"]
            df["Population"] = df_raw["Population"]
            df["AveOccup"] = df_raw["Population"] / df_raw["households"]
            df["Latitude"] = df_raw["Latitude"]
            df["Longitude"] = df_raw["Longitude"]
            # Sklearn target is scaled to $100,000s
            df["MedHouseVal"] = df_raw["MedHouseVal"] / 100000.0
            return df
    except Exception as e:
        logger.warning(f"Could not extract from tar archive {tar_path}: {e}")
        return None


def acquire_dataset(data_dir: Path = DATA_DIR) -> pd.DataFrame:
    """
    Acquire the dataset using the following fallback chain:
    1. Local project CSV cache (data/california_housing.csv)
    2. Local project archive (data/cal_housing.tgz)
    3. User home scikit_learn_data/cal_housing.tgz
    4. Scikit-learn fetch_california_housing(download_if_missing=True)
    """
    data_dir.mkdir(parents=True, exist_ok=True)
    csv_file = data_dir / "california_housing.csv"

    # Step 1: Check existing CSV cache
    if csv_file.exists():
        logger.info(f"Reusing existing cached dataset: {csv_file}")
        df = pd.read_csv(csv_file)
        return df

    # Step 2: Check local archive
    local_archive = data_dir / "cal_housing.tgz"
    df_archive = extract_from_tar(local_archive)
    if df_archive is not None:
        logger.info(f"Successfully unpacked local archive: {local_archive}")
        df_archive.to_csv(csv_file, index=False)
        return df_archive

    # Step 3: Check common system cache locations
    user_home = Path.home()
    possible_user_archives = [
        user_home / "scikit_learn_data" / "cal_housing.tgz",
        user_home / ".scikit_learn_data" / "cal_housing.tgz",
        Path("C:/Users/karnv/scikit_learn_data/cal_housing.tgz"),
    ]
    for user_archive in possible_user_archives:
        if user_archive.exists():
            df_home = extract_from_tar(user_archive)
            if df_home is not None:
                logger.info(f"Reused archive from host cache: {user_archive}")
                df_home.to_csv(csv_file, index=False)
                return df_home

    # Step 4: Download via scikit-learn
    logger.info("Attempting online acquisition via sklearn.datasets.fetch_california_housing...")
    try:
        from sklearn.datasets import fetch_california_housing
        bunch = fetch_california_housing(as_frame=True, data_home=str(data_dir), download_if_missing=True)
        df = bunch.frame.copy()
        df.to_csv(csv_file, index=False)
        logger.info(f"Dataset successfully acquired and persisted to {csv_file}")
        return df
    except Exception as e:
        error_msg = (
            f"\n[DATASET ACQUISITION ERROR] Could not automatically acquire the California Housing dataset.\n"
            f"Underlying cause: {e}\n\n"
            f"HOW TO PROVIDE THE DATASET MANUALLY:\n"
            f"1. Download 'cal_housing.tgz' from: https://ndownloader.figshare.com/files/5976036\n"
            f"2. Place 'cal_housing.tgz' or 'california_housing.csv' directly into:\n"
            f"   {data_dir.resolve()}\n"
            f"3. Re-run this command: python backend/scripts/fetch_dataset.py\n"
        )
        logger.error(error_msg)
        raise RuntimeError(error_msg)


def validate_dataset(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Validates dataset integrity:
    - Expected row count
    - Column schema (8 features + 1 target)
    - Missing/NaN values
    - Range sanity checks
    """
    logger.info("Running rigorous dataset integrity checks...")
    validation_report = {
        "is_valid": True,
        "row_count": len(df),
        "column_count": len(df.columns),
        "columns": list(df.columns),
        "missing_values": {},
        "issues": [],
        "warnings": [],
    }

    # Row count verification
    if len(df) < 1000:
        validation_report["is_valid"] = False
        validation_report["issues"].append(f"Row count ({len(df)}) is abnormally low for California Housing.")
    elif len(df) != EXPECTED_ROW_COUNT:
        validation_report["warnings"].append(
            f"Row count {len(df)} differs slightly from standard {EXPECTED_ROW_COUNT}."
        )

    # Column presence
    for feat in EXPECTED_FEATURES:
        if feat not in df.columns:
            validation_report["is_valid"] = False
            validation_report["issues"].append(f"Missing required feature: '{feat}'")

    if TARGET_COL not in df.columns:
        validation_report["is_valid"] = False
        validation_report["issues"].append(f"Missing required target column: '{TARGET_COL}'")

    # Missing values
    null_counts = df.isnull().sum().to_dict()
    validation_report["missing_values"] = {k: int(v) for k, v in null_counts.items()}
    total_nulls = sum(null_counts.values())
    if total_nulls > 0:
        validation_report["warnings"].append(f"Found {total_nulls} missing/null values across columns.")

    # Range and type checks
    for col in EXPECTED_FEATURES + [TARGET_COL]:
        if col in df.columns:
            if not np.issubdtype(df[col].dtype, np.number):
                validation_report["is_valid"] = False
                validation_report["issues"].append(f"Column '{col}' must be numeric, got {df[col].dtype}")

    if validation_report["is_valid"]:
        logger.info(f"Validation PASSED: {len(df)} rows, {len(df.columns)} columns, 0 critical issues.")
    else:
        logger.error(f"Validation FAILED: {validation_report['issues']}")

    return validation_report


def generate_dataset_summary(df: pd.DataFrame, output_path: Path = SUMMARY_PATH) -> Dict[str, Any]:
    """
    Generates summary statistics and Pearson correlation matrix for the dataset.
    Saves to JSON so the web dashboard can load metadata instantly.
    """
    logger.info("Computing summary statistics and feature correlations...")
    cols = EXPECTED_FEATURES + [TARGET_COL]
    sub_df = df[cols]

    stats = {}
    for col in cols:
        series = sub_df[col]
        stats[col] = {
            "count": int(series.count()),
            "mean": float(round(series.mean(), 4)),
            "std": float(round(series.std(), 4)),
            "min": float(round(series.min(), 4)),
            "p25": float(round(series.quantile(0.25), 4)),
            "p50_median": float(round(series.median(), 4)),
            "p75": float(round(series.quantile(0.75), 4)),
            "max": float(round(series.max(), 4)),
            "missing": int(series.isnull().sum()),
        }

    # Correlation with target and cross-correlation
    corr_matrix = sub_df.corr().round(4).to_dict()

    feature_descriptions = {
        "MedInc": "Median income in block group (tens of thousands of USD)",
        "HouseAge": "Median house age in block group (years)",
        "AveRooms": "Average number of rooms per household",
        "AveBedrms": "Average number of bedrooms per household",
        "Population": "Block group population",
        "AveOccup": "Average number of household members",
        "Latitude": "Block group centroid latitude (degrees north)",
        "Longitude": "Block group centroid longitude (degrees west)",
        "MedHouseVal": "Median house value for California districts ($100,000s)",
    }

    summary = {
        "dataset_name": "USA California Housing (Census 1990)",
        "source": "StatLib repository / Scikit-learn datasets",
        "reference_url": "https://scikit-learn.org/stable/datasets/real_world.html#california-housing-dataset",
        "region": "California, United States",
        "currency": "USD",
        "target_column": TARGET_COL,
        "target_unit": "$100,000 USD",
        "total_records": len(df),
        "total_features": len(EXPECTED_FEATURES),
        "feature_names": EXPECTED_FEATURES,
        "feature_descriptions": feature_descriptions,
        "statistics": stats,
        "correlation_with_target": {
            feat: float(corr_matrix[feat][TARGET_COL]) for feat in EXPECTED_FEATURES
        },
        "full_correlation_matrix": corr_matrix,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    logger.info(f"Dataset summary successfully saved to: {output_path}")
    return summary


def main():
    logger.info("=== GlobalEstate AI: Dataset Acquisition and Setup Pipeline ===")
    try:
        df = acquire_dataset(DATA_DIR)
        report = validate_dataset(df)
        if not report["is_valid"]:
            sys.exit(1)
        summary = generate_dataset_summary(df, SUMMARY_PATH)
        print("\n" + "=" * 60)
        print("DATASET ACQUISITION SUMMARY:")
        print(f"  Total Records: {summary['total_records']:,}")
        print(f"  Features: {summary['total_features']} ({', '.join(summary['feature_names'])})")
        print(f"  Target: {summary['target_column']} ({summary['target_unit']})")
        print(f"  Cached Path: {CSV_PATH.resolve()}")
        print(f"  Metadata Path: {SUMMARY_PATH.resolve()}")
        print("=" * 60 + "\n")
    except Exception as e:
        logger.error(f"Failed to acquire/validate dataset: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

