#!/usr/bin/env python3
"""Validate and build a deterministic public plugin ZIP from approved file types."""
from __future__ import annotations

import sys
import zipfile
from pathlib import Path

from validate_repo import ROOT, package_files, validate_repository


def build(root: Path = ROOT, expected_version: str | None = None) -> Path:
    version = validate_repository(root)
    expected = expected_version.removeprefix("v") if expected_version else version
    if expected != version:
        raise ValueError(f"Version mismatch: tag/request={expected}, manifest={version}")
    plugin = root / "plugins/xmemo"
    # Read all approved inputs before creating an artifact so validation failures
    # cannot leave a partial ZIP advertised as this release.
    contents = [(path.relative_to(plugin).as_posix(), path.read_bytes()) for path in package_files(plugin)]
    output_dir = root / "dist"
    output_dir.mkdir(exist_ok=True)
    output = output_dir / f"xmemo-plugin-v{version}.zip"
    temporary = output.with_suffix(".zip.tmp")
    try:
        with zipfile.ZipFile(temporary, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
            for name, content in contents:
                info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o100644 << 16
                archive.writestr(info, content)
        temporary.replace(output)
    finally:
        temporary.unlink(missing_ok=True)
    return output


def main() -> int:
    print(build(expected_version=sys.argv[1] if len(sys.argv) > 1 else None))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
