#!/usr/bin/env python3
"""Check documented OpenAI package constraints, not portal approval or runtime parity."""
from __future__ import annotations

import json
import re
import sys
import unicodedata
from pathlib import Path, PurePosixPath
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
PUBLISHED_NAME = "app-6a112deb1d4881919bde555b7c16b24b"
EXPECTED_SCHEMA = "https://developers.openai.com/apps-sdk/schemas/chatgpt-app-submission.v1.json"
SEMVER = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")
SECRET_PATTERNS = {
    "OpenAI key": re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    "GitHub token": re.compile(r"gh[opsu]_[A-Za-z0-9]{20,}"),
    "Private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "Reviewer password": re.compile(r"(?i)reviewer.{0,32}password\s*[:=]"),
}
EXPECTED_SKILLS = {
    "xmemo-memory-steward", "xmemo-brainstorm", "xmemo-plan-project",
    "xmemo-review-plan", "xmemo-audit-progress", "xmemo-distill-session",
    "xmemo-resume-work", "xmemo-handoff-work",
}
UNSUPPORTED_OPENAI_TOOLS = {"get_project_context", "create_pending_decision", "resolve_decision"}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def load_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), f"Expected JSON object: {path}")
    return value


def package_path(plugin: Path, relative: str) -> Path:
    require(isinstance(relative, str) and relative.startswith("./"), "Package paths must start with ./")
    raw = relative[2:]
    parts = PurePosixPath(raw).parts
    require(bool(parts) and not raw.startswith("/") and "\\" not in raw and ":" not in raw
            and all(part not in {".", ".."} for part in parts), "Unsafe package path")
    current = plugin
    require(not current.is_symlink(), "Plugin root must not be a symlink")
    for part in parts:
        current = current / part
        require(not current.is_symlink(), "Package symlinks are forbidden")
    require(current.resolve().is_relative_to(plugin.resolve()), "Package path escapes root")
    require(current.is_file(), f"Missing package file: {relative}")
    return current


def text_field(value: object, limit: int, label: str, single_line: bool = True) -> None:
    require(isinstance(value, str) and bool(value.strip()) and len(value) <= limit, f"Invalid {label}")
    require(not single_line or not any(c in value for c in "\r\n"), f"{label} must be one line")


def https_url(value: object, label: str) -> None:
    text_field(value, 1024, label)
    try:
        parsed = urlsplit(value)
        valid = parsed.scheme == "https" and bool(parsed.hostname) and not parsed.username and not parsed.password
    except ValueError:
        valid = False
    require(bool(valid), f"{label} must be a credential-free HTTPS URL")


def reject_auth_overrides(value: object) -> None:
    """This package updates an app whose authentication is managed in Platform."""
    if isinstance(value, dict):
        require(not {"auth", "authentication"}.intersection(value),
                "Keep the existing MCP connection: remove ZIP auth overrides; manage authentication in the existing app")
        for child in value.values():
            reject_auth_overrides(child)
    elif isinstance(value, list):
        for child in value:
            reject_auth_overrides(child)


def validate_manifest(plugin: Path) -> dict:
    manifest = load_json(package_path(plugin, "./.codex-plugin/plugin.json"))
    reject_auth_overrides(manifest)
    require(manifest.get("name") == PUBLISHED_NAME, "Preserve the published plugin package identity")
    require(bool(SEMVER.fullmatch(str(manifest.get("version", "")))), "Version must be strict semver")
    require(manifest.get("mcpServers") == "./.mcp.json", "Unexpected MCP config path")
    require(manifest.get("skills") == "./skills/", "Unexpected skills directory")
    require(not any(key in manifest for key in ("hooks", "apps")), "Public upload forbids hooks and app references")
    require(not any((plugin / path).exists() for path in ("hooks", ".app.json", "plugin.json", "mcp.json")),
            "Do not mix incompatible or duplicate package entry points")
    interface = manifest.get("interface", {})
    for key, limit in (("displayName", 30), ("shortDescription", 30), ("longDescription", 4000), ("developerName", 80)):
        text_field(interface.get(key), limit, key, single_line=key != "longDescription")
    require(interface.get("category") == "Productivity", "Unexpected listing category")
    for key in ("websiteURL", "supportURL", "privacyPolicyURL", "termsOfServiceURL"):
        https_url(interface.get(key), key)
    capabilities = interface.get("capabilities", [])
    require(isinstance(capabilities, list) and len(capabilities) <= 20, "Invalid capabilities")
    for capability in capabilities:
        text_field(capability, 120, "capability")
    prompts = interface.get("defaultPrompt", [])
    require(isinstance(prompts, list) and 1 <= len(prompts) <= 3, "Expected one to three starter prompts")
    normalized = []
    for prompt in prompts:
        text_field(prompt, 128, "starter prompt")
        require("@" not in prompt, "Starter prompts must not mention an MCP server")
        normalized.append(" ".join(unicodedata.normalize("NFKC", prompt).split()))
    require(len(set(normalized)) == len(prompts), "Duplicate normalized starter prompts")
    for key in ("composerIcon", "composerIconDark", "logo", "logoDark"):
        if key in interface:
            package_path(plugin, interface[key])
    require("logo" in interface, "Provide a packaged logo")
    for reference in interface.get("screenshots", []):
        package_path(plugin, reference)
    return manifest


