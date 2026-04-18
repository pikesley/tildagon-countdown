from pathlib import Path


class Excluder:
    """Generate exclusions."""

    def __init__(self, app_root=""):
        """Construct."""
        self.app_root = app_root
        self.includes = Path(self.app_root, "includes").read_text().strip().splitlines()

        offset = 0
        if app_root:
            offset = 1

        self.items = sorted(
            [
                str(x)[len(self.app_root) + offset :]
                for x in sorted(Path(self.app_root).glob("*"))
            ]
        )

        self.candidates = sorted(set(self.items) - set(self.includes))

        self.filtered = filter(lambda x: not x.startswith(".git"), self.candidates)

    def __str__(self):
        """As a string."""
        return "\n".join(sorted([f"/{x} export-ignore" for x in self.filtered]))


if __name__ == "__main__":
    import sys

    includes = "includes"
    inc = Path(includes)
    if not inc.exists():
        print(f"`{includes}` needs to exist")
        sys.exit(1)

    if Path("includes").stat().st_size == 0:
        print(f"`{includes}` needs be populated")
        sys.exit(1)

    exc = Excluder()
    Path(".gitattributes").write_text(str(exc))
