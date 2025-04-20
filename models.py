from typing import Optional
from pathlib import Path
from csv import DictReader, DictWriter
from packaging.version import Version, parse

from dataclasses import dataclass, fields, asdict


@dataclass
class ReleaseAsset:
    version: str
    name: Optional[str] = None
    cuda: Optional[str] = None
    torch: Optional[str] = None
    cxx: Optional[str] = None
    python: Optional[str] = None
    download_url: Optional[str] = None


def read_csv(csv_file: Path) -> list[ReleaseAsset]:
    if not csv_file.exists():
        return []
    output = []
    with csv_file.open() as f:
        reader = DictReader(f)
        for row in reader:
            output.append(ReleaseAsset(**row))
    return output


def sort_key(asset: ReleaseAsset) -> tuple:
    return (parse(asset.version), asset.name, asset.cuda, asset.torch, asset.cxx, asset.python)


def write_assets(csv_file: Path, assets: list[ReleaseAsset]):
    assets.sort(key=sort_key, reverse=True)
    fieldnames = [field.name for field in fields(ReleaseAsset)]
    with csv_file.open("w") as f:
        writer = DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows([asdict(asset) for asset in assets])
