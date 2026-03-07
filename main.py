import argparse
import csv
import os
from datetime import datetime, date
from typing import List, Set


def detect_type(raw_value: str) -> str:
    value = raw_value.strip()
    if value == "":
        return "empty"

    lower = value.lower()
    if lower in {"true", "false", "yes", "no"}:
        return "bool"

    try:
        int(value)
        return "int"
    except ValueError:
        pass

    try:
        float(value)
        return "float"
    except ValueError:
        pass

    datetime_formats = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%d-%m-%Y %H:%M:%S",
        "%d-%m-%Y %H:%M",
        "%m/%d/%Y %H:%M:%S",
        "%m/%d/%Y %H:%M",
    ]
    date_formats = [
        "%Y-%m-%d",
        "%d-%m-%Y",
        "%m/%d/%Y",
    ]

    for fmt in datetime_formats:
        try:
            datetime.strptime(value, fmt)
            return "datetime"
        except ValueError:
            pass

    for fmt in date_formats:
        try:
            datetime.strptime(value, fmt)
            return "date"
        except ValueError:
            pass

    return "string"


def merge_types(type_set: Set[str]) -> str:
    if not type_set:
        return "empty"
    if len(type_set) == 1:
        return next(iter(type_set))

    if type_set <= {"int", "float"}:
        return "float"

    ordered = sorted(type_set)
    return f"mixed({', '.join(ordered)})"


def print_report(csv_path: str) -> None:
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"File not found: {csv_path}")

    file_name = os.path.basename(csv_path)
    file_size = os.path.getsize(csv_path)

    with open(csv_path, newline="", encoding="utf-8-sig") as handle:
        reader = csv.reader(handle)
        try:
            headers = next(reader)
        except StopIteration:
            print(f"File name: {file_name}")
            print(f"File size (bytes): {file_size}")
            print("Rows (excluding header): 0")
            print("Columns: 0")
            print("Headers: []")
            print("Note: Empty CSV file.")
            return

        col_count = len(headers)
        type_sets: List[Set[str]] = [set() for _ in headers]
        null_counts = [0 for _ in headers]
        non_null_counts = [0 for _ in headers]
        distinct_values = [set() for _ in headers]
        row_count = 0
        bad_row_count = 0

        for row in reader:
            row_count += 1

            if len(row) != col_count:
                bad_row_count += 1
                if len(row) < col_count:
                    row = row + [""] * (col_count - len(row))
                else:
                    row = row[:col_count]

            for idx, raw_value in enumerate(row):
                value = raw_value.strip()
                if value == "":
                    null_counts[idx] += 1
                    continue

                non_null_counts[idx] += 1
                distinct_values[idx].add(value)
                type_sets[idx].add(detect_type(value))

    print(f"File name: {file_name}")
    print(f"File size (bytes): {file_size}")
    print(f"Rows (excluding header): {row_count}")
    print(f"Columns: {col_count}")
    print(f"Headers: {headers}")

    if bad_row_count > 0:
        print(f"Rows with mismatched column count: {bad_row_count}")

    print("\nColumn profile:")
    for idx, header in enumerate(headers):
        inferred = merge_types(type_sets[idx])
        print(
            f"- {header}: type={inferred}, non_null={non_null_counts[idx]}, "
            f"null={null_counts[idx]}, distinct={len(distinct_values[idx])}"
        )

    print("\nSuggestions:")
    print("- Check columns with high null counts before analysis.")
    print("- Review columns with mixed(...) types for data-cleaning.")
    print("- Add validation rules (required columns/ranges/formats) for production use.")


def main() -> None:
    parser = argparse.ArgumentParser(description="CSV quick profiler")
    parser.add_argument("csv_file", help="Path to the CSV file")
    args = parser.parse_args()
    print_report(args.csv_file)


if __name__ == "__main__":
    main()


