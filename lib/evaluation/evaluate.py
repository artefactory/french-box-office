from sklearn.metrics import mean_squared_error, mean_absolute_error
import numpy as np
from loguru import logger


def get_evaluation_metrics(y_test, y_pred, y_train=None) -> dict:
    metrics = {
        'mape': mean_absolute_percentage_error(y_test, y_pred),
        'rmse': mean_squared_error(y_test, y_pred, squared=False),
        'mae': mean_absolute_error(y_test, y_pred),
    }
    return metrics


def mean_absolute_percentage_error(y_true, y_pred):
    """in percent"""
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.mean(np.abs((y_true - y_pred)/y_true)) * 100


def prettify_metrics(metrics: dict) -> str:
    output = [f"Evaluation:\n{'-'*10}"]
    for name, metric in metrics.items():
        output.append((f'- {name.upper()}: {round(metric, 2)}'))
    return '\n'.join(output) +'\n'


def evaluate(lr, features, target, transformer=None, ret=False):
    predicted_target = lr.predict(features)
    if transformer:
        predicted_target = transformer(predicted_target, forward=False)
    
    logger.info(get_evaluation_metrics(target, predicted_target))
    if ret==True:
        return get_evaluation_metrics(target, predicted_target)