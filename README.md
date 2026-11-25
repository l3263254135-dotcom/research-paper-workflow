# Evidence to Paper

A Codex plugin for evidence-first research papers: publishability checks, project harness setup, data and result audit, figure planning and optimization, evidence-preserving manuscript reconstruction, manuscript drafting, dual-AI independent review, submission checks, revision tracking, and optional science communication. The optional P2 adapter adds bounded analysis rules for Tibetan Plateau height and Arctic sea-ice research.

The workflow keeps questions, results, figures, claims, manuscript text, review findings, and submission records traceable. It reports scientific quality and presentation quality separately, preserves `BLOCKED` dependencies, and does not replace scientific judgment or author decisions. Start with `$research-paper-workflow:idea-to-journal-paper` to compare competing explanations, choose the smallest test that could change the scientific claim, and decide how to revise for each outcome. See [usage-playbook.md](plugins/research-paper-workflow/usage-playbook.md) for phase prompts.

Default working order (separate from the journal's section order):

1. Define a testable scientific question and check its contribution against prior work.
2. Document data and methods before new analysis; keep planned and executed methods separate.
3. Arrange verified figures and tables to answer successive questions, then write Results and Discussion. If the argument has a gap, display an existing result, run the missing analysis, or narrow the claim to what the design can support.
4. Strengthen the Introduction and research significance based on what the results answer.
5. Write the bounded Conclusion, then condense the argument into the Abstract.

Follow with independent review and submission checks. The plugin display name changed; its ID and skill commands remain unchanged.

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
