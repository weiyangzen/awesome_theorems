# Intake validation

Base revision: `3d1d6d3eb018f17657cae1cfd7d25fc30492a12b` (tree
`3aa3dd324b35549da6cf2c5a54183a63ed1bfff9`). Validation ran on 2026-07-12 in
the isolated worker clone.

Validation is limited to target-set consistency, dossier structure and scope invariants, pinned
environment identity, a narrow Lean API probe, a bounded local name search, proof-escape hygiene,
and whitespace. The catalog record is not a proposition, so elaborating a purported canonical Lean
target would invent missing mathematics. `IntakeProbe.lean` therefore checks only possible
substrate; it introduces no theorem and supplies no statement or proof credit.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to the canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was performed.
The primary-source PDF was streamed to a temporary directory for source identification and removed;
it was not added as a dependency. This is nonrelease worker evidence.

| Command (repository root unless noted) | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1422` | 0 | rank 920, planned, L0/rework_required, no legacy slot, legacy artifacts unaccepted, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-1422/instance.json` | 0 | valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-1422/task-dag.json` | 0 | valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-1422/intake-receipt.json` | 0 | valid JSON after receipt finalization |
| `python3 -m json.tool .stage1-worker-selftest.json` | 0 | valid JSON after worker-manifest finalization |
| `python3 Stage1_Instances/THM-M-1422/check_intake.py` | 0 | target identity, H5/M4/R4 planned boundary, null target, empty accepted state, exact artifact inventory, and six open tasks agree |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1422-pycache python3 -m py_compile Stage1_Instances/THM-M-1422/check_intake.py` | 0 | intake validator compiles without adding generated files to the owned path |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1422/IntakeProbe.lean)` | 0 | seven pinned iteration, semiconjugacy, Birkhoff-sum, restriction, measure-preservation, and ergodicity API checks elaborated |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes `651c8acc...b1d2` and `321626c8...2d81`, respectively |
| `curl -L --fail --silent --show-error https://cims.nyu.edu/~lsy/papers/towers-billiards.pdf -o <temp>/young.pdf` followed by `sha256sum`, `pdfinfo`, `pdftotext`, and bounded theorem-heading checks | 0 | temporary 63-page source copy hashed to `549fdc2e...9171`; Theorem 1, 2, and 3 headings located; temporary files removed |
| Crossref DOI query for `10.2307/120960`, parsed with Python's JSON module | 0 | author, title, journal, volume 147, issue 3, starting page 585, and May 1998 metadata agree |
| bounded spelling search under pinned mathlib | 1 | expected no-match exit for concatenated, dotted, underscored, spaced, and hyphenated Young/Gibbs-Markov/return-time tower and inducing-scheme variants; intake discovery only |
| prohibited Lean proof-escape scan over the owned path | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, or `opaque` declaration |
| per-file `git diff --no-index --check /dev/null <owned-file>` plus owned-file invariants | 0 | no whitespace diagnostics across all untracked owned files and the worker manifest |

Known downstream failures remain deliberately open: an approved truth-valued target correction and
independent source review; exact binders, hypotheses, conclusion, and boundary cases; canonical Lean
elaboration, expression/environment fingerprints, checked transports, and mutations; immutable
formal anchor audit; discovery and obligation freezes; proof and composition; hermetic replay;
deterministic evidence bundling; independent release verification; and master acceptance. These
block ordinary theorem execution and completion but do not invalidate a truthful, self-tested
`planned` intake.
