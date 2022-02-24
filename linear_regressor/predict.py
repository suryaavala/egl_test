from linear_regressor.utils import load_artefact
from linear_regressor.linear_regressor import SimpleLinearRegression
from typing import List
import logging
import numpy as np

log = logging.getLogger(__name__)

model = load_artefact("models/simple_linear_regressor.joblib")
log.info("Loaded model from models/simple_linear_regressor.joblib")


def get_predictions(
    instances: List[List[float]],
    model: SimpleLinearRegression = model,
) -> List[float]:
    """
    Predicts the player's height based weight and age using the given model.
    Args:
        model (str): model to use for prediction
                        Default: model loaded from models/simple_linear_regressor.joblib
    Returns:
        List[float]: predictions.
    """

    predictions = model.predict(np.asarray(instances))
    log.debug(f"Predictions: {predictions}")

    return predictions.tolist()
