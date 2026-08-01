#!/usr/bin/env python3
"""Create a deterministic XMemo plugin ZIP for a matching semantic version."""

from __future__ import annotations

import json
import sys
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "xmemo"


def main() -> int:
    manifest = json.loads((PLUGIN / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
    version = manifest["version"]
    expected = sys.argv[1].removeprefix("v") if len(sys.argv) > 1 else version
    if expected != version:
        raise SystemExit(f"Version mismatch: tag/request={expected}, manifest={version}")
    output_dir = ROOT / "dist"
    output_dir.mkdir(exist_ok=True)
    output = output_dir / f"xmemo-plugin-v{version}.zip"
    files = sorted(path for path in PLUGIN.rglob("*") if path.is_file())
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in files:
            info = zipfile.ZipInfo(path.relative_to(PLUGIN).as_posix(), date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, path.read_bytes())
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
