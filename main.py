import click
from linear_regressor.linear_regressor import SimpleLinearRegression
from linear_regressor.utils import generate_data, evaluate, save_artefact, get_abs_path

import logging
from logging.config import fileConfig
import time

fileConfig(get_abs_path("logging_config.ini"), disable_existing_loggers=False)
logging.Formatter.converter = time.gmtime
LOGGER = logging.getLogger("linear_regressor")
LOGGER.propagate = True
CLI_LOGGER = logging.getLogger(__name__)
if not CLI_LOGGER.handlers:
    CLI_LOGGER.addHandler(logging.NullHandler())


@click.group()
def cli():
    """CLI for the linear regressor"""
    pass


@cli.command()
@click.option("--iterations", default=15000, help="Number of iterations")
@click.option("--lr", default=0.1, help="Learning rate")
@click.option(
    "--model-save-path",
    default="models/simple_linear_regressor.joblib",
    help="Path to save the model",
)
def train(
    iterations: int,
    lr: float,
    model_save_path: str,
) -> None:
    """Train the model

    Args:
        iterations (int): number of iterations to train the model for
        lr (float): learning rate for model training
        model_save_path (str): path to save the model
    """

    CLI_LOGGER.info(
        f"Training the model with {iterations} iterations and learning rate {lr}"
    )
    X_train, y_train, X_test, y_test = generate_data()
    CLI_LOGGER.debug(
        f"X_train: {X_train.shape}, y_train: {y_train.shape}, X_test: {X_test.shape}, y_test: {y_test.shape}"
    )
    model = SimpleLinearRegression()
    model.fit(X_train, y_train)
    predicted = model.predict(X_test)
    mse, r2_score = evaluate(model, X_test, y_test, predicted)
    CLI_LOGGER.info(f"Slope: {model.W.reshape(())}; Intercept: {model.b}")
    CLI_LOGGER.info(f"MSE: {mse:.2f}, R2: {r2_score:.2f}")

    save_artefact(model, model_save_path)
    CLI_LOGGER.info(f"Model saved to {get_abs_path(model_save_path)}")
    return None


if __name__ == "__main__":
    cli()
