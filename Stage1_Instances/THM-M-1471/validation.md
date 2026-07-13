# THM-M-1471 intake validation

Base revision: `1305c30bb297a27f8ce539ca8c0c90dc241aa6c7` (tree
`b77b52bf93cbd1927fd17f0d7f5bcab2eba3ab07`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers the planned dossier, exact catalog boundary, six-node open task DAG,
structured intake invariants, and a narrow pinned Lean API probe. It does not validate a canonical
a priori error proposition or proof because the repository record supplies no truth-valued root.
The automation-provided canonical `.lake` symlink existed before this intake and was used read-
only; no dependency update, build, clone, fetch, or other `.lake` mutation was performed. This
dirty worker run is nonrelease evidence.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e` on Linux `7.0.0-27-generic` x86_64.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status was clean before and after
  the probe.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1471` | exit 0; rank 1148, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` (preflight) | exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before intake |
| `git rev-parse HEAD 'HEAD^{tree}'` | exit 0; base revision and tree match this record |
| `git blame -L 10735,10740 -- Docs/researches/math_theorems.md` | exit 0; all six uncited catalog fields originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| repo-wide exact target/gloss/source search and bounded a-priori/error/order search over tracked Lean plus pinned mathlib | completed; no source citation or source-identical numerical error theorem was found; intake discovery only, not a global absence proof |
| `sha256sum` over manifest, blueprint, DAG, skill, guidelines, catalogs, Stage0, toolchain, lockfile, source excerpts, and three pinned mathlib modules | exit 0; exact hashes are recorded in `instance.json` and the provisional receipt |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean version and target recorded above |
| `(cd Formalizations/Lean && lake --version)` | exit 0; Lake version recorded above; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0 before and after the probe; empty output |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1471/IntakeProbe.lean)` | exit 0; seven adjacent pinned APIs elaborated and three representative axiom reports printed; stdout SHA-256 `106b532249fbd68bedfd0738274e0a166d1c177daeb39eda89ddc99e071ba999`, empty stderr; no target theorem declared |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | exit 0 for each after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1471-pycache python3 -m py_compile Stage1_Instances/THM-M-1471/check_intake.py` | exit 0; scoped validator compiled without adding generated files to the owned path |
| `python3 -B Stage1_Instances/THM-M-1471/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0 after finalization; manifest/DAG identity, null target, H5/M4/R4 boundary, source and dependency hashes, exact artifact inventory, receipt/packet, and six open tasks agree |
| `rg -n -e '\bsorry\b' -e '\badmit\b' -e '\bsorryAx\b' -e '\baxiom\b' -e '\bconstant\b' -e '\bopaque\b' -e '\bunsafe\b' Stage1_Instances/THM-M-1471 --glob '*.lean'` | exit 1 as expected; no prohibited declaration in the discovery-only probe |
| `git diff --check`, plus `git diff --no-index --check /dev/null <file>` for every untracked changed file | exit 0 for whitespace diagnostics; every changed file passed |

## Known open gates

An approved target correction, exact immutable primary or authoritative theorem/page,
incorporated definitions, complete premise/conclusion/proof-boundary/errata crosswalk, choice of
problem and method, exact and numerical solutions, approximation parameter, regularity and
stability assumptions, norm, rate, constants, quantifier order, arithmetic and boundary cases,
neighbor ownership review, and independent source review remain open. So do the canonical Lean
target and minimal imports, expression/environment fingerprints, checked transports, four
statement mutation classes, exhaustive anchor audit, discovery protocol, obligation registry,
typed graphs, proof and composition, source/provenance/trust closure, readable reconstruction,
hermetic replay, deterministic bundle, independent verification, master acceptance, audit
completion, and theorem completion. These failures do not invalidate a truthful self-tested
`planned` intake.