def validate_mcp(plugin: Path) -> None:
    config = load_json(package_path(plugin, "./.mcp.json"))
    reject_auth_overrides(config)
    expected = {"mcpServers": {"xmemo": {
        "type": "http", "url": "https://xmemo.dev/mcp"}}}
    require(config == expected, "Preserve the existing MCP endpoint without auth overrides, headers, or connection changes")


def validate_skills(plugin: Path) -> None:
    skills = plugin / "skills"
    require({path.name for path in skills.iterdir() if path.is_dir()} == EXPECTED_SKILLS, "Unexpected skill set")
    for name in sorted(EXPECTED_SKILLS):
        path = package_path(plugin, f"./skills/{name}/SKILL.md")
        package_path(plugin, f"./skills/{name}/agents/openai.yaml")
        text = path.read_text(encoding="utf-8")
        parts = text.split("---", 2)
        require(len(parts) == 3 and parts[0] == "", f"Missing frontmatter: {name}")
        require(f"name: {name}" in parts[1] and "description:" in parts[1], f"Invalid skill metadata: {name}")
        require("[TODO:" not in text, f"Unresolved template: {name}")
        for tool in UNSUPPORTED_OPENAI_TOOLS:
            require(f"`{tool}`" not in text, f"Unavailable tool in {name}: {tool}")


def package_files(plugin: Path) -> list[Path]:
    """Fail closed on unexpected inputs; never silently ship local files."""
    files = []
    for path in sorted(plugin.rglob("*")):
        require(not path.is_symlink(), "Package symlinks are forbidden")
        if not path.is_file():
            continue
        relative = path.relative_to(plugin)
        parts = relative.parts
        allowed = relative.as_posix() in {".codex-plugin/plugin.json", ".mcp.json"}
        allowed |= len(parts) >= 3 and parts[0] == "skills" and parts[1] in EXPECTED_SKILLS and (
            path.suffix == ".md" or parts[2:] == ("agents", "openai.yaml"))
        allowed |= len(parts) == 2 and parts[0] == "assets" and path.suffix == ".png"
        require(allowed, f"Unexpected package input: {relative}")
        package_path(plugin, "./" + relative.as_posix())
        files.append(path)
    return files


def validate_submission(root: Path) -> None:
    """Check the historical 2026-08-01 snapshot; this is not a live contract."""
    snapshot = load_json(root / "submission/chatgpt-app-submission.json")
    require(snapshot.get("$schema") == EXPECTED_SCHEMA and snapshot.get("schema_version") == 1, "Unexpected historical submission format")
    require(len(snapshot.get("tools", {})) == 20, "Historical submission tool inventory changed")
    require(len(snapshot.get("test_cases", [])) == 5 and len(snapshot.get("negative_test_cases", [])) == 3,
            "Historical submission case inventory changed")


def scan_secrets(root: Path) -> None:
    ignored = {".git", "dist", "build", "__pycache__", ".venv"}
    for path in root.rglob("*"):
        if ignored.intersection(path.relative_to(root).parts) or path.is_symlink() or not path.is_file():
            continue
        if path.suffix.lower() not in {".json", ".md", ".py", ".ps1", ".yml", ".yaml", ".txt", ".toml"}:
            continue
        if path.resolve() == Path(__file__).resolve():
            continue
        for label, pattern in SECRET_PATTERNS.items():
            require(not pattern.search(path.read_text(encoding="utf-8", errors="ignore")),
                    f"Potential {label} in {path.relative_to(root)} (value redacted)")


def validate_repository(root: Path = ROOT) -> str:
    plugin = root / "plugins/xmemo"
    manifest = validate_manifest(plugin)
    validate_mcp(plugin)
    validate_skills(plugin)
    package_files(plugin)
    marketplace = load_json(root / ".agents/plugins/marketplace.json")
    entries = [entry for entry in marketplace.get("plugins", []) if entry.get("name") == PUBLISHED_NAME]
    require(len(entries) == 1, "Marketplace must reference the published identity exactly once")
    require(entries[0].get("source", {}).get("path") == "./plugins/xmemo", "Unexpected marketplace source")
    require(entries[0].get("policy") == {"installation": "AVAILABLE", "authentication": "ON_INSTALL"}, "Unexpected marketplace policy")
    validate_submission(root)
    scan_secrets(root)
    return manifest["version"]


def main() -> int:
    version = validate_repository()
    print(f"OK: v{version} local package constraints and historical snapshot checks passed; no credential patterns detected.")
    print("OpenAI upload checks, skill scans, OAuth/runtime and device acceptance remain separate.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
