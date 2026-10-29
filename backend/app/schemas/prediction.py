"""
GlobalEstate AI - Prediction Schemas
INT315 - Cluster Computing Project
"""

from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class CaliforniaFeatures(BaseModel):
    MedInc: float = Field(..., ge=0.0, le=20.0, description="Median Income in block group ($10,000s)")
    HouseAge: float = Field(..., ge=0.5, le=100.0, description="Median House Age (years)")
    AveRooms: float = Field(..., ge=0.5, le=150.0, description="Average Rooms per household")
    AveBedrms: float = Field(..., ge=0.2, le=50.0, description="Average Bedrooms per household")
    Population: float = Field(..., ge=1.0, le=50000.0, description="Block group population")
    AveOccup: float = Field(..., ge=0.5, le=1500.0, description="Average Household Occupants")
    Latitude: float = Field(..., ge=32.0, le=43.0, description="Latitude (degrees north)")
    Longitude: float = Field(..., ge=-125.0, le=-113.0, description="Longitude (degrees west)")


class PredictionRequest(BaseModel):
    region_code: str = Field(default="USA", description="Country/Region ISO code")
    features: Optional[Dict[str, float]] = Field(
        default=None,
        description="Dictionary of feature key-value pairs matching region schema"
    )
    # Direct field fallback if passed at top level
    MedInc: Optional[float] = None
    HouseAge: Optional[float] = None
    AveRooms: Optional[float] = None
    AveBedrms: Optional[float] = None
    Population: Optional[float] = None
    AveOccup: Optional[float] = None
    Latitude: Optional[float] = None
    Longitude: Optional[float] = None

    def get_features_dict(self) -> Dict[str, float]:
        """Combines features dictionary or top-level fields."""
        if self.features:
            return self.features
        res = {}
        for f in ["MedInc", "HouseAge", "AveRooms", "AveBedrms", "Population", "AveOccup", "Latitude", "Longitude"]:
            val = getattr(self, f, None)
            if val is not None:
                res[f] = float(val)
        return res


class ConfidenceInterval(BaseModel):
    lower: int
    upper: int
    formatted: str


class ExecutionMetadata(BaseModel):
    inference_latency_ms: float
    total_request_latency_ms: float
    spark_master: str
    model_version: str


class PredictionResponse(BaseModel):
    model_id: str
    region: str
    predicted_target_value: float
    target_unit: str
    estimated_usd: int
    formatted_usd: str
    confidence_interval_95_usd: ConfidenceInterval
    disclaimer: str
    inputs_echo: Dict[str, float]
    execution_metadata: ExecutionMetadata

