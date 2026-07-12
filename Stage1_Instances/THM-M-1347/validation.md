# Intake validation

Base revision: `53ef4456383f8ae0068669a633bb02c08056bce8` (tree
`d88aafa961abcd157b3f589fa1eaf2d675c2395d`). Validation ran on 2026-07-13 in
the isolated worker clone.

Validation is limited to target-set consistency, dossier structure and scope invariants, pinned
environment identity, a narrow Lean API probe, bounded local discovery, proof-escape hygiene, and
whitespace. The source record is not binder-complete, so elaborating a purported canonical Lean
target would invent missing mathematics. `IntakeProbe.lean` therefore checks only potential
substrate; it introduces no theorem and supplies no statement or proof credit.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was performed.
This is nonrelease worker evidence.

| Command (repository root unless noted) | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1347` | 0 | rank 958, planned, L0/rework_required, no legacy slot, legacy artifacts unaccepted, theorem_complete false |
| initial `git status --short --untracked-files=all` | 0 | only the pre-existing `.lake` reuse symlink; preserved read-only |
| source-history and Crossref/Springer metadata inspection | 0 | uncited catalog provenance and matching Carr book/chapter lead located; full theorem text and H0 mapping remain open |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | pinned revision `8a178386...eea95`, tree `bdc39a3...e5c2b`; a separate package status check was clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1347/IntakeProbe.lean)` | 0 | nine adjacent pinned ODE, invariance, smoothness, linear-operator, invariant-submodule, and spectrum APIs elaborated |
| bounded exact-topic search in repo-local Lean and pinned mathlib | 1 | expected no-match exit for center/centre-manifold names; discovery only, not an exhaustive external anchor audit |
| `python3 -m json.tool` on the three JSON artifacts and worker packet | 0 | valid JSON after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1347-pycache python3 -m py_compile Stage1_Instances/THM-M-1347/check_intake.py` | 0 | scoped validator compiles without generated owned-path files |
| `python3 -B Stage1_Instances/THM-M-1347/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target and DAG identity, source hashes, H1/M4/R4 boundary, null target, artifact inventory, receipt/packet agreement, and six open tasks agree |
| prohibited Lean proof-escape scan over the owned path | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| scoped whitespace checks | 0 | no diagnostics; the validator checks every untracked owned file |

The first attempted Lean probe used the nonexistent import
`Mathlib.Analysis.Normed.Operator.Spectrum` and exited 1. No dependency was fetched or built. The
probe was corrected to the already pinned and built `Mathlib.Analysis.Normed.Operator.Banach`,
which exposes the intended spectrum surface; the exact recorded recipe then exited 0. This failed
draft command is retained here as known validation history and carries no evidence.

Known downstream failures remain deliberately open: a lawful complete primary-source edition,
exact numbered theorem, definition/assumption/conclusion/proof-boundary/errata mapping, and
independent review; canonical binders and boundary cases; Lean elaboration, expression and
environment fingerprints, transports, and mutations; exhaustive immutable formal-anchor audit;
discovery and obligation freezes; proof and composition; readable reconstruction; hermetic replay;
deterministic evidence bundling; independent release verification; and master acceptance. These
block theorem execution and completion but do not invalidate a truthful, self-tested `planned`
intake.
