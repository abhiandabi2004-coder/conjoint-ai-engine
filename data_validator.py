def validate_format(df, expected_columns):

    if list(df.columns) != expected_columns:
        return False, f"Column mismatch. Expected: {expected_columns}"

    if df.isnull().sum().sum() > 0:
        return False, "Dataset contains missing values."

    if df["Respondent_ID"].duplicated().any():
        return False, "Duplicate Respondent_ID found."

    return True, "Valid format."