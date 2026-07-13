# Intake validation

Base revision: `db4b8793e70ce8af74c9c9490acfa50aa3684d5e` (tree
`6434a20532ae7c523ad293e67a6228ab384bfb8a`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers only `S56-M-0913-INTAKE`: manifest membership, the planned dossier and
source/non-substitution boundaries, the six-task open DAG, scoped structural invariants, and a
narrow pinned Lean API probe. It does not validate a canonical statement or proof because neither
is frozen. The automation-provided canonical `.lake` symlink was pre-existing and used read-only;
no update, build, clone, fetch, or other `.lake` mutation was performed. The dirty worker run is
nonrelease evidence.

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

All commands ran from the repository root unless a different working directory is shown.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, and execution skill passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0913` | exit 0; rank 1455, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | preflight exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before this intake |
| `git rev-parse HEAD 'HEAD^{tree}'` | exit 0; base revision and tree recorded above |
| `git blame -L 6679,6684 -- Docs/researches/math_theorems.md` | exit 0; all six uncited catalog lines originate in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `sed -n '6679,6684p' Docs/researches/math_theorems.md \| sha256sum` | exit 0; catalog block SHA-256 `8e7f3942cfb7103cdecabfb69d05fa402066fd8af6d90f7afcaf4756c046938a` |
| `rg -n 'inclusion.?exclusion\|card.*union'` over pinned mathlib Lean sources | exit 0; the dedicated finite-family module, cardinality/sum/complement variants, and two-set identity were located for bounded intake inspection |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0; empty output |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0913/IntakeProbe.lean)` | exit 0; six adjacent interfaces elaborated; principal finite-family and two-set candidates both reported `propext`, `Classical.choice`, and `Quot.sound` |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | exit 0 for each finalized JSON artifact |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0913-pycache python3 -m py_compile Stage1_Instances/THM-M-0913/check_intake.py` | exit 0; scoped validator compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0913/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0; target/DAG identity, source and pin hashes, H5/M3/R4 null-target boundary, exact inventory, packet agreement, Lean replay, and six open tasks agree |
| `rg -n --glob '*.lean' '(^\|[^A-Za-z])(sorry\|admit\|sorryAx\|axiom\|constant\|opaque\|unsafe)([^A-Za-z]\|$)' Stage1_Instances/THM-M-0913` | exit 1 as expected; no prohibited declaration or proof escape matched |
| scoped tracked and no-index `git diff --check` over the dossier and worker packet | exit 0; every new file passed the explicit whitespace check, with no tracked-diff diagnostics |

## Structured recipes

The provisional receipt records two replayable, network-denied recipes: the owned structural
checker and the narrow pinned Lean probe. Both cover only `S56-M-0913-INTAKE`; they cover no
canonical obligation, canonical theorem declaration, or accepted proof body. Exact output and
artifact hashes are recorded in `intake-receipt.json`.

## Known open gates

An accepted primary or authoritative source edition and exact theorem passage, complete
definition/assumption/errata crosswalk, independent source review, family arity, set encoding,
coefficient and subtraction convention, binder order, intersection convention, alternate-form
strength, and boundary policy remain open. So do canonical target elaboration,
expression/environment fingerprints, checked transports and mutations, exhaustive
anchor/provenance/trust audits, discovery and obligation freezes, typed graphs, proof and
composition, readable reconstruction, hermetic replay, deterministic bundle, independent
verification, master acceptance, audit completion, and theorem completion.

The assigned intake is self-tested and proposed as worker state `[_]`; only the integration lane
may accept it. These downstream open gates do not invalidate a truthful `planned` intake.
