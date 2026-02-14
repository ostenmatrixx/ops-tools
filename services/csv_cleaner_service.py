import csv
from io import StringIO
from pathlib import Path


def clean_csv_file(
    source_path: Path,
    deduplicate: bool = True,
    drop_empty_rows: bool = True,
    trim_strings: bool = True,
) -> Path:
    with source_path.open("r", encoding="utf-8-sig", newline="") as f:
        cleaned_csv = clean_csv_text(
            f.read(),
            deduplicate=deduplicate,
            drop_empty_rows=drop_empty_rows,
            trim_strings=trim_strings,
        )

    output_path = source_path.with_name(f"{source_path.stem}_cleaned.csv")
    output_path.write_text(cleaned_csv, encoding="utf-8", newline="")
    return output_path


def clean_csv_text(csv_text: str, **kwargs) -> str:
    trim_strings = kwargs.get("trim_strings", True)
    drop_empty_rows = kwargs.get("drop_empty_rows", True)
    deduplicate = kwargs.get("deduplicate", True)

    source = StringIO(csv_text)
    reader = csv.DictReader(source)
    fieldnames = reader.fieldnames or []

    cleaned_rows = []
    seen = set()

    for row in reader:
        normalized = {}
        for key in fieldnames:
            value = row.get(key, "")
            if value is None:
                value = ""
            if trim_strings:
                value = value.strip()
            normalized[key] = value

        if drop_empty_rows and all((normalized.get(k, "") == "") for k in fieldnames):
            continue

        if deduplicate:
            row_key = tuple(normalized.get(k, "") for k in fieldnames)
            if row_key in seen:
                continue
            seen.add(row_key)

        cleaned_rows.append(normalized)

    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()
    writer.writerows(cleaned_rows)
    return output.getvalue()
