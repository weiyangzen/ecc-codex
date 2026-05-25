# ECC to Codex Migration Index

This index records the deterministic migration surface used for the local Codex-ready package.

- Source repository: `https://github.com/affaan-m/ECC`
- Source origin: `git@github.com:affaan-m/ecc.git`
- Source HEAD: `1e8c7e7994223e0ff337d1626cd08e04a1ae67ed`
- Original author credit: Affaan Mustafa and ECC contributors
- License: MIT, preserved from upstream

## Migrated Surfaces

- Codex skills: `233` under `skills/`
- Agent references: `60` under `agents/`
- Command references: `75` under `commands/`
- Rule references: `110` under `rules/`
- Hook references: `4` under `hooks/`
- Codex plugin manifest: `.codex-plugin/plugin.json`
- Codex configuration: `.codex/config.toml`
- Codex project instructions: `AGENTS.md` and `.codex/AGENTS.md`

## Mapping Contract

| Upstream ECC path | Codex-ready path | Notes |
|---|---|---|
| `skills/<name>/SKILL.md` | `skills/<name>/SKILL.md` | Direct Codex skill surface; includes `everything-claude-code` promoted from `.agents/skills` for Codex loading. |
| `.agents/skills/<name>/SKILL.md` | `.agents/skills/<name>/SKILL.md` | Preserved upstream compatibility surface. |
| `agents/*.md` | `agents/*.md` | Preserved as reference agent role docs. |
| `.codex/**` | `.codex/**` | Preserved Codex-native config/roles from upstream. |
| `.codex-plugin/plugin.json` | `.codex-plugin/plugin.json` | Preserved plugin metadata with local installer support. |
| `rules/**` | `rules/**` | Preserved project rule references. |
| `hooks/**` | `hooks/**` | Preserved as reference; Codex currently lacks native hook events. |
| `commands/**` | `commands/**` | Preserved as instruction/reference shims. |

## Validation

Run `python3 scripts/codex/verify_ecc_codex.py` from the repository root. It checks skill frontmatter, key Codex files, manifest consistency, and install target integrity without requiring upstream npm dev dependencies.

