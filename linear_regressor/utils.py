import numpy as np
from sklearn.datasets import load_diabetes
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
from pathlib import Path
from typing import Union, Any, Tuple
from os import path
import joblib
from linear_regressor.linear_regressor import SimpleLinearRegression
from sklearn.base import BaseEstimator
import logging

log = logging.getLogger(__name__)


def generate_data() -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Generates a random dataset from a normal distribution.

    Returns:
        diabetes_X_train: the training dataset
        diabetes_y_train: The output corresponding to the training set
        diabetes_X_test: the test dataset
        diabetes_y_test: The output corresponding to the test set

    """
    # Load the diabetes dataset
    diabetes_X, diabetes_y = load_diabetes(return_X_y=True)

    # Use only one feature
    diabetes_X = diabetes_X[:, np.newaxis, 2]

    # Split the data into training/testing sets
    diabetes_X_train = diabetes_X[:-20]
    diabetes_X_test = diabetes_X[-20:]

    # Split the targets into training/testing sets
    diabetes_y_train = diabetes_y[:-20].reshape(-1, 1)
    diabetes_y_test = diabetes_y[-20:].reshape(-1, 1)

    log.debug(
        f"# Training Samples: {len(diabetes_X_train)}; # Test samples: {len(diabetes_X_test)};"
    )
    return diabetes_X_train, diabetes_y_train, diabetes_X_test, diabetes_y_test


def evaluate(
    model: Union[SimpleLinearRegression, BaseEstimator],
    X: np.ndarray,
    y: np.ndarray,
    y_predicted: np.ndarray,
    plot: bool = False,
) -> Tuple[Union[float, np.ndarray], Union[float, np.ndarray]]:
    """Calculates evaluation metrics."""
    # The mean squared error
    mse = mean_squared_error(y, y_predicted)
    # The coefficient of determination: 1 is perfect prediction
    r2 = r2_score(y, y_predicted)

    if plot:
        # Plot outputs
        plt.scatter(X, y, color="black")
        plt.plot(X, y_predicted, color="blue", linewidth=3)

        plt.xticks(())
        plt.yticks(())

        plt.show()

    if r2 >= 0.4:
        log.info("****** Success ******")
    else:
        log.info("****** Failed ******")

    return mse, r2


def get_py_project_dir() -> Path:
    """Returns abspath of the current python project's base dir - so the dirpath of where setup.py resides

    Returns:
        Path: absolute path of this python project
    """
    return Path(__file__).resolve(strict=True).parents[1]


def get_abs_path(file_path: str) -> Path:
    """Takes in a relative (or absolute path) path, relative to the current python project's base directory (where setup.py resides), and returns the absolute path equivalent

    Args:
        file_path (str): relative path, relative to the current python project's base directory (where setup.py resides)

    Returns:
        PosixPath: returns the absolute path
    """  # noqa: E501

    return get_py_project_dir().joinpath(file_path).resolve(strict=True)


def save_artefact(artefact: Any, artefact_path: str) -> None:
    """Save artefact to artefact_path

    Args:
        artefact (Any): artefact to be saved
        artefact_path (Path): path to save artefact to,
                                must be either absolute
                                    or relative to linear_regressor's setup.py.
    """
    basename = path.basename(artefact_path)
    dirname = path.dirname(artefact_path)
    abs_path = str(get_abs_path(dirname) / basename)
    joblib.dump(artefact, abs_path)
    return


def load_artefact(artefact_path: str) -> Any:
    """Load artefact from artefact_path

    Args:
        artefact_path (Path): path to load artefact from,
                                must be either absolute
                                    or relative to linear_regressor's setup.py.

    Returns:
        Any: loaded artefact
    """
    abs_path = str(get_abs_path(artefact_path))
    artefact = joblib.load(abs_path)
    return artefact
