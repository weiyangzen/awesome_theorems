# THM-M-1472 intake validation

Base revision: `f4efdfc7c685252a98f3508a5974ba81c0377a95` (tree
`94a9cfc613f86042a21fdfa174ba887334b93893`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers the planned dossier, exact catalog boundary, historical and modern
source-family discrimination, external Coq lead, six-node open task DAG, structured intake
invariants, and a narrow pinned Lean API probe. It does not validate a canonical Lax-Richtmyer
statement or proof because source identity and direction are not frozen. The automation-provided
canonical `.lake` symlink existed before intake and was used read-only; no dependency update,
build, clone, fetch, or other `.lake` mutation was performed. This dirty worker run is nonrelease
evidence.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e` on Linux x86_64.
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
| `python3 scripts/stage1_target.py show THM-M-1472` | exit 0; rank 1149, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` (preflight) | exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before intake |
| `git rev-parse HEAD 'HEAD^{tree}'` | exit 0; base revision and tree match this record |
| `git blame -L 10742,10747 -- Docs/researches/math_theorems.md` | exit 0; all six uncited catalog fields originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| Crossref query for DOI `10.1002/cpa.3160090206` | exit 0; title, Lax and Richtmyer authorship, May 1956, journal 9(2), pages 267-293 confirmed; publisher full text returned HTTP 403, so bibliography only |
| Retrieval and inspection of arXiv `2103.13534` | exit 0; 23-page PDF SHA-256 `efa90f24bccc18f9cfb04fa958da96a49d27ab094b0b64a7fc3c4aaa157fc1f6`; Definitions 1-5, Theorem 1, Coq/foundation boundary, and Sanz-Serna-Palencia provenance recorded; modern lead only |
| GitHub API/raw retrieval at `mohittkr/Lax_equivalence@c19b626513ce8ec1a6426f2364e6c45e8caa85ae` | exit 0; tree, `lax_equivalence.v` declaration `is_convergent`, README dependency pins, and exact hashes recorded; no clone, fetch, build, or proof credit |
| `sha256sum` over authority inputs, catalog/Stage0 excerpts, toolchain/lockfile, three pinned mathlib modules, and observed external surfaces | exit 0; exact hashes are recorded in `instance.json` and the provisional receipt |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean version and target recorded above |
| `(cd Formalizations/Lean && lake --version)` | exit 0; Lake version recorded above; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0 before and after probe; empty output |
| bounded case-insensitive search for Lax-Richtmyer, Lax equivalence, finite-difference scheme, discretization-method, and exact slogan patterns in repo-local Lean and pinned mathlib | completed; no exact topic declaration appeared; intake discovery only, not a global absence proof |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1472/IntakeProbe.lean)` | exit 0; six adjacent pinned APIs elaborated and two axiom reports printed; stdout SHA-256 `b8e000af7bd6b5c69c599349fadef4c69b0ac10132d43c8aa62d158989add909`, empty stderr; no target theorem declared |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | exit 0 for each after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1472-pycache python3 -m py_compile Stage1_Instances/THM-M-1472/check_intake.py` | exit 0; scoped validator compiled without adding generated files to the owned path |
| `python3 -B Stage1_Instances/THM-M-1472/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0 after finalization; authority/DAG identity, source and dependency hashes, null target, H1/M4/R4 boundary, exact artifact inventory, receipt/packet, validation actions, and six open tasks agree |
| `rg -n -e '\bsorry\b' -e '\badmit\b' -e '\bsorryAx\b' -e '\baxiom\b' -e '\bconstant\b' -e '\bopaque\b' -e '\bunsafe\b' Stage1_Instances/THM-M-1472 --glob '*.lean'` | exit 1 as expected; no prohibited declaration in the discovery-only probe |
| `git diff --check`, plus `git diff --no-index --check /dev/null <file>` for every untracked changed file | exit 0 for whitespace diagnostics; every changed file passed |

The axiom reports for the adjacent pinned declarations `banach_steinhaus` and
`ContinuousLinearMap.le_opNorm` were `[propext, Classical.choice, Quot.sound]`. They describe
discovery substrate only and do not select a foundation profile or prove the target.

## Known open gates

A preserved and approved historical or generalized source result, corrected Lax-Richtmyer
attribution, complete definition/assumption/direction/proof-boundary/errata crosswalk, choice of
continuous and discrete problems, step family, consistency/stability/convergence predicates,
norms, filters, quantifiers, data and time boundary, neighbor ownership, and independent source
review remain open. So do the canonical Lean target and minimal imports, expression/environment
fingerprints, checked transports, four statement mutation classes, exhaustive anchor and external
Coq audit, discovery protocol, obligation registry, typed graphs, proof and composition,
source/provenance/trust closure, readable reconstruction, hermetic replay, deterministic bundle,
independent verification, master acceptance, audit completion, and theorem completion. These open
gates do not invalidate a truthful self-tested `planned` intake.
