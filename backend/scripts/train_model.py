"""
GlobalEstate AI - Model Training Script
INT315 - Cluster Computing Project

Trains an Apache Spark MLlib LinearRegression model on the California Housing dataset.
Usage:
    python backend/scripts/train_model.py [--dataset usa_california] [--train-ratio 0.8] [--seed 42]
"""

import sys
import argparse
import logging
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from backend.app.services.dataset_service import dataset_service
from backend.app.services.model_service import model_service
from backend.app.services.spark_service import get_spark_session, stop_spark_session

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("GlobalEstate.TrainCLI")


def main():
    parser = argparse.ArgumentParser(description="Train Spark MLlib model for GlobalEstate AI")
    parser.add_argument(
        "--dataset", type=str, default="usa_california", help="Dataset identifier"
    )
    parser.add_argument(
        "--train-ratio", type=float, default=0.8, help="Train split ratio (default: 0.8)"
    )
    parser.add_argument(
        "--seed", type=int, default=42, help="Random split seed for reproducibility"
    )
    parser.add_argument(
        "--force", action="store_true", help="Force retraining even if model already exists"
    )
    args = parser.parse_args()

    print("\n" + "=" * 65)
    print("  GLOBALESTATE AI - APACHE SPARK MLLIB MODEL TRAINING")
    print("  INT315: Cluster Computing Final Project")
    print("=" * 65 + "\n")

    if not args.force and model_service.is_model_trained(model_service.default_model_id):
        meta = model_service.get_metadata()
        metrics = meta.get("metrics", {})
        print(f"[*] Found existing trained model '{model_service.default_model_id}'")
        print(f"    Trained at: {meta.get('trained_at')}")
        print(f"    RMSE:       {metrics.get('rmse')} (${metrics.get('rmse_usd'):,} USD)")
        print(f"    MAE:        {metrics.get('mae')} (${metrics.get('mae_usd'):,} USD)")
        print(f"    R²:         {metrics.get('r2')}")
        print("\nUse --force to retrain the model.\n")
        return

    logger.info("Verifying dataset availability...")
    dataset_service.get_dataframe()

    logger.info("Initializing SparkSession for training...")
    spark = get_spark_session()
    print(f"[*] Spark Engine: {spark.version} | Master: {spark.sparkContext.master}")

    try:
        metadata = model_service.train_model(
            dataset_id=args.dataset,
            train_ratio=args.train_ratio,
            seed=args.seed
        )

        metrics = metadata["metrics"]
        timing = metadata["timing_seconds"]
        split = metadata["train_test_split"]
        params = metadata["model_parameters"]

        print("\n" + "=" * 65)
        print("  MODEL TRAINING COMPLETED SUCCESSFULLY")
        print("=" * 65)
        print(f"  Framework:         {metadata['framework']}")
        print(f"  Algorithm:         {metadata['algorithm']}")
        print(f"  Total Records:     {split['total_records']:,}")
        print(f"  Train Records:     {split['train_samples']:,} ({int(split['train_ratio']*100)}%)")
        print(f"  Test Records:      {split['test_samples']:,} ({int(split['test_ratio']*100)}%)")
        print("-" * 65)
        print("  EVALUATION METRICS (ON HELD-OUT TEST DATA):")
        print(f"  RMSE:              {metrics['rmse']:.4f} (~${metrics['rmse_usd']:,} USD)")
        print(f"  MAE:               {metrics['mae']:.4f} (~${metrics['mae_usd']:,} USD)")
        print(f"  R² Score:          {metrics['r2']:.4f}")
        print("-" * 65)
        print("  STAGE TIMINGS:")
        print(f"  Data Load/Count:   {timing['data_load_duration']:.2f} s")
        print(f"  Pipeline Fit:      {timing['training_duration']:.2f} s")
        print(f"  Test Evaluation:   {timing['eval_duration']:.2f} s")
        print(f"  Total Duration:    {timing['total_duration']:.2f} s")
        print("-" * 65)
        print("  FEATURE COEFFICIENTS:")
        for feat, weight in params["feature_coefficients"].items():
            print(f"    {feat:<12} : {weight:+.6f}")
        print(f"    Intercept    : {params['intercept']:+.6f}")
        print("=" * 65 + "\n")

    finally:
        stop_spark_session()


if __name__ == "__main__":
    main()

