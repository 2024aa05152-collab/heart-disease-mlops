import pandas as pd
from src.preprocess import load_data, clean_data, split_features_target, get_preprocessor


def test_load_data():
    df = load_data("data/heart.csv")
    assert isinstance(df, pd.DataFrame)
    assert df.shape[1] == 14  # 13 features + target


def test_clean_data():
    df = load_data("data/heart.csv")
    df_clean = clean_data(df)

    # No missing values after cleaning
    assert df_clean.isnull().sum().sum() == 0

    # Target must be binary
    assert set(df_clean["target"].unique()).issubset({0, 1})


def test_split_features_target():
    df = load_data("data/heart.csv")
    df_clean = clean_data(df)

    X, y = split_features_target(df_clean)

    assert X.shape[1] == 13
    assert len(X) == len(y)


def test_preprocessor():
    preprocessor = get_preprocessor()
    assert preprocessor is not None
