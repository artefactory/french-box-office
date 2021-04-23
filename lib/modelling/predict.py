def predict(model, features, transformer=None):
    predicted_target = model.predict(features)
    if transformer:
        predicted_target = transformer(predicted_target, forward=False)
    return predicted_target