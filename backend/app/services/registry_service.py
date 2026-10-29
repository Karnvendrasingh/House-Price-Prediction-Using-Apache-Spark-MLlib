"""
GlobalEstate AI - Multi-Country & Dataset Registry Service
INT315 - Cluster Computing Project
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

from backend.app.core.config import settings

logger = logging.getLogger("GlobalEstate.RegistryService")


class RegistryService:
    def __init__(self, regions_dir: Path = settings.REGIONS_DIR):
        self.regions_dir = regions_dir

    def list_regions(self) -> List[Dict[str, Any]]:
        """Scans the regions directory and returns list of registered regional configurations."""
        regions = []
        if not self.regions_dir.exists():
            return regions

        for f in self.regions_dir.glob("*.json"):
            try:
                with open(f, "r", encoding="utf-8") as rf:
                    data = json.load(rf)
                    regions.append(data)
            except Exception as e:
                logger.warning(f"Could not load region file {f}: {e}")

        # Ensure active regions come first
        regions.sort(key=lambda x: (x.get("support_status") != "ACTIVE", x.get("country_name", "")))
        return regions

    def get_region(self, country_code: str) -> Optional[Dict[str, Any]]:
        """Retrieves configuration for a specific country or region code (e.g. 'USA', 'GBR')."""
        code = country_code.upper()
        # Direct file check
        candidate_file = self.regions_dir / f"{code.lower()}.json"
        if candidate_file.exists():
            with open(candidate_file, "r", encoding="utf-8") as f:
                return json.load(f)

        # Fallback check inside JSON files
        for r in self.list_regions():
            if r.get("country_code", "").upper() == code:
                return r

        return None

    def validate_prediction_request(self, region_code: str, features: Dict[str, Any]) -> Tuple[bool, Optional[str], Optional[Dict[str, Any]]]:
        """
        Validates if the requested region is active and if the provided feature payload
        strictly matches the country's registered feature schema.
        Returns: (is_valid, error_message, region_config)
        """
        region = self.get_region(region_code)
        if not region:
            return (
                False,
                f"Region code '{region_code}' is not recognized in the GlobalEstate registry.",
                None
            )

        if region.get("support_status") != "ACTIVE":
            return (
                False,
                (
                    f"Model not available for region '{region.get('country_name', region_code)}' ({region.get('region')}). "
                    f"Support status: {region.get('support_status')}. "
                    f"Notes: {region.get('compatibility_notes', 'Trained model has not been validated for this market.')} "
                    f"To prevent misleading valuations, automated estimates are disabled for this region."
                ),
                region
            )

        # Validate feature schema
        feature_schema = region.get("feature_schema", [])
        missing_features = []
        invalid_types = []

        for feat in feature_schema:
            name = feat["name"]
            if name not in features:
                missing_features.append(name)
            else:
                val = features[name]
                try:
                    float_val = float(val)
                    # Check optional bounds if defined
                    if "min" in feat and float_val < feat["min"]:
                        invalid_types.append(f"{name} ({float_val}) is below realistic minimum {feat['min']}")
                    if "max" in feat and float_val > feat["max"]:
                        invalid_types.append(f"{name} ({float_val}) exceeds realistic maximum {feat['max']}")
                except (ValueError, TypeError):
                    invalid_types.append(f"{name} must be numeric, got {type(val).__name__}")

        if missing_features:
            return (
                False,
                f"Missing required features for {region['country_name']}: {', '.join(missing_features)}",
                region
            )

        if invalid_types:
            return (
                False,
                f"Invalid feature values: {'; '.join(invalid_types)}",
                region
            )

        return (True, None, region)


registry_service = RegistryService()
