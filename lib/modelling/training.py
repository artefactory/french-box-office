from lib.evaluation.evaluate import get_evaluation_metrics
from loguru import logger
from lightgbm import LGBMRegressor


def train(lr, features, target, transformer = None):
    logger.info(f"start fitting a {lr.__class__}...")
    if transformer:
        lr = lr.fit(features, transformer(target, forward = True))
    predicted_target = lr.predict(features)
    if transformer:
        predicted_target = transformer(predicted_target, forward= False)
    logger.info(get_evaluation_metrics(target, predicted_target))
    return lr


def save_model(model: LGBMRegressor, filepath: str):
    model.booster_.save_model(filepath, num_iteration=model.best_iteration_)
    logger.info(f'Model saved to {filepath}')
