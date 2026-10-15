from datetime import date, datetime
from pydantic import BaseModel, field_validator


class DrugLabel(BaseModel):
    set_id: str
    version: str
    effective_date: date
    brand_name: str | None
    generic_name: str | None
    manufacturer: str | None
    indications: str | None
    warnings: str | None
    boxed_warning: str | None

    @field_validator(
        "effective_date", mode="before"
    )  # runs BEFORE Pydantic checks the type
    @classmethod
    def parse_yyyymmdd(cls, value):
        return datetime.strptime(value, "%Y%m%d").date()


def first(values: list[str] | None) -> str | None:
    # this returns the first value in a list of strings, or None if the list is empty or None
    if not values:
        return None
    return values[0].strip()


def from_raw(raw: dict) -> DrugLabel:
    openfda = raw.get("openfda", {})
    return DrugLabel(
        set_id=raw["set_id"],
        version=raw["version"],
        effective_date=raw["effective_time"],
        brand_name=first(openfda.get("brand_name")),
        generic_name=first(openfda.get("generic_name")),
        manufacturer=first(openfda.get("manufacturer_name")),
        indications=first(raw.get("indications_and_usage")),
        warnings=first(raw.get("warnings_and_cautions") or raw.get("warnings")),
        boxed_warning=first(raw.get("boxed_warning")),
    )
