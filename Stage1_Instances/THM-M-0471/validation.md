# THM-M-0471 intake validation

Base revision: `8a13381618b241479a4786ca67704af7322f77aa` (tree
`0cc75f807f4c75d2a0aa8a72062e025083bd18ad`). Validation date: 2026-07-13
(Asia/Shanghai).

The intake validation below covers the planned dossier, natural-number scope,
source-statement crosswalk, open task DAG, JSON and scoped invariants, and a narrow pinned Lean API
probe. It did not validate a canonical THM-M-0471 expression or proof because exact representation
selection and expression fingerprinting originally belonged to the dependent statement phase.
That phase now has its own
`statement-validation.md` and provisional receipt. The automation-provided canonical `.lake`
symlink pre-existed this work and was used read-only. No `lake update`, `lake build`, dependency
clone/fetch, or other `.lake` mutation was performed. This dirty worker packet is nonrelease
evidence.

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
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0471` | 0 | rank 1353, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | 0 | preflight contained only the automation-provided untracked `Formalizations/Lean/.lake` symlink |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree match this record |
| bounded HTTPS inspection of Joyce's Euclid VII.30, VII.31, and IX.14 pages | 0 | relevant historical propositions located and HTML hashes recorded; discovery leads only, no H0 acceptance |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean identity recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake identity recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned mathlib revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output; pinned source was clean |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes recorded above |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0471/IntakeProbe.lean` | 0 | nine pinned list/exponent APIs and representative 2, 6-ordering, 0, and 1 boundaries elaborated; exact stdout hash is recorded in the receipt, with empty stderr |
| `python3 -m json.tool` on all owned JSON artifacts and the root worker packet | 0 | valid JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0471-pycache python3 -m py_compile Stage1_Instances/THM-M-0471/check_intake.py` | 0 | scoped validator compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0471/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | originally validated intake identity and the then-null target; the reconciled checker now validates the exact target, expanded artifact inventory, worker packet, H1/M3/R4 boundary, and open tasks |
| `python3 -B Stage1_Instances/THM-M-0471/check_intake.py` | 0 | public replay mode passed |
| prohibited-construct scan over the owned path | 0 policy result | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` Lean declaration token found |
| scoped per-new-file whitespace checks plus `git diff --check` | 0 | no whitespace errors |

## Evidence boundary

The intake Lean probe proves only that the named pinned declarations and small boundary examples
elaborate. The later statement packet freezes the root separately; neither packet maps the ancient
source to an accepted formal encoding, credits terminal proof bodies, or establishes release-grade
trust. The original-language/edition and translation audit, full source proof crosswalk,
independent review, candidate/provenance audit, obligation registry and typed graphs, proof and
composition, readable reconstruction, hermetic replay, deterministic bundle, and independent
verification all remain open. These boundaries prevent audit and theorem completion but do not
invalidate the planned dossier.
