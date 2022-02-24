import pytest
from pathlib import Path
from linear_regressor import utils


def test_valid_get_py_project_dir():
    excpeted_py_project_dir = Path(__file__).resolve(strict=True).parents[1]
    assert excpeted_py_project_dir == utils.get_py_project_dir()


@pytest.mark.parametrize(
    "relpath",
    [
        "tests",
        "linear_regressor",
        "linear_regressor/linear_regressor.py",
        "models/",
        "./tests",
    ],
)
def test_valid_get_abs_path(relpath):
    expected_abs_path = Path(__file__).resolve(strict=True).parents[1].joinpath(relpath)
    assert expected_abs_path == utils.get_abs_path(relpath)
