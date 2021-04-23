from lib.evaluation.evaluate import get_evaluation_metrics
from loguru import logger


def train(lr, features, target, transformer = None):
    logger.info(f"start fitting a {lr.__class__}...")
    if transformer:
        lr = lr.fit(features, transformer(target, forward = True))
    predicted_target = lr.predict(features)
    if transformer:
        predicted_target = transformer(predicted_target, forward= False)
    logger.info(get_evaluation_metrics(target, predicted_target))
    return lr
