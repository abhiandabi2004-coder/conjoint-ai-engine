import pandas as pd

def process_data(df, target_column):

    X = df.drop(columns=["Respondent_ID", target_column])
    y = df[target_column]

    # One-hot encode categorical attributes
    X_encoded = pd.get_dummies(X, drop_first=True)

    return {
        "X": X_encoded,
        "y": y,
        "original_attributes": X.columns
    }