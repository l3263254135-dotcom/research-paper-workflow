# Research Paper Workflow

A Codex plugin for evidence-first research papers: research positioning, data and result audit, manuscript drafting, independent review, submission checks, and revision tracking. The optional P2 adapter adds bounded analysis rules for Tibetan Plateau height and Arctic sea-ice research.

The workflow keeps results, figures, claims, and manuscript text traceable. It does not replace scientific judgment or author decisions. See [usage-playbook.md](plugins/research-paper-workflow/usage-playbook.md) for phase prompts.

## Install from GitHub

```bash
codex plugin marketplace add l3263254135-dotcom/research-paper-workflow
codex plugin add research-paper-workflow@research-paper-workflow
```

Start a new Codex task to load the installed skills.

## Local development and publishing

The editable personal source is `~/plugins/research-paper-workflow/`. Keep original source documents local; this repository contains only a description of the article methodology and the P2 domain rules. The Codex cache is an installation artifact.

```bash
../research-knowledge-onramp/scripts/publish-project.sh research-paper-workflow --dry-run
../research-knowledge-onramp/scripts/publish-project.sh research-paper-workflow --message "docs: refine evidence audit"
```

The publisher validates the plugin, checks for private paths and credentials, syncs this repository, commits and pushes `main`, then reinstalls the personal plugin. For GitHub installations, refresh the Git marketplace with `codex plugin marketplace upgrade research-paper-workflow` and reinstall.

Licensed under [MIT](LICENSE).
