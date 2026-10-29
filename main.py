"""
GlobalEstate AI - Terminal Interface & CLI Entrypoint
INT315 - Cluster Computing Project

Interactive terminal menu and direct command runner for Apache Spark MLlib:
- Model Training
- Property Price Prediction
- Model Evaluation & Residual Analysis
- Dataset Exploration
- Scalability Benchmarking
- Cluster & Model Diagnostics
"""

import sys
import os
import argparse
from pathlib import Path

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

from backend.app.core.config import settings
from backend.app.services.dataset_service import dataset_service
from backend.app.services.model_service import model_service
from backend.app.services.benchmark_service import benchmark_service
from backend.app.services.registry_service import registry_service
from backend.app.services.spark_service import get_spark_status, stop_spark_session


BANNER = r"""
  ╔═══════════════════════════════════════════════════════════════════════╗
  ║                     G L O B A L E S T A T E   A I                     ║
  ║      Scalable Real Estate Price Prediction Platform (Spark MLlib)     ║
  ║                   INT315 - Cluster Computing Project                  ║
  ╚═══════════════════════════════════════════════════════════════════════╝
"""


def prompt_float(prompt_text: str, default_val: float, min_val: float = None, max_val: float = None) -> float:
    """Prompt user for a valid float with range checking and sensible defaults."""
    while True:
        try:
            raw = input(f"  {prompt_text} [Default: {default_val}]: ").strip()
            if not raw:
                return default_val
            val = float(raw)
            if min_val is not None and val < min_val:
                print(f"  [!] Value must be >= {min_val}. Try again.")
                continue
            if max_val is not None and val > max_val:
                print(f"  [!] Value must be <= {max_val}. Try again.")
                continue
            return val
        except ValueError:
            print("  [!] Invalid number. Please enter a numerical value.")


def cmd_train():
    print("\n--- [1] TRAIN APACHE SPARK MLLIB MODEL ---")
    if model_service.is_model_trained():
        meta = model_service.get_metadata()
        metrics = meta.get("metrics", {})
        print(f"[*] An active trained model already exists on disk (trained at {meta.get('trained_at')}).")
        print(f"    Current RMSE: {metrics.get('rmse')} (${metrics.get('rmse_usd'):,} USD) | R²: {metrics.get('r2')}")
        choice = input("    Do you want to retrain the model? (y/N): ").strip().lower()
        if choice not in ("y", "yes"):
            print("    Retraining cancelled. Reusing existing model.\n")
            return

    train_ratio = prompt_float("Enter training split ratio (0.5 to 0.95)", default_val=0.8, min_val=0.5, max_val=0.95)
    seed = int(prompt_float("Enter random seed for reproducibility", default_val=42, min_val=0))

    print("\n[*] Initializing Apache Spark MLlib Pipeline...")
    try:
        metadata = model_service.train_model(
            dataset_id=settings.DEFAULT_DATASET_ID,
            train_ratio=train_ratio,
            seed=seed
        )
        metrics = metadata["metrics"]
        print("\n[+] MODEL TRAINING SUCCEEDED:")
        print(f"    Algorithm:       {metadata['algorithm']}")
        print(f"    Train Samples:   {metadata['train_test_split']['train_samples']:,}")
        print(f"    Test Samples:    {metadata['train_test_split']['test_samples']:,}")
        print(f"    Test RMSE:       {metrics['rmse']:.4f} (~${metrics['rmse_usd']:,} USD)")
        print(f"    Test MAE:        {metrics['mae']:.4f} (~${metrics['mae_usd']:,} USD)")
        print(f"    Test R² Score:   {metrics['r2']:.4f}")
        print(f"    Total Duration:  {metadata['timing_seconds']['total_duration']:.2f} s")
        print(f"    Saved Artifact:  {model_service.model_path.resolve()}\n")
    except Exception as e:
        print(f"\n[!] Training failed: {e}\n")


