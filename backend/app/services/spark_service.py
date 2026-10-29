"""
GlobalEstate AI - Spark Session Lifecycle Manager
INT315 - Cluster Computing Project
"""

import os
import sys
import logging
from typing import Optional, Dict, Any

# Ensure PySpark workers on Windows find the current python executable instead of non-existent 'python3'
os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

logger = logging.getLogger("GlobalEstate.SparkService")

# SparkSession singleton reference
_spark_instance = None


def get_spark_session(
    app_name: str = "GlobalEstateAI-SparkEngine",
    master: str = "local[*]",
    driver_memory: str = "2g",
    shuffle_partitions: int = 4
):
    """
    Retrieves or initializes a singleton Apache SparkSession.
    Configures low-overhead local execution optimized for Windows / single-node cluster simulation.
    """
    global _spark_instance
    if _spark_instance is not None:
        try:
            # Check if active
            if not _spark_instance._jsc.sc().isStopped():
                return _spark_instance
        except Exception:
            _spark_instance = None

    try:
        from pyspark.sql import SparkSession
    except ImportError as e:
        logger.error(f"PySpark is not installed in the active environment: {e}")
        raise RuntimeError("PySpark module not found. Please run environment setup.")

    logger.info(f"Initializing Apache SparkSession: {app_name} on {master}")

    builder = (
        SparkSession.builder
        .appName(app_name)
        .master(master)
        .config("spark.driver.memory", driver_memory)
        .config("spark.sql.shuffle.partitions", str(shuffle_partitions))
        .config("spark.driver.host", "localhost")
        .config("spark.driver.bindAddress", "127.0.0.1")
        .config("spark.ui.showConsoleProgress", "false")
        .config("spark.sql.execution.arrow.pyspark.enabled", "false")
    )

    _spark_instance = builder.getOrCreate()
    # Suppress verbose JVM log spam
    _spark_instance.sparkContext.setLogLevel("WARN")

    logger.info(
        f"SparkSession active: version={_spark_instance.version}, "
        f"master={_spark_instance.sparkContext.master}, "
        f"app_id={_spark_instance.sparkContext.applicationId}"
    )
    return _spark_instance


def stop_spark_session():
    """Safely shuts down the active SparkSession."""
    global _spark_instance
    if _spark_instance is not None:
        logger.info("Stopping Apache SparkSession...")
        try:
            _spark_instance.stop()
        except Exception as e:
            logger.warning(f"Error stopping SparkSession: {e}")
        finally:
            _spark_instance = None


def get_spark_status() -> Dict[str, Any]:
    """Inspects the current state of the Spark runtime."""
    global _spark_instance
    if _spark_instance is None:
        return {
            "status": "STOPPED",
            "is_active": False,
            "version": None,
            "master": None,
            "app_name": None,
            "app_id": None,
            "default_parallelism": None
        }

    try:
        sc = _spark_instance.sparkContext
        is_stopped = sc._jsc.sc().isStopped()
        if is_stopped:
            return {
                "status": "STOPPED",
                "is_active": False,
                "version": _spark_instance.version,
                "master": sc.master,
                "app_name": sc.appName,
                "app_id": sc.applicationId,
                "default_parallelism": None
            }

        return {
            "status": "ACTIVE",
            "is_active": True,
            "version": _spark_instance.version,
            "master": sc.master,
            "app_name": sc.appName,
            "app_id": sc.applicationId,
            "default_parallelism": sc.defaultParallelism,
            "spark_user": sc.sparkUser()
        }
    except Exception as e:
        return {
            "status": "ERROR",
            "is_active": False,
            "error": str(e)
        }

