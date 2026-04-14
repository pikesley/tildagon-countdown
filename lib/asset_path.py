# https://tildagon.badge.emfcamp.org/tildagon-apps/reference/ctx/#adding-images
import os

apps = os.listdir("/apps")  # noqa: PTH208
path = ""
ASSET_PATH = "apps/"

if "pikesley_tildagon_countdown" in apps:
    ASSET_PATH = "/apps/pikesley_tildagon_countdown/"

if "countdown" in apps:
    ASSET_PATH = "apps/countdown/"
