"""
GlobalEstate AI - Dataset Management Service
INT315 - Cluster Computing Project
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional

import pandas as pd

from backend.app.core.config import settings

logger = logging.getLogger("GlobalEstate.DatasetService")


class DatasetService:
    def __init__(self, data_dir: Path = settings.DATA_DIR):
        self.data_dir = data_dir
        self.csv_path = self.data_dir / "california_housing.csv"
        self.summary_path = self.data_dir / "dataset_summary.json"
        self._df_cache: Optional[pd.DataFrame] = None

    def get_dataframe(self) -> pd.DataFrame:
        """Loads and caches pandas DataFrame in memory for preview & stats."""
        if self._df_cache is None:
            if not self.csv_path.exists():
                logger.warning(f"CSV file not found at {self.csv_path}. Attempting acquisition...")
                from backend.scripts.fetch_dataset import acquire_dataset
                self._df_cache = acquire_dataset(self.data_dir)
            else:
                self._df_cache = pd.read_csv(self.csv_path)
        return self._df_cache

    def get_summary(self, dataset_id: str = "usa_california") -> Dict[str, Any]:
        """Returns the precomputed dataset metadata, schema, and statistics."""
        if self.summary_path.exists():
            with open(self.summary_path, "r", encoding="utf-8") as f:
                return json.load(f)

        # If summary file doesn't exist yet, compute and persist it
        df = self.get_dataframe()
        from backend.scripts.fetch_dataset import generate_dataset_summary
        return generate_dataset_summary(df, self.summary_path)

    def get_preview(
        self,
        dataset_id: str = "usa_california",
        page: int = 1,
        page_size: int = 20,
        sort_by: Optional[str] = None,
        sort_desc: bool = False
    ) -> Dict[str, Any]:
        """
        Returns paginated records with metadata for frontend table rendering.
        Prevents browser memory exhaustion by slicing only requested rows.
        """
        df = self.get_dataframe()
        total_records = len(df)
        total_pages = max(1, (total_records + page_size - 1) // page_size)

        current_page = max(1, min(page, total_pages))

        if sort_by and sort_by in df.columns:
            df_sorted = df.sort_values(by=sort_by, ascending=not sort_desc)
        else:
            df_sorted = df

        start_idx = (current_page - 1) * page_size
        end_idx = min(start_idx + page_size, total_records)

        records_slice = df_sorted.iloc[start_idx:end_idx].to_dict(orient="records")

        # Format records for display
        formatted_records = []
        for row in records_slice:
            formatted_row = {
                k: round(v, 4) if isinstance(v, float) else v
                for k, v in row.items()
            }
            # Add formatted USD equivalent for MedHouseVal
            if "MedHouseVal" in formatted_row:
                formatted_row["EstimatedUSD"] = int(round(formatted_row["MedHouseVal"] * settings.TARGET_SCALE_FACTOR))
            formatted_records.append(formatted_row)

        return {
            "dataset_id": dataset_id,
            "page": current_page,
            "page_size": page_size,
            "total_records": total_records,
            "total_pages": total_pages,
            "records": formatted_records,
            "columns": list(df.columns)
        }

    def get_correlation(self, dataset_id: str = "usa_california") -> Dict[str, Any]:
        """Returns the Pearson correlation coefficients matrix and target correlation."""
        summary = self.get_summary(dataset_id)
        return {
            "dataset_id": dataset_id,
            "target_column": summary["target_column"],
            "correlation_with_target": summary["correlation_with_target"],
            "full_matrix": summary["full_correlation_matrix"]
        }

    def load_as_spark_dataframe(self, spark, dataset_id: str = "usa_california"):
        """
        Loads the cached dataset directly into an Apache Spark DataFrame with explicit DoubleType schema.
        """
        from pyspark.sql.types import StructType, StructField, DoubleType

        if not self.csv_path.exists():
            self.get_dataframe()

        schema = StructType([
            StructField("MedInc", DoubleType(), False),
            StructField("HouseAge", DoubleType(), False),
            StructField("AveRooms", DoubleType(), False),
            StructField("AveBedrms", DoubleType(), False),
            StructField("Population", DoubleType(), False),
            StructField("AveOccup", DoubleType(), False),
            StructField("Latitude", DoubleType(), False),
            StructField("Longitude", DoubleType(), False),
            StructField("MedHouseVal", DoubleType(), False),
        ])

        logger.info(f"Loading Spark DataFrame from CSV: {self.csv_path}")
        spark_df = (
            spark.read
            .format("csv")
            .option("header", "true")
            .schema(schema)
            .load(str(self.csv_path.resolve()))
        )
        return spark_df


dataset_service = DatasetService()

