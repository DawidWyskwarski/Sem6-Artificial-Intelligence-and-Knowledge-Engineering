from typing import Dict
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator
from sklearn.compose import ColumnTransformer
from sklearn.base import clone
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from pandas import DataFrame
from enum import StrEnum


class Metric(StrEnum):
    ACCURACY = "val_accuracy"
    PRECISION = "val_precision"
    RECALL = "val_recall"
    F1_SCORE = "val_f1"


def create_evaluation_dataframe(
    X_train: DataFrame,
    y_train: DataFrame,
    X_val: DataFrame,
    y_val: DataFrame,
    num_pipelines: Dict[str, Pipeline],
    cat_pipelines: Dict[str, Pipeline],
    models: Dict[str, BaseEstimator],
    sort_by: Metric = Metric.ACCURACY,
) -> DataFrame:

    results = []

    num_cols = list(X_train.select_dtypes(include=["number"]).columns)
    cat_cols = list(X_train.select_dtypes(exclude=["number"]).columns)

    for num_name, num_pipe in num_pipelines.items():
        for cat_name, cat_pipe in cat_pipelines.items():
            preprocessor = ColumnTransformer(
                transformers=[
                    ("num", clone(num_pipe), num_cols),
                    ("cat", clone(cat_pipe), cat_cols),
                ]
            )

            for model_name, model in models.items():
                clf_pipeline = Pipeline(
                    [("preprocessor", preprocessor), ("clf", clone(model))]
                )

                clf_pipeline.fit(X_train, y_train)

                y_train_pred = clf_pipeline.predict(X_train)
                y_val_pred = clf_pipeline.predict(X_val)

                train_acc = round(accuracy_score(y_train, y_train_pred), 4)
                train_prec = round(
                    float(
                        precision_score(
                            y_train, y_train_pred, average="weighted", zero_division=0
                        )
                    ),
                    4,
                )
                train_rec = round(
                    float(
                        recall_score(
                            y_train, y_train_pred, average="weighted", zero_division=0
                        )
                    ),
                    4,
                )
                train_f1 = round(
                    float(
                        f1_score(y_train, y_train_pred, average="weighted", zero_division=0)
                    ),
                    4,
                )

                val_acc = round(accuracy_score(y_val, y_val_pred), 4)
                
                val_prec = round(
                    float(
                        precision_score(
                            y_val, y_val_pred, average="weighted", zero_division=0
                        )
                    ),
                    4,
                )
                val_rec = round(
                    float(
                        recall_score(
                            y_val, y_val_pred, average="weighted", zero_division=0
                        )
                    ),
                    4,
                )
                val_f1 = round(
                    float(
                        f1_score(y_val, y_val_pred, average="weighted", zero_division=0)
                    ),
                    4,
                )

                results.append(
                    {
                        "num_pipeline": num_name,
                        "cat_pipeline": cat_name,
                        "model": model_name,
                        "train_accuracy": train_acc,
                        "val_accuracy": val_acc,
                        "train_precision": train_prec,
                        "val_precision": val_prec,
                        "train_recall": train_rec,
                        "val_recall": val_rec,
                        "train_f1": train_f1,
                        "val_f1": val_f1,
                    }
                )

    return (
        DataFrame(results).sort_values(sort_by, ascending=False).reset_index(drop=True)
    )
