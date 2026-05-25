# ECC Codex Migration

This repository is a Codex-ready migration of [ECC](https://github.com/affaan-m/ECC), the harness-native operator system for agentic work.

## Credit

Original project: **ECC** by **Affaan Mustafa** and contributors.

- Upstream repository: <https://github.com/affaan-m/ECC>
- Upstream homepage: <https://ecc.tools>
- Upstream license: MIT, preserved in this repository
- Migration target: OpenAI Codex local skills/config/plugin usage

This repository keeps the upstream directory tree as intact as possible and adds only Codex migration, installation, and validation files needed for local Codex use.

## What Was Migrated

- `skills/` is the primary Codex skill surface. It currently contains 233 `SKILL.md` skills copied from upstream ECC.
- `.codex/` and `.codex-plugin/` are preserved from upstream as Codex-native configuration and plugin metadata.
- `AGENTS.md` and `.codex/AGENTS.md` are preserved as Codex instruction entry points.
- `agents/`, `commands/`, `rules/`, `hooks/`, `scripts/`, and docs are preserved for traceability and future adaptation.
- `Docs/migrated/` records the migration manifest, source HEAD, source origin, and path mapping.

## Local Install

Install into the local Codex home:

```bash
python3 scripts/codex/install_ecc_codex.py --target "$HOME/.codex"
```

Verify the migration and installed files:

```bash
python3 scripts/codex/verify_ecc_codex.py --target "$HOME/.codex"
```

The installer is conservative:

- It copies all `skills/*` directories into `$HOME/.codex/skills/`.
- Existing target skill directories are backed up under `$HOME/.codex/skills/.ecc-codex-backups/<timestamp>/` before replacement.
- It installs plugin metadata under `$HOME/.codex/.tmp/plugins/ecc-codex/` for local inspection/use.
- It writes `$HOME/.codex/ecc-codex-install.json` with source HEAD, counts, and timestamp.
- It does not overwrite `$HOME/.codex/config.toml` automatically.

## Validation

The migration verifier checks:

- Required Codex files exist: `AGENTS.md`, `.codex/config.toml`, `.codex-plugin/plugin.json`, `Docs/migrated/migration-manifest.json`.
- Every skill directory under `skills/` has a non-empty `SKILL.md`.
- Skill frontmatter has `name` and `description` when frontmatter is present.
- Migration manifest counts match the current tree.
- Optional installed target contains the expected skill count and install marker.

## Notes

Codex does not currently expose the same hook event model as Claude Code. Upstream `hooks/` are therefore preserved as reference artifacts, not enabled as Codex runtime hooks. Commands are also preserved as reference/instruction shims; Codex usage should prefer skills and `AGENTS.md` guidance.
