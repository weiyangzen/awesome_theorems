# Intake validation

Base revision: `bd81d4853a030765585ef6fed4310484ceb1e458` (tree
`fb92fc7476bff9a2ce8c20f1d7be34c6655ca6b4`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers target membership, the `planned` dossier and open task DAG, repository and
primary-source identity, source-scope crosswalk, JSON and scoped invariants, a narrow pinned Lean
candidate probe, prohibited-construct hygiene, and whitespace. It does not validate a canonical
Hahn-Banach proposition or proof because scalar, space, historical-to-modern premise, and target
selection remain open.

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

## Commands and results

All repository commands ran at the repository root unless a different cwd is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0274` | 0 | rank 1280, planned, no legacy slot, legacy artifacts unaccepted, theorem_complete false |
| `git status --short --untracked-files=all` before edits | 0 | only the automation-provided `.lake` link was untracked; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame` on both catalogue records | 0 | both six-line records originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| retrieve and inspect Crossref metadata for DOI `10.1515/crll.1927.157.214` outside the repository | 0 | Hans Hahn, 1927, printed pages 214-229; response SHA-256 `d530282...509` |
| retrieve and inspect the GDZ IIIF volume manifest and printed pages 214-229 outside the repository | 0 | manifest has 269 canvases, is 364,004 bytes, and has SHA-256 `0ae9178...ae9`; Theorem III and the preceding definition chain were inspected at printed pages 215-218; page-217 OCR SHA-256 `22a0808...67` |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'`; package `status --short` | 0 | pinned revision/tree recorded above; empty status output |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0274/IntakeProbe.lean)` | 0 | seven subspace, dual, real/uniform analytic, algebraic, finite-range, and dual-vector interfaces elaborated; both candidates reported `[propext, Classical.choice, Quot.sound]`; stdout SHA-256 `c4608d8...d75` |
| bounded exact-topic `rg` inspection of pinned mathlib and repo-local Lean | 0 | exact-topic declarations and geometric variants located; no source-identical root transport or proof credit inferred; this is not the later exhaustive anchor audit |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 | all structured records parse after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0274-pycache python3 -m py_compile Stage1_Instances/THM-M-0274/check_intake.py` | 0 | scoped checker compiles without writing generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0274/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/DAG identity, null target, H1/M3/R4 boundary, source and dependency pins, artifact hashes, packet/receipt agreement, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0274/check_intake.py` | 0 | public replay mode passes without the scheduler-only root packet |
| `python3 -B Stage1_Instances/THM-M-0274/check_intake.py --replay-recipes --worker-packet .stage1-worker-selftest.json` | 0 | both recorded structured recipes replayed with denied-network policy and the Lean stdout digest matched |
| token-anchored prohibited Lean declaration scan over the owned path | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration token; diagnostic `#print axioms` remains permitted |
| scoped per-file new-file whitespace checks and `git diff --check` | 0 | no whitespace diagnostics |

## Known open gates

Complete primary-source definitions, exact ordered statement, assumptions, historical-to-modern
translation, proof mapping, Hahn/Banach attribution, corrections or errata, and independent review
remain open. So do canonical scalar and space selection, exact Lean imports and expression,
environment fingerprint, checked transports and mutations, exhaustive anchor/provenance audit,
discovery and obligation freezes, typed graphs, proof and composition, trust closure, readable
reconstruction, hermetic replay, deterministic bundle, independent verification, master acceptance,
audit completion, and theorem completion. These failures do not invalidate a truthful, self-tested
`planned` intake.
