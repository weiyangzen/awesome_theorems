# Statement-phase validation record

Base revision: `e562dd8e1c84c4ba651e8fc451dabc0401e3af8f`.

Verdict: **blocked at `exact_source_statement`**. The intake dependency is present, but it
deliberately freezes only a claim family. Its primary-source locator, complete assumptions, and
relative conclusion remain open. Consequently there is no exact proposition on which the Lean 4
statement gate or its required mutation tests can truthfully run. No `Statement.lean` was created:
an abstract record carrying the desired product diffeomorphism, or an arbitrary choice among the
open conventions, would be a substituted theorem.

## Commands and results

All commands ran in the worker clone. The existing automation-provided `.lake` link was used
read-only; no dependency update, fetch, build, or cache mutation was requested.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0587` | exit 0; rank 627, L0/rework required, planned, theorem complete false |
| `git rev-parse HEAD` | exit 0; `e562dd8e1c84c4ba651e8fc451dabc0401e3af8f` |
| `cd Formalizations/Lean && lake env lean --version` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `cd Formalizations/Lean && lake --version` | exit 0; Lake `5.0.0-src+98dc76e` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | exit 0; hashes recorded in `statement-blocker.json` |
| `rg -n -i 'h.?cobord\|cobordism\|配边' Docs Formalizations Stage1_Instances` (scoped review) | exit 0; repository catalog glosses and generic audit prose only; no exact THM-M-0587 formal target |
| `rg -n -i 'h.?cobord\|cobordism' Formalizations/Lean/.lake/packages/mathlib/Mathlib` | exit 1; no matching h-/smooth-cobordism API; unrelated `coborder` matches were reviewed separately |
| `cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_117.lean` | exit 0; the only nearby audit module elaborates, but contains no THM-M-0587 proposition and receives no credit |

## Gate boundary

This is blocker evidence, not a successful statement self-test. The canonical expression,
expression hash, minimal imports, checked alternate transports, and removed-hypothesis,
changed-domain, changed-scope, and boundary mutations are unavailable because their mathematical
input is not frozen. Therefore `.stage1-worker-selftest.json` is intentionally absent and no
statement, proof, audit-completion, or theorem-completion claim is made.
