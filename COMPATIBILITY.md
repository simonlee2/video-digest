# Host compatibility

Checked 2026-10-03. The shared `skills/` tree uses the Agent Skills core (`name`, `description`, scripts and references), with no vendor invocation fields, fixed model names or mandatory subagent API. Copy only `skills/video-digest`: stage guides and runtimes are internal and self-contained. The agent needs local file/shell access and image inspection; skill discovery alone does not provide these capabilities. The bundled transcription script still targets Apple Silicon macOS.

| Host | Project-local route | Actual coverage |
| --- | --- | --- |
| Codex CLI 0.156.1 | `python3 scripts/check_install.py ../try-codex --host codex` | Clean copy; the single entrypoint validates; copied renderer builds both formats; fresh local `codex debug prompt-input` discovers the entrypoint. No model turn sent. |
| Claude Code 2.1.280 | `python3 scripts/check_install.py ../try-claude --host claude` | Clean copy; component/manifest validation; copied renderer builds both formats. Live interactive discovery not verified. |
| Cursor | `--host generic`, then open the created project | Expected compatible with documented `.agents/skills/`; host not exercised here. |
| VS Code / GitHub Copilot | `--host generic`, then open the created project | Expected compatible with documented `.agents/skills/`; host not exercised here. |
| Other Agent Skills harnesses | Copy the single neutral `plugins/video-digest/skills/video-digest` folder into its documented project skill directory | Format-compatible in principle; runtime tools, vision and discovery must be checked in that host. |

The final design needs no vendor invocation fields: only the entrypoint is `SKILL.md`; internal guides use `STAGE.md` and are loaded by relative path. Thin plugin manifests and host-specific destination directories are the only adapters. The same scripts and editorial policy run in every host.

Manual installation copies the single skill folder into the chosen host directory. It has been exercised outside the checkout with spaces in the destination path. No globally registered plugin, account or paid API was used for these checks.

Official references:

- [Agent Skills specification](https://agentskills.io/specification): required `SKILL.md` metadata and optional resource directories.
- [Claude Code skills](https://code.claude.com/docs/en/skills): project `.claude/skills/`, plugin discovery and Claude invocation controls.
- [Cursor skills](https://cursor.com/docs/skills): project `.agents/skills/` and `.cursor/skills/` discovery.
- [VS Code Agent Skills](https://code.visualstudio.com/docs/agent-customization/agent-skills): project `.github/skills/`, `.claude/skills/` and `.agents/skills/` discovery.
- Codex behavior was checked against the installed CLI help, bundled `openai.yaml` reference and fresh-process local prompt discovery; no claim is made about a different CLI version.

First supported path to recommend: Codex project-local installation, because it has actual no-model discovery coverage here. Claude remains a target and has an adapter, not a claim of identical validation coverage. Full live inference in either host and remote marketplace installation remain outside this no-paid-call test.

Design references applied: [Anthropic webapp-testing](https://github.com/anthropics/skills/tree/main/skills/webapp-testing) for a small entrypoint with helper scripts; [Vercel installer](https://github.com/vercel-labs/skills/blob/main/src/installer.ts) for the selected-folder boundary; [Agent Skills script guidance](https://agentskills.io/skill-creation/using-scripts) for doctor/help/exit behavior; [Superpowers](https://github.com/obra/superpowers) for thin host manifests over shared skills. No source text or assets were copied from these projects. No required file is named metadata.json.
