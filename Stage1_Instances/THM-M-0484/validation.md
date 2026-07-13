# Intake validation

Base revision: `2226f559136f12fde46b1bf73cdf629043b8a648` (tree
`33cb254ed06b1391379b8e7f88c5e23188957b62`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers target membership, the planned dossier and open task DAG, the catalog and
source boundary, exact-topic pinned Lean candidate discovery, the candidate direction composition,
and the `p = 2` counterexample to an unconditional iff. It does not execute the statement,
anchor-audit, proof, or release phases and establishes no canonical expression fingerprint,
source-fidelity closure, terminal-body provenance, or proof credit. Initial status contained only
the automation-provided untracked `Formalizations/Lean/.lake` symlink. The canonical pinned
artifacts behind it were used read-only; no update, build, clone, fetch, or dependency mutation was
run. This dirty worker run is nonrelease evidence.

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
| `python3 scripts/stage1_target.py show THM-M-0484` | 0 | rank 1365; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all` | 0 | before intake, only the automation-provided untracked `.lake` symlink existed |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree recorded above |
| `git blame -L 3553,3558 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| bounded PrimePages and Crossref source inspection | 0 | modern odd-prime one-based criterion, incomplete displayed proof, Lehmer 1930 bibliographic lead, and source limitations recorded; no H0 admission |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned mathlib revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output |
| exact-topic repository and pinned-mathlib search | 0 | exact mathlib module and both correctness directions found; separate BHV and neighbor-target boundaries recorded |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0484/IntakeProbe.lean)` | 0 | eight definitions/declarations elaborated; both directions report `[propext, Classical.choice, Quot.sound]`; candidate iff and `p = 2` exception kernel-checked; stdout SHA-256 `27164568a5367c07303ed7d023ea02af91721972fb6bae221a212b7a5519031a` |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0484-pycache python3 -m py_compile Stage1_Instances/THM-M-0484/check_intake.py` | 0 | scoped checker compiled without generated repository files |

The final JSON parsing, scoped invariant check and worker-packet linkage, prohibited Lean construct
scan, and whitespace checks are recorded after receipt finalization in `intake-receipt.json`.

## Known open gates

The repository supplies no citation or exact source proposition. The primary Lehmer article and
complete proof were not inspected; source corrections, errata, Lucas/Lehmer attribution, the
odd-prime versus all-natural domain, recurrence indexing, congruence representation, correctness
directions, and any performance claim lack independent approval. The exact Lean expression and
environment fingerprints, checked source transports, and required statement mutations remain
open. So do the exhaustive anchor and terminal-provenance audit, discovery protocol, obligation
registry and typed graphs, proof/composition credit, trust closure, readable reconstruction,
hermetic replay, deterministic bundle, independent verification, and master acceptance. These
failures prevent every theorem-completion claim but do not invalidate a truthful self-tested
`planned` intake.
