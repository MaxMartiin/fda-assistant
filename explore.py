import json
from pathlib import Path

raw_file = sorted(Path("data/raw").glob("labels_*.json"))[-1]
records = json.loads(raw_file.read_text(encoding="utf-8"))["response"]["results"]

no_openfda = [
    r for r in records if not r.get("openfda")
]  # catches a missing block AND an empty {}
print(len(no_openfda), "labels with no openfda block")

sample = no_openfda[0]
print(sorted(sample.keys()))
print(sample.get("spl_product_data_elements", "")[:200])
print(sample.get("package_label_principal_display_panel", "")[:200])
