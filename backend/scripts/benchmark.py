"""
GlobalEstate AI - Scalability Benchmark Script
INT315 - Cluster Computing Project

Executes scalable Spark MLlib workload experiments and records wall-clock timings.
Usage:
    python backend/scripts/benchmark.py [--partitions 4]
"""

import sys
import argparse
import logging
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from backend.app.services.benchmark_service import benchmark_service
from backend.app.services.spark_service import stop_spark_session

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("GlobalEstate.BenchmarkCLI")


def main():
    parser = argparse.ArgumentParser(description="Run Scalability Benchmarks for GlobalEstate AI")
    parser.add_argument("--partitions", type=int, default=4, help="Spark shuffle/RDD partition count (default: 4)")
    args = parser.parse_args()

    print("\n" + "=" * 70)
    print("  GLOBALESTATE AI - APACHE SPARK MLLIB SCALABILITY EXPERIMENT")
    print("  INT315: Cluster Computing Project")
    print("=" * 70 + "\n")

    print("[*] Benchmark Configurations:")
    print(f"    Workload subsets: 25%, 50%, 100% of California Census Blocks")
    print(f"    RDD Partitions:   {args.partitions}")
    print(f"    Execution Mode:   Local[*] Single-Node Spark Cluster Simulation\n")

    try:
        results = benchmark_service.run_benchmark_suite(
            fractions=[0.25, 0.50, 1.00],
            partitions=args.partitions
        )

        print("\n" + "=" * 70)
        print("  BENCHMARK MEASUREMENT RESULTS (ACTUAL TIMINGS):")
        print("=" * 70)
        print(f"{'Subset':<10} {'Rows':<10} {'Prep (s)':<12} {'Train (s)':<12} {'Inference (s)':<15} {'Total (s)':<10}")
        print("-" * 70)
        for r in results["runs"]:
            print(
                f"{r['percentage_label']:<10} {r['row_count']:<10,} "
                f"{r['preprocessing_duration_s']:<12.4f} {r['training_duration_s']:<12.4f} "
                f"{r['prediction_duration_s']:<15.4f} {r['total_duration_s']:<10.4f}"
            )
        print("-" * 70)
        print(f"  Total Suite Duration: {results['total_suite_duration_s']:.2f} s")
        print(f"  Execution Master:     {results['execution_environment']['master']}")
        print(f"  Hardware Note:        {results['execution_environment']['hardware_note']}")
        print("=" * 70 + "\n")

    finally:
        stop_spark_session()


if __name__ == "__main__":
    main()

