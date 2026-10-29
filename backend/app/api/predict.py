"""
GlobalEstate AI - Real-Time Housing Price Prediction Endpoint
INT315 - Cluster Computing Project
"""

from fastapi import APIRouter, HTTPException

from backend.app.schemas.prediction import PredictionRequest, PredictionResponse
from backend.app.services.registry_service import registry_service
from backend.app.services.model_service import model_service

router = APIRouter(prefix="/predict", tags=["Prediction"])


@router.post("", response_model=PredictionResponse)
def predict_housing_value(request: PredictionRequest):
    """
    Predicts median real estate value using trained Apache Spark MLlib regression pipeline.
    Validates features against region schema and returns valuation in USD.
    """
    features_dict = request.get_features_dict()

    # 1. Validate Region and Feature Schema
    is_valid, err_msg, region_config = registry_service.validate_prediction_request(
        request.region_code, features_dict
    )
    if not is_valid:
        raise HTTPException(status_code=400, detail=err_msg)

    # 2. Check if model exists
    target_model_id = region_config.get("model_id", model_service.default_model_id)
    if not model_service.is_model_trained(target_model_id):
        raise HTTPException(
            status_code=400,
            detail=(
                f"Trained model '{target_model_id}' is not ready. "
                "Please trigger training via POST /api/models/{model_id}/train or run `python backend/scripts/train_model.py`."
            )
        )

    # 3. Perform MLlib Inference
    try:
        prediction_result = model_service.predict(features_dict)
        return prediction_result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Inference pipeline execution error: {str(e)}"
        )

