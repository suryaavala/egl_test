import click
from linear_regressor.linear_regressor import SimpleLinearRegression
from linear_regressor.utils import generate_data, evaluate, save_artefact, get_abs_path
from multiprocessing import cpu_count
import logging
from logging.config import fileConfig
import time
from linear_regressor.api import app
from linear_regressor.server import start


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


@cli.command()
@click.option(
    "--host",
    type=str,
    default="0.0.0.0",  # nosec
    help="server host.",
    show_default=True,
)
@click.option("--port", type=int, default=5000, help="server port", show_default=True)
@click.option("--debug", is_flag=True, help="Enable debug mode")
@click.option(
    "--server",
    default="gunicorn",
    type=click.Choice(["gunicorn", "flask"], case_sensitive=False),
    help="Server type to use: gunicorn for prod & flask dev server",
)
@click.option(
    "--workers",
    type=int,
    default=(cpu_count() * 2) + 1,
    help="Number of workers (when using --server gunicorn)",
)
def serve(host: str, port: int, server: str, workers: int, debug: bool):
    """Server linear_regressor application depending on command line arguments

    Args:\n
        host (str): host address to start the server at.
                    Defaults to "0.0.0.0".\n
        port (int): port number for the server to listen at.
                    Defaults to 5000.\n
        with_gunicorn (bool): use gunicorn instead of flask dev server.
                               Defaults to False.\n
        workers (int): number of workers to use when using gunicorn.
                       Defaults to (cpu_count() * 2) + 1.\n
        debug (bool): enable debug mode.\n
                        Defaults to False.
    """
    CLI_LOGGER.info(f"Starting {server} server at {host}:{port}")
    start(
        app=app,
        host=host,
        port=port,
        server=server,
        workers=workers,
        debug=debug,
    )


if __name__ == "__main__":
    cli()
