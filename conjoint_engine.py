import pandas as pd
from sklearn.linear_model import LinearRegression, LogisticRegression

def run_conjoint(data, analysis_type):

    X = data["X"]
    y = data["y"]

    # Auto Detect
    if analysis_type == "Auto Detect":
        if y.nunique() <= 2:
            analysis_type = "Choice Based"
        else:
            analysis_type = "Rating Based"

    if analysis_type == "Choice Based":
        model = LogisticRegression(max_iter=1000)
    else:
        model = LinearRegression()

    model.fit(X, y)

    utilities = pd.Series(model.coef_, index=X.columns)

    importance = calculate_importance(utilities)

    return {
        "utilities": utilities,
        "importance": importance,
        "model_type": analysis_type
    }


def calculate_importance(utilities):

    grouped = utilities.abs().groupby(
        lambda x: x.split("_")[0]
    ).sum()

    importance = 100 * grouped / grouped.sum()

    return importance