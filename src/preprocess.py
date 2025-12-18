import pandas as pd
import numpy as np

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler


# Feature and target definitions (UCI Cleveland dataset)
FEATURE_COLUMNS = [
    "age", "sex", "cp", "trestbps", "chol", "fbs",
    "restecg", "thalach", "exang", "oldpeak",
    "slope", "ca", "thal"
]

TARGET_COLUMN = "target"


def load_data(path: str) -> pd.DataFrame:
    """
    Load the Heart Disease UCI dataset from CSV
    """
    df = pd.read_csv(path, header=None)
    df.columns = FEATURE_COLUMNS + [TARGET_COLUMN]
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean raw data:
    - Handle missing values ('?')
    - Convert data types
    - Encode target variable
    """
    df = df.copy()

    # Replace '?' with NaN
    df.replace("?", np.nan, inplace=True)

    # Convert all columns to numeric
    df = df.astype(float)

    # Binary classification: 1 = disease present, 0 = absent
    df[TARGET_COLUMN] = (df[TARGET_COLUMN] > 0).astype(int)

    # Median imputation
    df.fillna(df.median(), inplace=True)

    return df


def split_features_target(df: pd.DataFrame):
    """
    Split dataframe into X (features) and y (target)
    """
    X = df[FEATURE_COLUMNS]
    y = df[TARGET_COLUMN]
    return X, y


def get_preprocessor():
    """
    Create preprocessing pipeline (scaling)
    """
    return ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), FEATURE_COLUMNS)
        ]
    )