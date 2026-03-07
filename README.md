# CSV Reader / Profiler

Quick CSV summary tool that prints:
- File name and file size
- Number of rows and columns
- Column headers
- Inferred column data types (best effort)
- Per-column null/non-null/distinct counts
- Basic data-quality suggestions

## Usage

```bash
python main.py <path-to-csv>
```

Example:

```bash
python main.py sample.csv
```
