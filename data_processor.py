import pandas as pd

def process_data(df, target_column):

    # Clean columns
    df.columns = df.columns.str.strip()
    target_column = target_column.strip()

    if target_column not in df.columns:
        raise ValueError(
            f"Target column '{target_column}' not found.\n"
            f"Available columns: {list(df.columns)}"
        )

    if "Respondent_ID" not in df.columns:
        raise ValueError(
            "'Respondent_ID' column missing."
        )

    X = df.drop(columns=["Respondent_ID", target_column])
    y = df[target_column]

    X_encoded = pd.get_dummies(X, drop_first=True)

    return {
        "X": X_encoded,
        "y": y,
        "original_attributes": X.columns
    }
