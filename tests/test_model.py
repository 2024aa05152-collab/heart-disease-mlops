import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression

from src.preprocess import load_data, clean_data, split_features_target, get_preprocessor


def test_model_training():
    df = load_data("data/heart.csv")
    df_clean = clean_data(df)
    X, y = split_features_target(df_clean)

    pipeline = Pipeline([
        ("preprocessor", get_preprocessor()),
        ("model", LogisticRegression(max_iter=1000))
    ])

    pipeline.fit(X, y)

    score = pipeline.score(X, y)
    assert score > 0.5  # sanity check


def test_model_prediction_shape():
    df = load_data("data/heart.csv")
    df_clean = clean_data(df)
    X, y = split_features_target(df_clean)

    pipeline = Pipeline([
        ("preprocessor", get_preprocessor()),
        ("model", LogisticRegression(max_iter=1000))
    ])

    pipeline.fit(X, y)
    preds = pipeline.predict(X[:5])

    assert len(preds) == 5
