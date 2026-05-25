#!/usr/bin/env python3
"""Verify the ECC Codex migration without upstream npm dependencies."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REQUIRED_FILES = [
    "AGENTS.md",
    ".codex/AGENTS.md",
    ".codex/config.toml",
    ".codex-plugin/plugin.json",
    "Docs/migrated/MIGRATION_INDEX.md",
    "Docs/migrated/migration-manifest.json",
]


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def parse_frontmatter(text: str) -> dict[str, str] | None:
    if text.startswith("\ufeff"):
        text = text[1:]
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end == -1:
        return None
    fields: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if not line or line.startswith(" ") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip().strip('"').strip("'")
    return fields


def verify_repo() -> tuple[int, int, int, int]:
    for rel in REQUIRED_FILES:
        path = ROOT / rel
        if not path.exists():
            fail(f"missing required file: {rel}")
        if path.is_file() and path.stat().st_size == 0:
            fail(f"empty required file: {rel}")

    manifest_path = ROOT / "Docs/migrated/migration-manifest.json"
    try:
        manifest = json.loads(manifest_path.read_text())
    except json.JSONDecodeError as exc:
        fail(f"invalid migration manifest JSON: {exc}")

    skills_root = ROOT / "skills"
    skills = sorted(p for p in skills_root.iterdir() if p.is_dir())
    skill_count = 0
    for skill_dir in skills:
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            fail(f"skill missing SKILL.md: {skill_dir.name}")
        text = skill_md.read_text(errors="replace")
        if not text.strip():
            fail(f"empty SKILL.md: {skill_dir.name}")
        frontmatter = parse_frontmatter(text)
        if frontmatter is not None:
            if not frontmatter.get("name"):
                fail(f"skill frontmatter missing name: {skill_dir.name}")
            if not frontmatter.get("description"):
                fail(f"skill frontmatter missing description: {skill_dir.name}")
        skill_count += 1

    agents = sorted((ROOT / "agents").glob("*.md"))
    commands = sorted((ROOT / "commands").glob("*.md"))
    rules = sorted((ROOT / "rules").rglob("*.md"))

    surface = manifest.get("codex_surface", {})
    expected = {
        "skills": skill_count,
        "agents": len(agents),
        "commands_reference": len(commands),
        "rules": len(rules),
    }
    for key, actual in expected.items():
        recorded = surface.get(key)
        if recorded != actual:
            fail(f"manifest {key}={recorded!r}, actual={actual}")

    plugin = json.loads((ROOT / ".codex-plugin/plugin.json").read_text())
    if not plugin.get("name"):
        fail(".codex-plugin/plugin.json missing name")
    if not plugin.get("skills"):
        fail(".codex-plugin/plugin.json missing skills path")

    print(f"repo ok: skills={skill_count} agents={len(agents)} commands={len(commands)} rules={len(rules)}")
    return skill_count, len(agents), len(commands), len(rules)


def verify_target(target: Path, expected_skills: int) -> None:
    marker = target / "ecc-codex-install.json"
    if not marker.exists():
        fail(f"install marker missing: {marker}")
    try:
        install = json.loads(marker.read_text())
    except json.JSONDecodeError as exc:
        fail(f"invalid install marker JSON: {exc}")
    if install.get("skills") != expected_skills:
        fail(f"install marker skills={install.get('skills')!r}, expected={expected_skills}")

    skills_root = target / "skills"
    installed = sorted(p for p in skills_root.iterdir() if p.is_dir() and (p / "SKILL.md").exists())
    if len(installed) < expected_skills:
        fail(f"installed skill count {len(installed)} below expected {expected_skills}")

    plugin_manifest = target / ".tmp/plugins/ecc-codex/.codex-plugin/plugin.json"
    if not plugin_manifest.exists():
        fail(f"installed plugin manifest missing: {plugin_manifest}")
    plugin_skills = target / ".tmp/plugins/ecc-codex/skills"
    if not plugin_skills.exists():
        fail(f"installed plugin skills directory missing: {plugin_skills}")
    plugin_skill_count = sum(1 for p in plugin_skills.iterdir() if p.is_dir() and (p / "SKILL.md").exists())
    if plugin_skill_count != expected_skills:
        fail(f"installed plugin skill count {plugin_skill_count}, expected {expected_skills}")
    print(f"install ok: target={target} installed_skills>={expected_skills}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", type=Path, default=None, help="Optional Codex home to verify after install.")
    args = parser.parse_args()

    skill_count, _, _, _ = verify_repo()
    if args.target:
        verify_target(args.target.expanduser().resolve(), skill_count)


if __name__ == "__main__":
    main()