def cmd_predict():
    print("\n--- [2] PREDICT HOUSING VALUE (SPARK MLLIB INFERENCE) ---")
    if not model_service.is_model_trained():
        print("[!] No trained model found on disk.")
        print("    Please train the model first using Option 1 or: python backend/scripts/train_model.py\n")
        return

    print("  Enter California Census Block group attributes for valuation:")
    print("  (Press Enter to accept realistic California defaults)\n")

    med_inc = prompt_float("1. Median Income (tens of thousands USD, e.g. 8.325 = $83,250/yr)", 8.325, min_val=0.1, max_val=25.0)
    house_age = prompt_float("2. Median House Age (years)", 28.0, min_val=1.0, max_val=100.0)
    ave_rooms = prompt_float("3. Average Rooms per household", 6.98, min_val=0.5, max_val=50.0)
    ave_bedrms = prompt_float("4. Average Bedrooms per household", 1.02, min_val=0.2, max_val=20.0)
    population = prompt_float("5. Block Group Population", 1425.0, min_val=1.0, max_val=40000.0)
    ave_occup = prompt_float("6. Average Household Occupants", 2.55, min_val=0.5, max_val=200.0)
    latitude = prompt_float("7. Latitude (degrees north, California: 32.5 to 42.0)", 37.88, min_val=32.0, max_val=43.0)
    longitude = prompt_float("8. Longitude (degrees west, California: -124.5 to -114.0)", -122.23, min_val=-125.0, max_val=-113.0)

    features = {
        "MedInc": med_inc,
        "HouseAge": house_age,
        "AveRooms": ave_rooms,
        "AveBedrms": ave_bedrms,
        "Population": population,
        "AveOccup": ave_occup,
        "Latitude": latitude,
        "Longitude": longitude
    }

    print("\n[*] Assembling feature vector and executing Spark MLlib Pipeline inference...")
    try:
        result = model_service.predict(features)
        print("\n" + "=" * 65)
        print("  VALUATION RESULT:")
        print("=" * 65)
        print(f"  Target Value (MedHouseVal) : {result['predicted_target_value']:.4f} ($100,000 USD)")
        print(f"  ESTIMATED HOUSING VALUE    : {result['formatted_usd']} USD")
        print(f"  95% Confidence Interval    : {result['confidence_interval_95_usd']['formatted']}")
        print(f"  Inference Latency          : {result['execution_metadata']['inference_latency_ms']:.2f} ms")
        print(f"  Total Request Latency      : {result['execution_metadata']['total_request_latency_ms']:.2f} ms")
        print(f"  Spark Execution Master     : {result['execution_metadata']['spark_master']}")
        print("-" * 65)
        print(f"  Note: {result['disclaimer']}")
        print("=" * 65 + "\n")
    except Exception as e:
        print(f"\n[!] Prediction failed: {e}\n")


def cmd_evaluate():
    print("\n--- [3] EVALUATE MODEL & TEST METRICS ---")
    if not model_service.is_model_trained():
        print("[!] No trained model found. Train the model first.\n")
        return

    meta = model_service.get_metadata()
    metrics = meta.get("metrics", {})
    timing = meta.get("timing_seconds", {})
    split = meta.get("train_test_split", {})
    params = meta.get("model_parameters", {})

    print("\n" + "=" * 65)
    print("  EVALUATION SUMMARY:")
    print("=" * 65)
    print(f"  Model ID:            {meta.get('model_id')}")
    print(f"  Algorithm:           {meta.get('algorithm')}")
    print(f"  Framework:           {meta.get('framework')}")
    print(f"  Trained Timestamp:   {meta.get('trained_at')}")
    print(f"  Total Dataset Rows:  {split.get('total_records', 0):,}")
    print(f"  Train / Test Split:  {split.get('train_samples', 0):,} / {split.get('test_samples', 0):,}")
    print("-" * 65)
    print("  GENUINE TEST METRICS:")
    print(f"  Root Mean Squared Error (RMSE) : {metrics.get('rmse')} (~${metrics.get('rmse_usd', 0):,} USD)")
    print(f"  Mean Absolute Error (MAE)      : {metrics.get('mae')} (~${metrics.get('mae_usd', 0):,} USD)")
    print(f"  Coefficient of Determination R²: {metrics.get('r2')}")
    print("-" * 65)
    print("  FEATURE COEFFICIENTS:")
    for feat, coef in params.get("feature_coefficients", {}).items():
        print(f"    {feat:<12} : {coef:+.6f}")
    print(f"    Intercept    : {params.get('intercept', 0.0):+.6f}")
    print("-" * 65)
    print(f"  Training Wall-Clock Duration   : {timing.get('training_duration', 0.0):.2f} s")
    print(f"  Test Evaluation Duration       : {timing.get('eval_duration', 0.0):.2f} s")
    print("=" * 65 + "\n")


def cmd_explore():
    print("\n--- [4] EXPLORE CALIFORNIA HOUSING DATASET ---")
    summary = dataset_service.get_summary()

    print("\n" + "=" * 65)
    print(f"  DATASET: {summary.get('dataset_name')}")
    print(f"  Source:  {summary.get('source')}")
    print(f"  Records: {summary.get('total_records'):,} | Features: {summary.get('total_features')}")
    print("=" * 65)
    print(f"{'Feature':<12} {'Mean':<10} {'Std':<10} {'Min':<10} {'Median':<10} {'Max':<10}")
    print("-" * 65)
    for feat, s in summary.get("statistics", {}).items():
        print(f"{feat:<12} {s['mean']:<10.2f} {s['std']:<10.2f} {s['min']:<10.2f} {s['p50_median']:<10.2f} {s['max']:<10.2f}")
    print("-" * 65)
    print("  PEARSON CORRELATION WITH TARGET (MedHouseVal):")
    for feat, corr in summary.get("correlation_with_target", {}).items():
        bar_len = int(abs(corr) * 25)
        sign = "+" if corr >= 0 else "-"
        bar = sign * bar_len
        print(f"    {feat:<12} : {corr:+.4f} | {bar}")
    print("=" * 65 + "\n")


