from pathlib import Path
import re
from itertools import chain
from typing import Annotated, Optional
import typer
from packaging.version import parse
from typer import Argument
from github import Github, Auth
from github import GitReleaseAsset
from github import GitRelease
from models import ReleaseAsset, read_csv, write_assets

GITHUB_REPO = "Dao-AILab/flash-attention"


release_re = re.compile(
    r"^flash_attn-([\w\.]*)\+(?P<cuda>cu[\d]+)(?P<torch>torch[\d\.]+)"
    r"(?P<cxx>cxx11abi(FALSE|TRUE))-(?P<python>\w+)"
)


def process_asset(
    asset: GitReleaseAsset.GitReleaseAsset, version: str
) -> Optional[ReleaseAsset]:
    name = asset.name
    matches = release_re.match(name)
    if not matches:
        return None
    download_url = {
        "download_url": asset.browser_download_url,
        "name": name,
        "version": version,
    }
    return ReleaseAsset(**matches.groupdict(), **download_url)


def process_release(release: GitRelease.GitRelease) -> list[ReleaseAsset]:
    out = [
        meta
        for asset in release.assets
        if (meta := process_asset(asset, release.tag_name)) is not None
    ]
    if not out:
        return [ReleaseAsset(version=release.tag_name)]

    return out


def main(
    out: Path,
    github_token: Annotated[str, Argument(envvar="_GITHUB_TOKEN")],
    update_latest: int = 3,
):
    cached_assets = read_csv(out)

    auth = Auth.Token(github_token)
    g = Github(auth=auth)
    repo = g.get_repo(GITHUB_REPO)
    releases = repo.get_releases()

    # Get releases to update
    released_versions = {release.tag_name: release for release in releases}
    cached_versions = set(asset.version for asset in cached_assets)
    newest_releases = set(sorted(released_versions, key=parse)[-update_latest:])
    versions_to_updated = (set(released_versions) - cached_versions) | newest_releases

    releases_to_update = [released_versions[version] for version in versions_to_updated]

    print(f"Updating: {versions_to_updated}")

    release_assets = list(
        chain.from_iterable(process_release(release) for release in releases_to_update)
    )
    new_cached_assets = [
        asset for asset in cached_assets if asset.version not in versions_to_updated
    ]
    all_assets = release_assets + new_cached_assets

    print(f"Writing assets to {out}")
    write_assets(out, all_assets)


if __name__ == "__main__":
    typer.run(main)
