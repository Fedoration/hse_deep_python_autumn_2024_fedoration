class SomeModel:
    def fit(self, data: list[str]) -> None:
        raise NotImplementedError
    def predict(self, message: str) -> float:
        raise NotImplementedError


def predict_message_mood(
    message: str,
    bad_thresholds: float = 0.3,
    good_thresholds: float = 0.8,
) -> str:
    model = SomeModel()
    prediction = model.predict(message)

    if prediction < bad_thresholds:
        return "неуд"
    if prediction > good_thresholds:
        return "отл"
    return "норм"
