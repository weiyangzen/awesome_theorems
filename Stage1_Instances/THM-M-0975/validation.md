# Intake validation

Base revision: `9c75282d42a7ef447d885d1d56997a79418bcd8a` (tree
`cc5285432a02107fadffb68c698690d1b98ac5f2`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers target membership, the `planned` dossier and open task DAG, duplicated
repository-source identity, primary-source and sibling-target boundaries, JSON and scoped
invariants, a narrow pinned Lean candidate probe, prohibited-construct hygiene, and whitespace. It
does not validate a canonical Azuma-Hoeffding proposition or proof because root selection,
historical-to-modern mapping, and the relationship to `THM-M-1080` remain open.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` link to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was performed.
This dirty worker run is nonrelease evidence.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`; no update or build was run.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status was clean.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Source discovery boundary

The J-STAGE article page, PDF, Crossref metadata, and bounded erratum query were retrieved only to
`/tmp` and were not added to the repository. Azuma's definitions, Lemma 1, and Remark 1 on printed
pages 357-358 were inspected. Crossref records no update relation, and the bounded query located no
erratum for this DOI; that is not a certified absence. The source observation supports H1, not H0.

## Commands and results

All repository commands ran at the repository root unless a different cwd is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0975` | 0 | rank 1509, planned, no legacy slot, legacy artifacts unaccepted, theorem_complete false |
| `git status --short --branch` before edits | 0 | detached HEAD; only the automation-provided `.lake` link was untracked and it was preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 7120,7125` and `-L 7287,7292 -- Docs/researches/math_theorems.md` | 0 | both uncited six-line records originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| retrieve J-STAGE article page and PDF for DOI `10.2748/tmj/1178243286` to `/tmp`, then run `file`, `wc -c`, `sha256sum`, `pdfinfo`, `pdftotext`, and scoped page-image inspection | 0 | free-access 1967 article, 11 pages and 537,047 bytes, SHA-256 `cf45e970...64d9`; definitions, Lemma 1, and Remark 1 on printed pp.357-358 inspected |
| retrieve and inspect Crossref metadata plus a bounded erratum query | 0 | author, title, journal, volume, issue, year, and DOI confirmed; no update relation or exact erratum found in the bounded query, not a certified absence |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'`; package `status --short` | 0 | pinned revision/tree recorded above; empty status output |
| bounded exact-topic `rg` inspection of pinned mathlib and repo-local Lean | 0 | exact-topic conditional sub-Gaussian tail theorem, MGF aggregator, ordinary Hoeffding lemma, and a legacy wrapper located; no source-identical root or bounded conditional bridge credited |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0975/IntakeProbe.lean)` | 0 | seven probability interfaces elaborated; both main candidates reported `[propext, Classical.choice, Quot.sound]`; stdout SHA-256 `bad24eed...f3cc` |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 | all structured records parse after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0975-pycache python3 -m py_compile Stage1_Instances/THM-M-0975/check_intake.py` | 0 | scoped checker compiles without writing generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0975/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/DAG identity, null target, H1/M3/R4 boundary, duplicate/source and dependency pins, artifact hashes, packet/receipt agreement, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0975/check_intake.py` | 0 | public replay mode passes without the scheduler-only root packet |
| `python3 -B Stage1_Instances/THM-M-0975/check_intake.py --replay-recipes --worker-packet .stage1-worker-selftest.json` | 0 | both recorded denied-network structured recipes replayed; structural invariants passed and Lean stdout digest matched |
| token-anchored prohibited Lean declaration scan over the owned path | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration token; diagnostic `#print axioms` remains permitted |
| scoped per-file new-file whitespace checks and `git diff --check` | 0 | no whitespace diagnostics |

## Known open gates

An admitted immutable source edition, exact finite or asymptotic root, complete definition and
assumption map, Hoeffding genealogy, correction/errata audit, independent source review, and a
master-approved disposition of the `THM-M-1080` overlap remain open. So do exact Lean imports and
expression, environment fingerprint, checked transports and mutations, exhaustive anchor and
provenance audit, discovery and obligation freezes, typed graphs, proof and composition, trust
closure, readable reconstruction, hermetic replay, deterministic bundle, independent verification,
master acceptance, audit completion, and theorem completion. These failures do not invalidate a
truthful, self-tested `planned` intake.
