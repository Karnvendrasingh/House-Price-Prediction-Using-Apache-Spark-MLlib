"""
GlobalEstate AI - Scalability Benchmark Endpoints
INT315 - Cluster Computing Project
"""

import threading
from typing import Dict, Any, List
from fastapi import APIRouter, HTTPException, BackgroundTasks

from backend.app.schemas.benchmark import BenchmarkRunRequest, BenchmarkResponse
from backend.app.services.benchmark_service import benchmark_service

router = APIRouter(prefix="/benchmarks", tags=["Scalability Benchmarks"])

_benchmark_state = {
    "is_running": False,
    "current_run_id": None,
    "last_error": None
}


def _run_benchmark_job(fractions: List[float], partitions: int, synthetic: bool):
    global _benchmark_state
    try:
        _benchmark_state["is_running"] = True
        _benchmark_state["last_error"] = None
        benchmark_service.run_benchmark_suite(
            fractions=fractions,
            partitions=partitions,
            synthetic_scaling=synthetic
        )
    except Exception as e:
        _benchmark_state["last_error"] = str(e)
    finally:
        _benchmark_state["is_running"] = False


@router.get("/status")
def get_benchmark_status():
    """Returns current benchmark worker status."""
    return {
        "is_running": _benchmark_state["is_running"],
        "last_error": _benchmark_state["last_error"]
    }


@router.get("/results", response_model=List[Dict[str, Any]])
def get_benchmark_results():
    """Retrieves all historical scalability benchmark experiments."""
    return benchmark_service.get_benchmark_history()


@router.post("/run")
def trigger_benchmark(
    payload: BenchmarkRunRequest,
    background_tasks: BackgroundTasks
):
    """Submits a scalability benchmark execution task to the Spark engine."""
    global _benchmark_state
    if _benchmark_state["is_running"]:
        return {
            "status": "ALREADY_RUNNING",
            "message": "A scalability benchmark job is currently running on the Spark cluster."
        }

    background_tasks.add_task(
        _run_benchmark_job,
        fractions=payload.fractions,
        partitions=payload.partitions,
        synthetic=payload.synthetic_scaling
    )

    return {
        "status": "SUBMITTED",
        "message": "Scalability benchmark suite queued for Spark execution.",
        "configuration": payload.dict()
    }

