# Intake validation

Base revision: `d502dd6f3d278ca9cb0ead8cbdc5f16c0e1fd8c9` (tree
`829a47c47ae831cada4f8acc6c2c00ba5883215e`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers the planned dossier, exact catalog and same-name scope boundaries, open task
DAG, structured intake invariants, source-family discrimination, and a narrow pinned Lean API
probe. It does not validate a canonical finite-difference theorem or proof because the repository
record supplies no truth-valued proposition. The automation-provided canonical `.lake` symlink
existed before this intake and was used read-only; no dependency update, build, clone, fetch, or
other `.lake` mutation was performed. This dirty worker evidence is nonrelease evidence.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status was clean before and after the
  probe.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; all 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1395` | exit 0; rank 1005, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | preflight exit 0; only the pre-existing automation-provided `Formalizations/Lean/.lake` symlink existed before this intake |
| `git blame -L 10160,10165 -- Docs/researches/math_theorems.md` | exit 0; all six uncited catalog fields originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `git blame -L 10693,10698 -- Docs/researches/math_theorems.md` | exit 0; the distinct same-name PDE record also originates at that commit and remains `THM-M-1465` |
| source retrieval and inspection for LeVeque, DOI `10.1137/1.9780898717839` | exit 0; author page, six-page table of contents, preface, errata, and Crossref metadata inspected; source-family lead only, not H0 |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0 before and after the probe; empty output |
| `sha256sum` on authoritative manifests, source records, toolchain, lock, source-family surfaces, and three probed mathlib modules | exit 0; hashes recorded in `instance.json` and the provisional receipt |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1395/IntakeProbe.lean)` | exit 0; eight adjacent pinned difference, exact-ODE, and Taylor interfaces elaborated; output SHA-256 `0a8fbc5ba33ae5ee7b9a9d83935c6b11844f192a581e8d60bbe7adf0b723bd9f`; no target theorem declared |
| bounded case-insensitive `rg` search for finite-difference ODE, numerical ODE, Euler-method, difference-scheme, convergence, and stability target patterns in repo-local Lean and pinned mathlib | exit 1; expected no exact-topic match, discovery only rather than an exhaustive external anchor audit |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and the root worker packet | exit 0 for each after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1395-pycache python3 -m py_compile Stage1_Instances/THM-M-1395/check_intake.py` | exit 0; the scoped checker compiled without generated files under the owned path |
| `python3 -B Stage1_Instances/THM-M-1395/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0; manifest and authoritative-DAG identity, null target, H5/M4/R4 boundary, source/dependency hashes, exact artifact inventory, provisional receipt/packet agreement, and six open tasks agree |
| prohibited Lean construct scan over the owned path | exit 1; expected no match for `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` |
| scoped no-index whitespace checks plus `git diff --check` | exit 0 for whitespace diagnostics; every untracked changed file passed |

## Known open gates

An approved target correction, exact immutable primary or authoritative theorem/page, incorporated
definitions, complete premise/conclusion/proof-boundary/errata crosswalk, choice among IVP/BVP,
scheme, consistency, stability, convergence, solvability, and error variants, `THM-M-1465` and
neighbor ownership review, and independent source review remain open. So do the canonical Lean
target and minimal imports, expression/environment fingerprints, checked transports, four
statement mutation classes, exhaustive anchor audit, discovery protocol, obligation registry,
typed graphs, proof and composition, source/provenance/trust closure, readable reconstruction,
hermetic replay, deterministic bundle, independent verification, master acceptance, audit
completion, and theorem completion. These failures do not invalidate a truthful self-tested
`planned` intake.
