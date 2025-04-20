import os
from string import Template
from collections import defaultdict
from pathlib import Path
import typer
from typing import Annotated, NamedTuple
from models import read_csv, ReleaseAsset


PACKAGE_NAME = "flash-attn"


class Variant(NamedTuple):
    cuda: str
    torch: str
    cxx: str


PACKAGE_INDEX = Template("""
<html>
<head></head>
<body>
<h1>$HEADER</h1>
$LINKS
</body>
</html>
""")


def create_package_whl_index(variant: Variant, assets: list[ReleaseAsset]) -> str:
    header = f"flash-attn: Python wheels for CUDA {variant.cuda} + {variant.torch} + {variant.cxx}"
    links = []
    for asset in assets:
        links.append(f'<a href="{asset.download_url}">{asset.name}</a><br>')
    all_links = os.linesep.join(links)

    return PACKAGE_INDEX.substitute(HEADER=header, LINKS=all_links)


def generate_header_for_path(path: Path, root_path: Path) -> str:
    relative_path = path.relative_to(root_path)
    parts = relative_path.parts
    assert len(parts) <= 3
    if len(parts) == 0:
        return "flash-attn: Python wheels"
    elif len(parts) == 1:
        return f"flash-attn: Python wheels for CUDA {parts[0]}"
    elif len(parts) == 2:
        return f"flash-attn: Python wheels for CUDA {parts[0]} + {parts[1]}"
    else:
        return f"flash-attn: Python wheels for CUDA {parts[0]} + {parts[1]}"


def generate_links(dirs: list[Path]) -> str:
    names = sorted([dir_path.name for dir_path in dirs])
    return os.linesep.join(f'<a href="{name}">{name}</a><br>' for name in names)


def create_root_indexes(asset_paths: list[Path], root_path: Path):
    for asset_path in asset_paths:
        dirs = [path for path in asset_path.iterdir() if path.is_dir()]
        header = generate_header_for_path(asset_path, root_path)
        links = generate_links(dirs)
        index_path = asset_path / "index.html"

        index_content = PACKAGE_INDEX.substitute(HEADER=header, LINKS=links)
        index_path.write_text(index_content)


def create_indexes(
    root_path: Path, structured_assets: dict[Variant, list[ReleaseAsset]]
):
    root_path.mkdir(exist_ok=True, parents=True)
    # create folders
    asset_paths = set()
    asset_paths.add(root_path)

    for variant, assets in structured_assets.items():
        new_folder = (
            root_path / variant.cuda / variant.torch / variant.cxx / PACKAGE_NAME
        )
        new_folder.mkdir(exist_ok=True, parents=True)
        index_path = new_folder / "index.html"

        index_path.write_text(create_package_whl_index(variant, assets))

        asset_paths.add(root_path / variant.cuda)
        asset_paths.add(root_path / variant.cuda / variant.torch)
        asset_paths.add(root_path / variant.cuda / variant.torch / variant.cxx)

    create_root_indexes(list(asset_paths), root_path)


def main(
    csv_file: Path, out: Annotated[Path, typer.Option(file_okay=False, dir_okay=True)]
):
    assets = read_csv(csv_file)

    structured_assets = defaultdict(list)
    for asset in assets:
        if asset.cuda is None or asset.torch is None or asset.cxx is None:
            continue
        if asset.cuda == "" or asset.torch == "" or asset.cxx == "":
            continue

        structured_assets[
            Variant(cuda=asset.cuda, torch=asset.torch, cxx=asset.cxx)
        ].append(asset)

    create_indexes(out, structured_assets)


if __name__ == "__main__":
    typer.run(main)
