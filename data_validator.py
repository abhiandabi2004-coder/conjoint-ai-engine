def validate_format(df, expected_columns):

    # Clean uploaded columns
    df.columns = df.columns.str.strip()

    # Clean expected columns
    expected_columns = [col.strip() for col in expected_columns]

    # Compare as sets (ignore order)
    if set(df.columns) != set(expected_columns):
        return False, f"""
        Column mismatch.
        Expected: {expected_columns}
        Found: {list(df.columns)}
        """

    if df["Respondent_ID"].duplicated().any():
        return False, "Duplicate Respondent_ID found."

    if df.isnull().sum().sum() > 0:
        return False, "Dataset contains missing values."

    return True, "Valid format."
