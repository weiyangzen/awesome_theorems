# Intake validation

Base revision: `c76fe0f1a7514b41f191d16840eff25e64ee9d17`.

Validation covers target membership, source and dependency fingerprints, planned-dossier invariants,
the exact open task chain, artifact ownership, and a discovery-only Lean API probe. The automation-
provided canonical `.lake` symlink was used read-only. No `lake update`, `lake build`, clone, fetch,
or dependency mutation was run. This dirty worker run is not release evidence.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-0052` | exit 0; rank 1090, L0/rework_required, planned, theorem_complete false |
| `git status --short --untracked-files=all` | exit 0; pre-edit status contained only the automation-provided `Formalizations/Lean/.lake` symlink |
| `git blame -L 391,396 -- Docs/researches/math_theorems.md` | exit 0; all six uncited record lines originate at `bcf3f9fa...` |
| publisher PDF and Crossref inspection | exit 0; Penrose 1955 bibliographic identity and Theorem 1 source lead inspected; not H0 |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | exit 0; Lean 4.29.0 at `98dc76e3`, Lake 5.0.0-src+98dc76e |
| pinned mathlib revision/status check | exit 0; `8a178386...`, tree `bdc39a31...`, clean package worktree |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0052/IntakeProbe.lean` | exit 0; nine adjacent APIs elaborated, stdout SHA-256 `06a13297...`; no target or proof |
| bounded Moore-Penrose/pseudoinverse search | exit 0; no exact declaration under the patterns; only explicit non-support and unrelated prose |
| JSON parsing for `instance.json`, `task-dag.json`, `intake-receipt.json`, and the worker packet | exit 0 |
| `python3 -B Stage1_Instances/THM-M-0052/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0; target, hashes, pins, planned boundary, artifacts, receipt, and task chain agree |
| controlled owned-artifact mutation test | expected exit 1 after appending to `README.md`; checker rejected its stale digest, file restored byte-for-byte, clean replay then exited 0 |
| prohibited Lean declaration scan | expected no-match exit 1; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `git diff --check -- Stage1_Instances/THM-M-0052 .stage1-worker-selftest.json` | exit 0; no whitespace diagnostics; scoped validator covers untracked file bytes |

Known downstream failures are source identity and independent review, Moore attribution audit,
immutable source admission, exact canonical statement and elaboration, alternate encodings and
mutations, anchor audit, proof, provenance/trust/composition closure, readable reconstruction,
hermetic replay, independent verification, and master acceptance. These prevent any theorem claim
but do not invalidate this fail-closed planned intake.