def cmd_benchmark():
    print("\n--- [5] RUN SCALABILITY BENCHMARK EXPERIMENT ---")
    partitions = int(prompt_float("Enter Spark RDD partition count", default_val=4, min_val=1, max_val=16))
    print(f"[*] Running repeatable benchmarks across 25%, 50%, 100% data partitions on Spark...")

    try:
        result = benchmark_service.run_benchmark_suite(fractions=[0.25, 0.50, 1.00], partitions=partitions)
        print("\n" + "=" * 70)
        print("  SCALABILITY BENCHMARK MEASUREMENTS:")
        print("=" * 70)
        print(f"{'Subset':<10} {'Rows':<10} {'Prep (s)':<12} {'Train (s)':<12} {'Inference (s)':<15} {'Total (s)':<10}")
        print("-" * 70)
        for r in result["runs"]:
            print(
                f"{r['percentage_label']:<10} {r['row_count']:<10,} "
                f"{r['preprocessing_duration_s']:<12.4f} {r['training_duration_s']:<12.4f} "
                f"{r['prediction_duration_s']:<15.4f} {r['total_duration_s']:<10.4f}"
            )
        print("-" * 70)
        print(f"  Total Benchmark Suite Duration: {result['total_suite_duration_s']:.2f} s")
        print(f"  Execution Master:               {result['execution_environment']['master']}")
        print(f"  Hardware / Scaling Note:        {result['execution_environment']['hardware_note']}")
        print("=" * 70 + "\n")
    except Exception as e:
        print(f"\n[!] Benchmark run failed: {e}\n")


def cmd_info():
    print("\n--- [6] SYSTEM & SPARK CLUSTER DIAGNOSTICS ---")
    spark_info = get_spark_status()
    print("\n" + "=" * 65)
    print("  SYSTEM RUNTIME STATUS:")
    print("=" * 65)
    print(f"  Python Version        : {sys.version.split()[0]}")
    print(f"  Spark Status          : {spark_info['status']}")
    print(f"  Spark Active Version  : {spark_info.get('version', 'Not started')}")
    print(f"  Spark Master          : {spark_info.get('master', settings.SPARK_MASTER)}")
    print(f"  Driver Memory         : {settings.SPARK_DRIVER_MEMORY}")
    print(f"  Shuffle Partitions    : {settings.SPARK_SHUFFLE_PARTITIONS}")
    print(f"  Dataset Cache Status  : {'Found' if dataset_service.csv_path.exists() else 'Missing'}")
    print(f"  Model Saved Status    : {'Trained' if model_service.is_model_trained() else 'Uninitialized'}")
    print(f"  Model Directory       : {model_service.models_dir.resolve()}")
    print("-" * 65)
    print("  REGISTERED MULTI-COUNTRY REGIONS:")
    for r in registry_service.list_regions():
        status_tag = f"[{r.get('support_status')}]"
        print(f"    - {r.get('country_code'):<4} {r.get('country_name'):<20} ({r.get('region')}): {status_tag}")
    print("=" * 65 + "\n")


def main_interactive():
    print(BANNER)
    while True:
        print("  MAIN MENU:")
        print("  1. Train Spark MLlib Model")
        print("  2. Predict Housing Value (Inference)")
        print("  3. Evaluate Model & View Residuals")
        print("  4. Explore Dataset & Statistics")
        print("  5. Run Scalability Benchmarks")
        print("  6. Show Cluster & Model Info")
        print("  7. Exit")
        print()

        choice = input("  Select an option [1-7]: ").strip()

        if choice == "1":
            cmd_train()
        elif choice == "2":
            cmd_predict()
        elif choice == "3":
            cmd_evaluate()
        elif choice == "4":
            cmd_explore()
        elif choice == "5":
            cmd_benchmark()
        elif choice == "6":
            cmd_info()
        elif choice in ("7", "q", "exit"):
            print("\n  Shutting down active Spark sessions... Goodbye!\n")
            stop_spark_session()
            break
        else:
            print("  [!] Invalid choice. Please choose 1 through 7.\n")


def main():
    parser = argparse.ArgumentParser(description="GlobalEstate AI CLI")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("train", help="Train Spark MLlib regression pipeline")
    subparsers.add_parser("predict", help="Interactive housing valuation inference")
    subparsers.add_parser("evaluate", help="Display model performance metrics")
    subparsers.add_parser("explore", help="Explore dataset features and summary stats")
    subparsers.add_parser("benchmark", help="Execute scalability benchmarking experiment")
    subparsers.add_parser("info", help="Display Spark cluster runtime diagnostics")

    args = parser.parse_args()

    if args.command == "train":
        cmd_train()
    elif args.command == "predict":
        cmd_predict()
    elif args.command == "evaluate":
        cmd_evaluate()
    elif args.command == "explore":
        cmd_explore()
    elif args.command == "benchmark":
        cmd_benchmark()
    elif args.command == "info":
        cmd_info()
    else:
        main_interactive()


if __name__ == "__main__":
    main()

