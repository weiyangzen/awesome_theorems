# Intake validation

Base revision: `62fad55ced807fdc06921c45d6fcd1f9ad86a1c2` (tree
`9d7c8fe49a4c859d90f3069dc47973ffc5ced768`). Validation ran on 2026-07-13 in
the isolated worker clone.

Validation is limited to target-set consistency, dossier structure and scope invariants, pinned
environment identity, a narrow Lean API probe, bounded local name discovery, proof-escape hygiene,
and whitespace. The source wording is not a proposition, so elaborating a purported canonical Lean
target would invent missing mathematics. `IntakeProbe.lean` checks only possible substrate; it
introduces no theorem and supplies no statement or proof credit.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to the canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was performed.
This is nonrelease worker evidence.

| Command (repository root unless noted) | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1590` | 0 | rank 1211, planned, L0/rework_required, no legacy slot, legacy artifacts unaccepted, theorem_complete false |
| initial `git status --short --untracked-files=all` | 0 | only the pre-existing automation-provided `Formalizations/Lean/.lake` symlink |
| `git blame -L 11714,11719 -- Docs/researches/math_theorems.md` | 0 | all six catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, finalized `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1590-pycache python3 -m py_compile Stage1_Instances/THM-M-1590/check_intake.py` | 0 | intake validator compiles without adding generated files to the owned path |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e`; no update or build was run |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1590/IntakeProbe.lean)` | 0 | eight adjacent coordinate-rotation, linear-transport, Hamming, and circulant-matrix APIs elaborated; output SHA-256 `63569025...eedd` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | pinned mathlib revision `8a178386...eea95`, tree `bdc39a31...c2b`; used read-only |
| bounded case-insensitive cyclic-code source-name search under pinned mathlib and repo-local Lean | 0 | the wrapped command verified an expected no-match exit; no exact-topic declaration found; intake discovery only, not an anchor audit |
| prohibited Lean proof-escape scan over the owned path | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `python3 -B Stage1_Instances/THM-M-1590/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target identity, H5/M4/R4 planned boundary, null target, exact artifact inventory, source hashes, worker packet, and six open tasks agree |
| `git diff --check -- Stage1_Instances/THM-M-1590 .stage1-worker-selftest.json` plus per-new-file no-index checks | 0 | no whitespace diagnostics, including all untracked owned artifacts |

Crossref metadata for Huffman and Pless, Chapter 4, was fetched only for intake source discovery
before validation recipes were frozen. It identified an authoritative source-family lead but did
not expose proposition or proof text; it is not source-proof evidence and is not part of a
network-denied validation recipe.

Known downstream failures remain deliberately open: an approved target correction or one immutable
truth-valued source proposition with independent review; exact alphabet, word, code, shift,
invariance, conclusion, and boundary conventions; canonical Lean elaboration, expression and
environment fingerprints, checked transports, and mutations; immutable formal-anchor audit;
discovery and obligation freezes; proof and composition; hermetic replay; deterministic evidence
bundling; independent release verification; and master acceptance. These block ordinary theorem
execution and completion but do not invalidate a truthful, self-tested `planned` intake.
