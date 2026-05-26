import pandas as pd

try:
    from validator import validate_email
except ModuleNotFoundError:
    from src.validator import validate_email


def separate_invalid_emails(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Split rows into valid email rows and invalid email rows."""
    if "email" not in df.columns:
        valid_df = df.iloc[0:0].copy()
        invalid_df = df.copy()
        invalid_df["rejection_reason"] = "missing_email_column"
        return valid_df, invalid_df

    email_is_valid = df["email"].apply(validate_email)

    valid_df = df[email_is_valid].copy()
    invalid_df = df[~email_is_valid].copy()
    invalid_df["rejection_reason"] = "invalid_email"

    return valid_df, invalid_df


def separate_duplicates(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Keep the first copy and reject extra duplicate rows."""
    if df.empty:
        return df.copy(), df.copy()

    columns_to_check = [column for column in df.columns if column != "id"]

    processed_df = df.drop_duplicates(subset=columns_to_check, keep="first").copy()
    duplicate_df = df[df.duplicated(subset=columns_to_check, keep="first")].copy()
    duplicate_df["rejection_reason"] = "duplicate_row"

    return processed_df, duplicate_df


def clean_users(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, int]]:
    """Run all cleaning rules and return processed rows, rejected rows, and report data."""
    valid_email_df, invalid_email_df = separate_invalid_emails(df)
    processed_df, duplicate_df = separate_duplicates(valid_email_df)
    rejected_df = pd.concat([invalid_email_df, duplicate_df], ignore_index=True)

    report = {
        "input_row_count": len(df),
        "valid_email_rows_before_duplicates": len(valid_email_df),
        "invalid_email_count": len(invalid_email_df),
        "duplicate_rejected_count": len(duplicate_df),
        "processed_row_count": len(processed_df),
        "rejected_row_count": len(rejected_df),
    }

    return processed_df, rejected_df, report
