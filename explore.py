import json
from pathlib import Path
from labels import first

CANDIDATES = ["spl_product_data_elements", "package_label_principal_display_panel"]
TEXT_FIELDS = [
    "indications_and_usage",
    "warnings_and_cautions",
    "warnings",
    "boxed_warning",
]


raw_file = sorted(Path("data/raw").glob("labels_*.json"))[-1]
records = json.loads(raw_file.read_text(encoding="utf-8"))["response"]["results"]

no_openfda = [
    r for r in records if not r.get("openfda")
]  # catches a missing block AND an empty {}
print(len(no_openfda), "labels with no openfda block")

print("Non-empty candidate fields in labels without openfda:")
for field in CANDIDATES:
    count = sum(bool(first(record.get(field))) for record in no_openfda)
    print(f"{field}: {count}")

print("Records with multiple values per text field:")
for field in TEXT_FIELDS:
    count = sum(
        isinstance(record.get(field), list) and len(record[field]) > 1
        for record in records
    )
    print(f"{field}: {count}")

sample = no_openfda[0]
print(sorted(sample.keys()))
print(" ".join(sample.get("spl_product_data_elements", []))[:200])
print(" ".join(sample.get("package_label_principal_display_panel", []))[:200])

print("First 120 characters of spl_product_data_elements for 3 records:")
for record in no_openfda[:3]:
    print(" ".join(record.get("spl_product_data_elements", []))[:120])
