#!/usr/bin/env python3
"""Install the ECC Codex migration into a local Codex home."""

from __future__ import annotations

import argparse
import json
import shutil
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def copytree_replace(src: Path, dst: Path, backup_root: Path | None = None) -> None:
    if dst.exists():
        if backup_root:
            backup_root.mkdir(parents=True, exist_ok=True)
            shutil.copytree(dst, backup_root / dst.name, symlinks=True)
        shutil.rmtree(dst)
    shutil.copytree(src, dst, symlinks=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", type=Path, default=Path.home() / ".codex")
    parser.add_argument("--no-backup", action="store_true")
    args = parser.parse_args()

    target = args.target.expanduser().resolve()
    skills_src = ROOT / "skills"
    skills_dst = target / "skills"
    skills_dst.mkdir(parents=True, exist_ok=True)

    stamp = time.strftime("%Y%m%d_%H%M%S")
    backup_root = None if args.no_backup else skills_dst / ".ecc-codex-backups" / stamp

    skill_count = 0
    for skill_dir in sorted(p for p in skills_src.iterdir() if p.is_dir()):
        if not (skill_dir / "SKILL.md").exists():
            continue
        copytree_replace(skill_dir, skills_dst / skill_dir.name, backup_root)
        skill_count += 1

    plugin_dst = target / ".tmp/plugins/ecc-codex"
    plugin_dst.mkdir(parents=True, exist_ok=True)
    for rel in [
        ".codex-plugin",
        ".agents/plugins",
        ".codex",
        ".mcp.json",
        "AGENTS.md",
        "Docs/migrated",
        "skills",
        "agents",
        "commands",
        "rules",
        "hooks",
    ]:
        src = ROOT / rel
        dst = plugin_dst / rel
        if src.is_dir():
            copytree_replace(src, dst)
        elif src.is_file():
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)

    manifest = json.loads((ROOT / "Docs/migrated/migration-manifest.json").read_text())
    marker = {
        "installed_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "source": manifest["source"],
        "repository": str(ROOT),
        "skills": skill_count,
        "plugin_path": str(plugin_dst),
        "backup_root": str(backup_root) if backup_root else None,
    }
    (target / "ecc-codex-install.json").write_text(json.dumps(marker, indent=2, ensure_ascii=False) + "\n")

    print(f"installed ECC Codex skills: {skill_count}")
    print(f"target: {target}")
    print(f"plugin copy: {plugin_dst}")
    if backup_root:
        print(f"backups: {backup_root}")


if __name__ == "__main__":
    main()
