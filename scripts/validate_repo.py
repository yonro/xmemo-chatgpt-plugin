#!/usr/bin/env python3
"""Validate the public XMemo OpenAI plugin repository without third-party packages."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "xmemo"
MANIFEST = PLUGIN / ".codex-plugin" / "plugin.json"
MARKETPLACE = ROOT / ".agents" / "plugins" / "marketplace.json"
SUBMISSION = ROOT / "submission" / "chatgpt-app-submission.json"
EXPECTED_SCHEMA = "https://developers.openai.com/apps-sdk/schemas/chatgpt-app-submission.v1.json"
SEMVER = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")
SECRET_PATTERNS = {
    "OpenAI key": re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    "GitHub token": re.compile(r"gh[opsu]_[A-Za-z0-9]{20,}"),
    "Private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "Reviewer password": re.compile(r"(?i)reviewer.{0,32}password\s*[:=]"),
}


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise AssertionError(f"Invalid JSON: {path.relative_to(ROOT)}: {exc}") from exc


def require_file(path: Path) -> None:
    assert path.is_file(), f"Missing file: {path.relative_to(ROOT)}"


def validate_manifest() -> str:
    manifest = load_json(MANIFEST)
    assert manifest.get("name") == "xmemo", "Plugin name must remain 'xmemo'"
    version = manifest.get("version", "")
    assert SEMVER.fullmatch(version), "Plugin version must be strict semver"
    assert manifest.get("mcpServers") == "./.mcp.json"
    assert manifest.get("skills") == "./skills/"
    interface = manifest.get("interface", {})
    assert interface.get("displayName") == "XMemo"
    prompts = interface.get("defaultPrompt", [])
    assert 1 <= len(prompts) <= 3
    assert all(isinstance(prompt, str) and len(prompt) <= 128 for prompt in prompts)
    for key in ("composerIcon", "logo", "logoDark"):
        require_file(PLUGIN / interface[key].removeprefix("./"))
    for screenshot in interface.get("screenshots", []):
        assert screenshot.endswith(".png")
        require_file(PLUGIN / screenshot.removeprefix("./"))
    return version


def validate_mcp() -> None:
    config = load_json(PLUGIN / ".mcp.json")
    server = config.get("mcpServers", {}).get("xmemo", {})
    assert server == {"type": "http", "url": "https://xmemo.dev/mcp"}, (
        "The packaged MCP config must contain only the production XMemo HTTP endpoint"
    )


def validate_marketplace() -> None:
    marketplace = load_json(MARKETPLACE)
    matches = [item for item in marketplace.get("plugins", []) if item.get("name") == "xmemo"]
    assert len(matches) == 1
    entry = matches[0]
    assert entry.get("source", {}).get("path") == "./plugins/xmemo"
    assert entry.get("policy") == {"installation": "AVAILABLE", "authentication": "ON_INSTALL"}


def validate_submission() -> None:
    submission = load_json(SUBMISSION)
    assert submission.get("$schema") == EXPECTED_SCHEMA
    assert submission.get("schema_version") == 1
    assert len(submission.get("tools", {})) == 20
    assert len(submission.get("test_cases", [])) == 5
    assert len(submission.get("negative_test_cases", [])) == 3


def scan_secrets() -> None:
    ignored_parts = {".git", "dist", "build", "__pycache__"}
    text_suffixes = {".json", ".md", ".py", ".ps1", ".yml", ".yaml", ".txt", ".toml"}
    findings: list[str] = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or ignored_parts.intersection(path.parts) or path.suffix.lower() not in text_suffixes:
            continue
        if path.resolve() == Path(__file__).resolve():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for label, pattern in SECRET_PATTERNS.items():
            if pattern.search(text):
                findings.append(f"{label}: {path.relative_to(ROOT)}")
    assert not findings, "Potential secrets found:\n" + "\n".join(findings)


def main() -> int:
    for required in (MANIFEST, MARKETPLACE, SUBMISSION, ROOT / "README.md", ROOT / "LICENSE"):
        require_file(required)
    version = validate_manifest()
    validate_mcp()
    validate_marketplace()
    validate_submission()
    scan_secrets()
    print(f"OK: XMemo plugin repository v{version} is structurally valid and secret scan is clean.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
