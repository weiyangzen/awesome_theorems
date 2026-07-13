# Intake validation

Base revision: `0c019b7194c9c43fa5f683fa82d637a0b275410d` (tree
`43cf6ac322b1dba09be739b52ab3d02e9f9d8f3e`). Validation date: 2026-07-13
(Asia/Shanghai).

Validation is limited to target-set consistency, the planned dossier and open task DAG, source and
variant discrimination, pinned environment identity, adjacent Lean API elaboration, bounded local
name search, JSON and scoped invariants, proof-escape hygiene, and whitespace. The catalog does not
provide a binder-complete proposition and its 1970 attribution conflicts with the modern history
of the independence-number ratio bound. Therefore no canonical target, expression hash, statement
mutation, H0 source acceptance, or proof is claimed.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was performed.
This is nonrelease worker evidence.

## Environment

- Platform: Linux 7.0.0-27-generic, x86_64; Lean target `x86_64-unknown-linux-gnu`.
- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package worktree clean.
- `Formalizations/Lean/lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `Formalizations/Lean/lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

| Command (repository root unless noted) | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0890` | 0 | rank 1440, planned, L0/rework_required, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| initial `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the pre-existing `.lake` symlink; base revision and tree recorded above |
| `git blame -L 6516,6521 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog fields originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| Crossref metadata inspection for DOI `10.1016/j.laa.2021.02.010`; arXiv `2102.05529v2` PDF inspection | 0 | exact modern statement/proof lead at Section 2, Theorem 1; PDF SHA-256 `e2a90698...22bc`; source reports that Hoffman did not publish the bound and calls the 1970 coloring paper a wrong reference; H1 discriminator only |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | pinned Lean and Lake versions above; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision/tree above; package source clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0890/IntakeProbe.lean)` | 0 | ten adjacent independent-set, regularity, adjacency-matrix, Hermitian-eigenvalue, and positive-semidefinite APIs elaborated; complete output SHA-256 recorded in the receipt; no target declaration or proof body |
| bounded case-insensitive `rg` for Hoffman and ratio-bound Lean declarations | 1 (expected no match) | no exact-topic target in repo-local or pinned-mathlib Lean; intake discovery only, not exhaustive external audit |
| `python3 -m json.tool` on the four owned/root JSON artifacts after finalization | 0 | valid JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0890-pycache python3 -m py_compile Stage1_Instances/THM-M-0890/check_intake.py` | 0 | scoped checker compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0890/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/DAG identity, source and dependency hashes, H1/M4/R4 null target, inventory, packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0890/check_intake.py` | 0 | public replay mode passed without the scheduler-only worker packet |
| prohibited Lean construct scan over the owned path | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| per-new-file whitespace checks and `git diff --check -- Stage1_Instances/THM-M-0890 .stage1-worker-selftest.json` | 0 aggregate | no whitespace diagnostics |

## Known open gates

Independent source selection and review, reconciliation of the catalog's 1970 attribution, primary
genealogy, complete definition/premise/conclusion/proof-boundary/correction crosswalk, and
separation of the regular ratio bound from chromatic, equality, weighted, irregular, Laplacian,
strongly regular, and other variants remain open. So do the canonical Lean target and minimal
imports, expression/environment fingerprints, checked transports, four statement mutation
classes, exhaustive anchor audit, discovery protocol, obligation registry, typed graphs, proof and
composition, source/provenance/trust closure, readable reconstruction, hermetic replay,
deterministic bundle, independent verification, master acceptance, audit completion, and theorem
completion. These failures block statement and theorem progress but do not invalidate a truthful
self-tested `planned` intake.

## Status boundary

This is provisional worker self-test evidence for `S56-M-0890-INTAKE` only. It supports a planned
dossier, not an accepted node receipt. No canonical statement, H0 source closure, proof, audit
completion, theorem completion, or master acceptance is claimed.
