# THM-M-1458 intake validation

Base revision: `01a2c11623c3f2f021424380d1c87b42f2d7e0e8` (tree
`8d6be645c3940807dbb57edc4fbe6c1485dbf1b6`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers the planned dossier, source-statement and non-substitution boundaries, the
six-node open task DAG, structured intake invariants, and a narrow pinned Lean API probe. It does
not validate a canonical FFT proposition or proof because no source-selected root exists. The
automation-provided canonical `.lake` symlink was pre-existing and used read-only; no dependency
update, build, clone, fetch, or other `.lake` mutation was performed. This dirty worker run is
nonrelease evidence.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e` on Linux `7.0.0-27-generic` x86_64.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status was clean.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1458` | exit 0; rank 1135, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | preflight exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before intake |
| `git rev-parse HEAD 'HEAD^{tree}'` | exit 0; base revision and tree recorded above |
| `git blame -L 10644,10649 -- Docs/researches/math_theorems.md` | exit 0; all six uncited catalog lines originate in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| Crossref DOI query for `10.1090/S0025-5718-1965-0178586-1` | exit 0; title, authors, 1965 date, volume 19, issue 90, and pages 297-301 confirmed; bibliographic lead only, no paper text or H credit |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0; empty output |
| bounded case-insensitive search for FFT, radix, butterfly, and Cooley-Tukey in pinned mathlib and tracked Lean | completed; dense DFT and finite-character APIs found, but no FFT algorithm, correctness bridge, or complexity theorem; intake discovery only |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1458/IntakeProbe.lean)` | exit 0; eight dense-DFT, inversion, and finite-character APIs elaborated; stdout SHA-256 `5898e3735ce796f385476d4a3d9a7d92ff3dcd2850cd726ce31db56d43098ec8`; representative axiom reports contain only `propext`, `Classical.choice`, and `Quot.sound`; no target theorem |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | exit 0 for each after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1458-pycache python3 -m py_compile Stage1_Instances/THM-M-1458/check_intake.py` | exit 0; scoped validator compiled without adding generated files to the owned path |
| `python3 -B Stage1_Instances/THM-M-1458/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0 after finalization; manifest/DAG identity, null target, H5/M4/R4 boundary, pins, hashes, receipt/packet, and six open tasks agree |
| `rg -n -e '\bsorry\b' -e '\badmit\b' -e '\bsorryAx\b' -e '\baxiom\b' -e '\bconstant\b' -e '\bopaque\b' -e '\bunsafe\b' Stage1_Instances/THM-M-1458 --glob '*.lean'` | exit 1 as expected; no prohibited declaration in the API-only probe |
| scoped `awk` trailing-whitespace checks on every new file plus `git diff --check` | exit 0; no whitespace diagnostics |

## Known open gates

The algorithm label must be redirected to an independently reviewed, immutable, exact proposition.
The DFT sign and normalization, carrier, indexing, admissible lengths and factorization, algorithm,
recursion, permutation, implementation semantics, correctness, termination, operation cost model,
complexity or error conclusion, ordered binders, and boundary cases remain open. So do the canonical
Lean expression and environment fingerprints, transports, statement mutations, exhaustive formal
anchor audit, discovery protocol, obligation registry, typed graphs, proof and composition,
trust/provenance closure, readable reconstruction, hermetic replay, deterministic bundle,
independent verification, master acceptance, audit completion, and theorem completion. These open
gates do not invalidate a truthful self-tested `planned` intake.
