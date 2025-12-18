import joblib
import numpy as np
import mlflow
import mlflow.sklearn

from pathlib import Path
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_validate

from preprocess import (
    load_data,
    clean_data,
    split_features_target,
    get_preprocessor
)

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "heart.csv"
MODEL_PATH = BASE_DIR / "models" / "heart_model.pkl"

# MLflow setup
mlflow.set_experiment("Heart Disease Classification")


def evaluate_model(pipeline, X, y):
    scores = cross_validate(
        pipeline,
        X,
        y,
        cv=5,
        scoring=["accuracy", "precision", "recall", "roc_auc"]
    )

    return {
        metric: np.mean(scores[f"test_{metric}"])
        for metric in ["accuracy", "precision", "recall", "roc_auc"]
    }


def main():
    df = load_data(DATA_PATH)
    df = clean_data(df)
    X, y = split_features_target(df)

    models = {
        "LogisticRegression": LogisticRegression(max_iter=1000),
        "RandomForest": RandomForestClassifier(
            n_estimators=200,
            random_state=42
        )
    }

    results = {}

    for name, model in models.items():
        with mlflow.start_run(run_name=name):

            pipeline = Pipeline([
                ("preprocessor", get_preprocessor()),
                ("model", model)
            ])

            metrics = evaluate_model(pipeline, X, y)
            results[name] = metrics

            # Log parameters
            mlflow.log_param("model_type", name)

            if name == "LogisticRegression":
                mlflow.log_param("max_iter", model.max_iter)

            if name == "RandomForest":
                mlflow.log_param("n_estimators", model.n_estimators)
                mlflow.log_param("random_state", model.random_state)

            # Log metrics
            for k, v in metrics.items():
                mlflow.log_metric(k, v)

            print(f"\n{name} metrics logged to MLflow")

    # Select best model
    best_model_name = max(results, key=lambda x: results[x]["roc_auc"])
    best_model = models[best_model_name]

    final_pipeline = Pipeline([
        ("preprocessor", get_preprocessor()),
        ("model", best_model)
    ])

    final_pipeline.fit(X, y)

    # Save model locally
    joblib.dump(final_pipeline, MODEL_PATH)

    # Log final model artifact
    with mlflow.start_run(run_name="Final_Model"):
        mlflow.sklearn.log_model(final_pipeline, "model")
        mlflow.log_param("selected_model", best_model_name)

    print(f"\n Best model saved and logged: {best_model_name}")


if __name__ == "__main__":
    main()
