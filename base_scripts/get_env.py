from pathlib import Path

tildagon_env = dict(
    [
        x.split("=")
        for x in (
            Path(Path.home(), ".config", "emf", "tildagon")
            .read_text(encoding="utf-8")
            .strip()
            .splitlines()
        )
    ]
)
