"""Top-level command-line router for condastats."""

import sys

from condastats import cli_flags, cli_legacy

_PREVIEW_FLAG = "--preview"


def _is_preview_mode(argv: list[str]) -> bool:
    """Return True when the preview flag is present before the subcommand."""
    for arg in argv:
        if arg == "--":
            return False
        if arg == _PREVIEW_FLAG:
            return True
        if not arg.startswith("-"):
            return False
    return False


def _strip_preview_flag(argv: list[str]) -> list[str]:
    """Remove preview routing flags before delegating to the preview CLI."""
    return [arg for arg in argv if arg != _PREVIEW_FLAG]


def main(argv: list[str] | None = None) -> int:
    """Entry point for the condastats CLI."""
    argv = list(sys.argv[1:] if argv is None else argv)

    if _is_preview_mode(argv):
        return cli_flags.main(_strip_preview_flag(argv))

    return cli_legacy.main(argv)


if __name__ == "__main__":
    sys.exit(main())
