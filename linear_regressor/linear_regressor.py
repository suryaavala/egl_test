import numpy as np
from typing import List
import logging

log = logging.getLogger(__name__)


class SimpleLinearRegression:
    def __init__(self, iterations: int = 15000, lr: float = 0.1):
        self.iterations = (
            iterations  # number of iterations the fit method will be called
        )
        self.lr = lr  # The learning rate
        self.losses: List[
            np.ndarray
        ] = []  # A list to hold the history of the calculated losses
        self.W: np.ndarray = np.array(None)  # the slope of the model
        self.b: np.ndarray = np.array(None)  # the intercept of the model

    def __loss(self, y: np.ndarray, y_hat: np.ndarray) -> List[np.ndarray]:
        """

        :param y: the actual output on the training set
        :param y_hat: the predicted output on the training set
        :return:
            loss: the sum of squared error

        """
        # ToDO calculate the loss. use the sum of squared error formula for simplicity
        # NOTE Using Mean Squared Error (sum( (y - y_hat)^2 ) / N)
        loss = np.sum((y - y_hat) ** 2) / y.shape[0]

        self.losses.append(loss)
        return loss

    def __init_weights(self, X: np.ndarray) -> None:
        """

        :param X: The training set
        """
        weights = np.random.normal(size=X.shape[1] + 1)
        self.W = weights[: X.shape[1]].reshape(-1, X.shape[1])
        self.b = weights[-1]

    def __sgd(self, X: np.ndarray, y: np.ndarray, y_hat: np.ndarray) -> None:
        """

        :param X: The training set
        :param y: The actual output on the training set
        :param y_hat: The predicted output on the training set
        :return:
            sets updated W and b to the instance Object (self)
        """
        if X.shape[0] != y.shape[0] or X.shape[0] != y_hat.shape[0]:
            raise ValueError("X, y and y_hat must have the same number of rows")
        # ToDo calculate dW & db.
        dW = (-2 / X.shape[0]) * np.sum(np.dot(X.T, (y - y_hat)))
        db = (-2 / X.shape[0]) * np.sum((y - y_hat))
        #  ToDO update the self.W and self.b using the learning rate and the values for dW and db
        self.W = self.W - self.lr * dW
        self.b = self.b - self.lr * db

    def fit(self, X: np.ndarray, y: np.ndarray) -> None:
        """

        :param X: The training set
        :param y: The true output of the training set
        :return:
        """
        self.__init_weights(X)
        y_hat = self.predict(X)
        loss = self.__loss(y, y_hat)
        log.debug(f"Initial Loss: {loss}")
        for i in range(self.iterations + 1):
            self.__sgd(X, y, y_hat)
            y_hat = self.predict(X)
            # NOTE try asarray_chkfinite here
            loss = self.__loss(y, y_hat)
            if not i % 100:
                log.debug(f"Iteration {i}, Loss: {loss}")

    def predict(self, X: np.ndarray) -> np.ndarray:
        """

        :param X: The training dataset
        :return:
            y_hat: the predicted output
        """
        # ToDO calculate the predicted output y_hat. remember the function of a line is defined as y = WX + b
        y_hat = np.dot(X, self.W) + self.b
        return y_hat
