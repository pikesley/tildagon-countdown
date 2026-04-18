import os

apps = os.listdir("/apps")
path = ""
ASSET_PATH = "apps"

if "%CODEBERG_USER%_tildagon_%APP_NAME%" in apps:
    ASSET_PATH = "/apps/%CODEBERG_USER%_tildagon_%APP_NAME%/"

if "%APP_NAME%" in apps:
    ASSET_PATH = "apps/%APP_NAME%/"
