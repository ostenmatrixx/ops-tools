from io import StringIO
from pathlib import Path

import pandas as pd


def clean_csv_file(
    source_path: Path,
    deduplicate: bool = True,
    drop_empty_rows: bool = True,
    trim_strings: bool = True,
) -> Path:
    df = pd.read_csv(source_path)

    if trim_strings:
        obj_cols = df.select_dtypes(include=["object"]).columns
        for col in obj_cols:
            df[col] = df[col].astype(str).str.strip()

    if drop_empty_rows:
        df = df.dropna(how="all")

    if deduplicate:
        df = df.drop_duplicates()

    output_path = source_path.with_name(f"{source_path.stem}_cleaned.csv")
    df.to_csv(output_path, index=False)
    return output_path


def clean_csv_text(csv_text: str, **kwargs) -> str:
    df = pd.read_csv(StringIO(csv_text))

    if kwargs.get("trim_strings", True):
        obj_cols = df.select_dtypes(include=["object"]).columns
        for col in obj_cols:
            df[col] = df[col].astype(str).str.strip()

    if kwargs.get("drop_empty_rows", True):
        df = df.dropna(how="all")

    if kwargs.get("deduplicate", True):
        df = df.drop_duplicates()

    output = StringIO()
    df.to_csv(output, index=False)
    return output.getvalue()
