from pathlib import Path

from base_scripts.get_env import tildagon_env

lines = Path("templates", "asset_path.py").read_text(encoding="utf-8").splitlines()
lookups = {
    "%CODEBERG_USER%": tildagon_env["CODEBERG_USER"],
    "%APP_NAME%": Path(__file__).parent.parent.stem,
}

fixed_lines = []

for line in lines:
    fixed_line = line
    for placeholder, replacement in lookups.items():
        fixed_line = fixed_line.replace(placeholder, replacement)

    fixed_lines.append(fixed_line)

Path("base", "asset_path.py").write_text("\n".join(fixed_lines))
