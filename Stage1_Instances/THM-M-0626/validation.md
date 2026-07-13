# Intake validation

Base revision: `d1b510bacab792f84a99231485cf4429fdb78978` (tree
`f77c4e4db196fc0ecc271815514a411d06ea6053`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers target membership, the planned dossier and open task DAG, the literal
source boundary, an immutable modern proof-source lead, and a narrow pinned Lean candidate probe.
It does not execute the statement, anchor-audit, proof, or release phases and establishes no
canonical expression fingerprint or proof credit. Initial status contained only the
automation-provided untracked `Formalizations/Lean/.lake` symlink. The canonical pinned artifacts
behind it were used read-only; no update, build, clone, fetch, or dependency mutation was run.
This dirty worker run is nonrelease evidence.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status was clean.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0626` | 0 | rank 1320; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all` | 0 | before intake, only the automation-provided untracked `.lake` symlink existed |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree recorded above |
| `git blame -L 4643,4648 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| immutable Stacks Project inspection at commit `3683021e95ea1610e2250658d59abc18fdf0bd7b` | 0 | Definition 5.7.1 and Lemma 5.7.2/tag `0376` locate the nonempty convention, exact global-continuity statement, and complete clopen proof; source SHA-256 `44548f...981` |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0626/IntakeProbe.lean)` | 0 | nine direct/adjacent interfaces elaborated; candidate axiom report `[propext, Classical.choice, Quot.sound]`; complete stdout SHA-256 `e4babbea7000e342c6a3204859eb95d98a058e0df494a210afef3161fe13159f` |

The final JSON parsing, Python checker compilation, scoped invariant check, worker-packet linkage,
prohibited Lean construct scan, and whitespace checks are recorded after receipt finalization in
`intake-receipt.json`.

## Known open gates

The catalog's historical source and attribution remain unidentified. Independent source review,
correction/errata disposition, local/global continuity transport, exact universes and binder order,
set/subtype encoding, expression and environment fingerprints, checked alternate encodings, and
four statement mutations remain open. So do the comprehensive formal-candidate audit, discovery
protocol, obligation registry and typed graphs, proof and composition credit, terminal provenance
and trust closure, readable reconstruction, hermetic replay, deterministic bundle, independent
verification, and master acceptance. These failures prevent every theorem-completion claim but do
not invalidate a truthful self-tested `planned` intake.
