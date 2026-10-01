import argparse
import json
import os
from datetime import date
from pathlib import Path

from huggingface_hub import HfApi, hf_hub_download

REPO = "thetrademarkk/india-index-options-1m"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--start", required=True)
    p.add_argument("--end", required=True)
    p.add_argument("--out", default="data/raw")
    a = p.parse_args()

    start = date.fromisoformat(a.start)
    end = date.fromisoformat(a.end)
    token = os.getenv("HF_TOKEN")
    if not token:
        raise SystemExit("HF_TOKEN is required")

    api = HfApi(token=token)
    files = api.list_repo_files(repo_id=REPO, repo_type="dataset")

    selected = []
    for name in files:
        if not name.startswith("options/NIFTY/") or not name.endswith(".parquet"):
            continue
        try:
            expiry = date.fromisoformat(Path(name).stem)
        except ValueError:
            continue
        if start <= expiry <= end:
            selected.append(name)

    if not selected:
        raise SystemExit("No NIFTY expiry files found in requested range")

    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)

    index_local = hf_hub_download(
        repo_id=REPO,
        filename="index/NIFTY.parquet",
        repo_type="dataset",
        token=token,
        local_dir=out,
    )

    downloaded = []
    for name in sorted(selected):
        local = hf_hub_download(
            repo_id=REPO,
            filename=name,
            repo_type="dataset",
            token=token,
            local_dir=out,
        )
        downloaded.append({
            "remote": name,
            "local": local,
            "size_bytes": Path(local).stat().st_size,
        })

    manifest = {
        "dataset": REPO,
        "start": a.start,
        "end": a.end,
        "index_file": index_local,
        "option_files": downloaded,
        "note": "Raw licensed data are not committed to this public repository.",
    }
    (out / "MANIFEST.json").write_text(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
