import openpyxl

wb = openpyxl.load_workbook(
    r"C:\Users\israe\Downloads\securelocksmithsolution.com-Coverage-2026-08-19.xlsx",
    read_only=True,
)
for ws in wb.worksheets:
    print(f"=== SHEET: {ws.title} ===")
    for i, row in enumerate(ws.iter_rows(values_only=True)):
        print(" | ".join("" if c is None else str(c) for c in row))
        if i > 120:
            print("... truncated ...")
            break
