# THM-M-0833 intake validation

Base revision: `be8701e88e791545c16a262edd1909486d5cef4b` (tree
`78b0a751473bf6d71f453a6aad18b130268a3428`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers the planned dossier, scope and non-substitution boundaries, source-statement
crosswalk, six-node open task DAG, and a narrow pinned Lean coloring-API probe. It does not validate
a canonical Four Color proposition or proof because planarity, representation, and exact source
scope remain unfrozen. The automation-provided canonical `.lake` symlink was pre-existing and used
read-only; no dependency update, build, clone, fetch, or other `.lake` mutation was performed. This
dirty worker run is nonrelease evidence.

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
- The pre-existing `.lake` symlink target string has SHA-256
  `e8714e9ebb75a5da1eeb16fdb6f50831a6cab29f115df43fa8e7535b38f59826`.

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0833` | exit 0; rank 1391, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | preflight exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before intake |
| `git rev-parse HEAD 'HEAD^{tree}'` | exit 0; base revision and tree recorded above |
| `git blame -L 6117,6122 -- Docs/researches/math_theorems.md` | exit 0; all six uncited catalog lines originate in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| HAL API query and inspection of `https://inria.hal.science/hal-04034866/document` | exit 0; Gonthier's 58-page authoritative report, Section 2 statement/definitions, displayed `four_color` target, and Sections 2-3 reductions inspected; observed PDF SHA-256 `ff10a58370486b0299cedf1203b72f0c94dbde82451cc48c1e41959e58026301`; source lead only |
| GitHub API queries for `rocq-community/fourcolor` at `f2fcc837b817632f334f9c7d7fbb0195ad4ba4e2` | exit 0; tree `b2da69f860096cce9480f2645298a2d04587f360`, README, `fourcolor.v`, and `combinatorial4ct.v` inspected without cloning; external Rocq/Coq lead only |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0; empty output |
| bounded searches for Four Color and planar-graph declarations in pinned mathlib and tracked Lean | completed; the coloring module marks planar graphs TODO and no Four Color or target-specific declaration was found; intake discovery only |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0833/IntakeProbe.lean)` | exit 0; eight graph/coloring APIs elaborated; stdout SHA-256 `784d85d99be0050818c297953323b84fdb6618019d6b244492781cc37f3f6ea5`; representative axiom reports contain only `propext`, `Classical.choice`, and `Quot.sound`; no target theorem |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | exit 0 for each after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0833-pycache python3 -m py_compile Stage1_Instances/THM-M-0833/check_intake.py` | exit 0; scoped validator compiled without adding generated files to the owned path |
| `python3 -B Stage1_Instances/THM-M-0833/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0 after finalization; manifest/DAG identity, source and pin hashes, null Lean target, H1/M3/R3 boundary, receipt/packet, and six open tasks agree |
| `rg -n -e '\bsorry\b' -e '\badmit\b' -e '\bsorryAx\b' -e '\baxiom\b' -e '\bconstant\b' -e '\bopaque\b' -e '\bunsafe\b' Stage1_Instances/THM-M-0833 --glob '*.lean'` | exit 1 as expected; no prohibited declaration in the API-only probe |
| scoped `awk` trailing-whitespace checks on every new file plus `git diff --check` | exit 0; no whitespace diagnostics |

## Known open gates

An independently reviewed immutable source must select the graph or map root and freeze planarity,
finiteness, embedding, simplicity, region adjacency, graph-map transports, colorability, binders,
foundations, computation policy, and boundary cases. So do the canonical Lean expression and
environment fingerprints, checked transports, statement mutations, exhaustive formal anchor audit,
external Rocq/Coq terminal-body provenance, discovery protocol, obligation registry, typed graphs,
proof and composition, trust/provenance closure, readable reconstruction, hermetic replay,
deterministic bundle, independent verification, master acceptance, audit completion, and theorem
completion. These open gates do not invalidate a truthful self-tested `planned` intake.

