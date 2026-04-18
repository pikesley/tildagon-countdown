import sys
import tomllib
from pathlib import Path

import requests
from git import Repo

repo = Repo(".")
subpath = "/".join(repo.remote().url.split("/")[-2:])[:-4]

base_url = "https://codeberg.org/api/v1/repos/"

releases_url = base_url + subpath + "/releases"

env = (
    Path(Path.home(), ".config", "emf", "tildagon")
    .read_text(encoding="utf-8")
    .strip()
    .splitlines()
)
env_vars = dict([x.split("=") for x in env])
token = env_vars["CODEBERG_TOKEN"]

headers = {"Authorization": f"token {token}"}

releases = requests.get(
    releases_url,
    timeout=10,
)

existing_releases = [x["tag_name"] for x in releases.json()]
proposed_release = tomllib.loads(Path("tildagon.toml").read_text())["metadata"][
    "version"
]

if proposed_release in existing_releases:
    print(f"Release {proposed_release} already exists. Did you update `tildagon.toml`?")
    sys.exit(127)

data = {
    "tag_name": proposed_release,
    "name": proposed_release,
}

print(f"Creating release `{proposed_release}`")
create = requests.post(
    releases_url,
    headers=headers,
    json=data,
    timeout=10,
)

print("Done")
print(create.json()["url"])
