def validate_format(df, expected_columns):

    # Clean uploaded columns
    df.columns = df.columns.str.strip()

    # Clean expected columns
    expected_columns = [col.strip() for col in expected_columns]

    # Check missing columns
    missing = set(expected_columns) - set(df.columns)
    extra = set(df.columns) - set(expected_columns)

    if missing:
        return False, f"Missing columns: {missing}"

    if extra:
        return False, f"Unexpected columns: {extra}"

    return True, "Valid format."
