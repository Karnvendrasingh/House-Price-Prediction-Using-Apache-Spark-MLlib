"""
GlobalEstate AI - Scalability Benchmark Service
INT315 - Cluster Computing Project
"""

import time
import json
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional

from backend.app.core.config import settings
from backend.app.services.spark_service import get_spark_session

logger = logging.getLogger("GlobalEstate.BenchmarkService")


class BenchmarkService:
    def __init__(self, benchmarks_dir: Path = settings.BENCHMARKS_DIR):
        self.benchmarks_dir = benchmarks_dir
        self.history_file = self.benchmarks_dir / "benchmark_results.json"
        self.benchmarks_dir.mkdir(parents=True, exist_ok=True)

    def get_benchmark_history(self) -> List[Dict[str, Any]]:
        """Reads historical benchmark runs from disk."""
        if not self.history_file.exists():
            return []
        try:
            with open(self.history_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Error reading benchmark history: {e}")
            return []

    def save_benchmark_result(self, result: Dict[str, Any]):
        """Appends a new benchmark execution record to history."""
        history = self.get_benchmark_history()
        history.insert(0, result)  # Most recent first
        # Keep up to 20 runs
        history = history[:20]
        with open(self.history_file, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2)

    def run_benchmark_suite(
        self,
        fractions: List[float] = [0.25, 0.50, 1.00],
        partitions: int = 4,
        synthetic_scaling: bool = False
    ) -> Dict[str, Any]:
        """
        Executes a controlled Spark workload scalability experiment across data sizes.
        For each fraction (e.g. 25%, 50%, 100%):
        - Measures Preprocessing (VectorAssembler + StandardScaler fit/transform)
        - Measures Training (LinearRegression fit)
        - Measures Batch Inference (transform on test partition)
        - Records exact row count, partition count, and memory allocation
        """
        from pyspark.ml import Pipeline
        from pyspark.ml.feature import VectorAssembler, StandardScaler
        from pyspark.ml.regression import LinearRegression
        from backend.app.services.dataset_service import dataset_service

        suite_start = time.time()
        spark = get_spark_session(shuffle_partitions=partitions)

        base_df = dataset_service.load_as_spark_dataframe(spark)
        base_df = base_df.repartition(partitions).cache()
        full_row_count = base_df.count()

        feature_cols = [
            "MedInc", "HouseAge", "AveRooms", "AveBedrms",
            "Population", "AveOccup", "Latitude", "Longitude"
        ]
        target_col = "MedHouseVal"

        runs = []

        for frac in fractions:
            logger.info(f"Running scalability benchmark at fraction={frac:.2f} ({int(frac*full_row_count):,} rows)...")
            
            # Subsample
            if frac < 1.0:
                sub_df = base_df.sample(withReplacement=False, fraction=frac, seed=42).cache()
            else:
                sub_df = base_df

            row_count = sub_df.count()

            # 1. Measure Preprocessing Duration
            t0 = time.time()
            assembler = VectorAssembler(inputCols=feature_cols, outputCol="raw_features")
            scaler = StandardScaler(inputCol="raw_features", outputCol="features", withMean=True, withStd=True)
            prep_pipeline = Pipeline(stages=[assembler, scaler])
            prep_model = prep_pipeline.fit(sub_df)
            prepped_df = prep_model.transform(sub_df).cache()
            # Action to force lazy evaluation execution
            _ = prepped_df.count()
            prep_duration = time.time() - t0

            # 2. Measure MLlib Training Duration
            t1 = time.time()
            train_sub, test_sub = prepped_df.randomSplit([0.8, 0.2], seed=42)
            lr = LinearRegression(featuresCol="features", labelCol=target_col, maxIter=50, regParam=0.0)
            lr_model = lr.fit(train_sub)
            train_duration = time.time() - t1

            # 3. Measure Prediction Throughput
            t2 = time.time()
            preds_df = lr_model.transform(test_sub).cache()
            test_row_count = preds_df.count()
            predict_duration = time.time() - t2

            total_run_duration = prep_duration + train_duration + predict_duration
            throughput_records_per_sec = test_row_count / max(0.001, predict_duration)

            runs.append({
                "fraction": frac,
                "percentage_label": f"{int(frac*100)}%",
                "row_count": row_count,
                "train_row_count": train_sub.count(),
                "test_row_count": test_row_count,
                "partition_count": sub_df.rdd.getNumPartitions(),
                "preprocessing_duration_s": round(prep_duration, 4),
                "training_duration_s": round(train_duration, 4),
                "prediction_duration_s": round(predict_duration, 4),
                "total_duration_s": round(total_run_duration, 4),
                "inference_throughput_rps": round(throughput_records_per_sec, 1)
            })

        total_suite_time = time.time() - suite_start

        # Compute speedup / scaling efficiency relative to the 25% run
        base_run = runs[0] if runs else None
        if base_run and base_run["total_duration_s"] > 0:
            for r in runs:
                expected_scaling = r["row_count"] / base_run["row_count"]
                actual_ratio = r["total_duration_s"] / base_run["total_duration_s"]
                r["scaling_linearity"] = round(actual_ratio / expected_scaling, 3)

        result = {
            "benchmark_id": f"bench_{int(time.time())}",
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "execution_environment": {
                "master": spark.sparkContext.master,
                "spark_version": spark.version,
                "driver_memory": settings.SPARK_DRIVER_MEMORY,
                "configured_partitions": partitions,
                "cluster_type": "Single-Node Local[*] Simulated Cluster (INT315 Laboratory Environment)",
                "hardware_note": "Local CPU cores simulated execution. Real multi-node cluster scaling requires physical Spark worker daemons."
            },
            "dataset": {
                "name": "California Housing (StatLib)",
                "is_synthetic": synthetic_scaling,
                "total_source_records": full_row_count
            },
            "runs": runs,
            "total_suite_duration_s": round(total_suite_time, 3)
        }

        self.save_benchmark_result(result)
        return result


benchmark_service = BenchmarkService()

