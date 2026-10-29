"""
GlobalEstate AI - Core Configuration
INT315 - Cluster Computing Project
"""

import os
from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env", extra="allow")
    PROJECT_NAME: str = "GlobalEstate AI"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "Scalable Real Estate Price Prediction Platform powered by Apache Spark MLlib"
    API_PREFIX: str = "/api"

    # Base Paths
    BACKEND_DIR: Path = Path(__file__).resolve().parent.parent.parent
    DATA_DIR: Path = BACKEND_DIR / "data"
    MODELS_DIR: Path = BACKEND_DIR / "models"
    CONFIG_DIR: Path = BACKEND_DIR / "config"
    REGIONS_DIR: Path = CONFIG_DIR / "regions"
    MODEL_CONFIGS_DIR: Path = CONFIG_DIR / "models"
    BENCHMARKS_DIR: Path = DATA_DIR / "benchmarks"

    # Spark Engine Settings
    SPARK_APP_NAME: str = "GlobalEstateAI-SparkEngine"
    SPARK_MASTER: str = "local[*]"
    SPARK_DRIVER_MEMORY: str = "2g"
    SPARK_EXECUTOR_MEMORY: str = "2g"
    SPARK_SHUFFLE_PARTITIONS: int = 4
    SPARK_LOG_LEVEL: str = "WARN"

    # Default Region and Model
    DEFAULT_REGION: str = "USA"
    DEFAULT_DATASET_ID: str = "usa_california"
    DEFAULT_MODEL_ID: str = "usa_california_lr"

    # Target scaling for California Housing: MedHouseVal is in $100,000s
    TARGET_SCALE_FACTOR: float = 100000.0



settings = Settings()

# Ensure critical runtime directories exist
settings.DATA_DIR.mkdir(parents=True, exist_ok=True)
settings.MODELS_DIR.mkdir(parents=True, exist_ok=True)
settings.CONFIG_DIR.mkdir(parents=True, exist_ok=True)
settings.REGIONS_DIR.mkdir(parents=True, exist_ok=True)
settings.MODEL_CONFIGS_DIR.mkdir(parents=True, exist_ok=True)
settings.BENCHMARKS_DIR.mkdir(parents=True, exist_ok=True)

