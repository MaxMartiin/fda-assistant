import json
from datetime import datetime, timezone
from pathlib import Path

import httpx

URL = "https://api.fda.gov/drug/label.json"
PARAMS = {"limit": 100}


def main():
    fetched_at = datetime.now(timezone.utc)
    response = httpx.get(URL, params=PARAMS, timeout=30)
    response.raise_for_status()  # 4xx/5xx = crash loudly, don't save junk
    data = response.json()

    out_dir = Path("data/raw")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = (
        out_dir / f"labels_{fetched_at:%Y%m%dT%H%M%SZ}.json"
    )  # new file every fetch, never overwrite

    wrapper = {
        "source_url": str(response.url),
        "fetched_at": fetched_at.isoformat(),
        "response": data,
    }
    out_file.write_text(json.dumps(wrapper), encoding="utf-8")
    print(
        f"Saved {len(data['results'])} labels "
        f"(of {data['meta']['results']['total']:,} total) to {out_file}"
    )


if (
    __name__ == "__main__"
):  # run main() only when the file is run directly, not when it's imported
    main()
