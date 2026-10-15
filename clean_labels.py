import json
from pathlib import Path

from pydantic import ValidationError

from labels import DrugLabel, from_raw

raw_file = sorted(Path("data/raw").glob("labels_*.json"))[
    -1
]  # newest; the timestamp format sorts correctly
wrapper = json.loads(raw_file.read_text(encoding="utf-8"))
records = wrapper["response"]["results"]
print(
    f"File: {raw_file.name} | fetched {wrapper['fetched_at']} | {len(records)} records"
)

valid, failed = [], []
for raw in records:
    try:
        valid.append(from_raw(raw))
    except (ValidationError, KeyError) as e:
        failed.append((raw.get("set_id", "?"), str(e)[:200]))

print(f"Valid: {len(valid)}   Failed: {len(failed)}")
for set_id, err in failed[:3]:
    print(f"  {set_id}: {err}")

total_count = len(valid)
for field_name in DrugLabel.model_fields:
    missing_count = sum(1 for label in valid if getattr(label, field_name) is None)
    print(f"{field_name}: {missing_count} missing out of {total_count} total")
