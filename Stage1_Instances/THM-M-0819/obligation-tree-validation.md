# THM-M-0819 obligation-tree validation

Item: `S56-M-0819-OBLIGATION_TREE`

Base revision: `dc600635160cace0916df5234bf8808c39dc656d`

Base tree: `8ee34b31ec38be1ef067aaab38c9a4cb4935b75a`

Validation date: `2026-07-14` (`Asia/Shanghai`)

## Frozen Result

Registry version 1 freezes 33 canonical obligations before proof status. Its 85 structured steps
make the high-risk finite-to-global route explicit without treating planned steps as proof. The canonical ten-field
projection has SHA-256
`3e19428b16575891198438f798957373f440bf15623c22c44df4c1f69239742c`.
The complete frozen registry scope has SHA-256
`745b3cd0536f5a84912eeaa88a41b0b26a39158ed81a47b66850e51cb0fae1f8`.
The graph bundle has 154 directed edge records in separate proof, refinement, provenance, evidence,
trust, documentation, and workflow indexes. Five reverse proof edges have exact conditional Lean
composition support; twelve open parent plans cover 31 deeper `logical_decomposition` relations.
This item freezes generic `T01`-`T03`; those internal certificates remain downstream proof/C01 work.

The architecture preserves the primary arbitrary-poset statement. It splits `k = 0` from positive
width, expands the visible finite-proof opening without inventing the uninspected tail, and selects
an explicit finite-restriction, local-coloring, Rado-selection, global-fiber route for the general
carrier. `Finset.rado_selection_subtype` was not classified by predecessor anchor inventory version
1, so a successor anchor/provenance audit is required before proof credit. The external finite ENat
equality remains scope-inexact and current-pin failing.

## Commands And Exact Results

The initial worker status contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink. Existing pinned artifacts were reused read-only. No
`lake update`, `lake build`, dependency clone/fetch, checkout, install, or `.lake` mutation ran.

| Command | Exit | Exact result and boundary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, all 1,546 uniform-L0 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1,546 unique targets at ranks 1 through 1,546 passed |
| `python3 scripts/stage1_target.py show THM-M-0819` | 0 | rank 1,377; planned L0/rework-required; legacy evidence unaccepted; theorem incomplete |
| `git status --short --untracked-files=all` before editing | 0 | only the pre-existing automation-provided `Formalizations/Lean/.lake` symlink |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree above |
| `python3 -B Stage1_Instances/THM-M-0819/build_obligation_artifacts.py` | 0 | wrote 33 obligations and 154 typed edge records; denominator `3e19428b...742c` |
| repeat the generator and compare generated JSON SHA-256 lines | 0 | `obligation-registry.json`, `typed-graphs.json`, and `validation-specs.json` were byte-identical |
| `python3 -B Stage1_Instances/THM-M-0819/check_obligation_tree.py` | 0 | predecessor/target identity, deterministic artifacts, closed field contracts, exclusions, mandatory layers, 33 ledgers/anchors and one bundle recipe, typed endpoint reciprocity/reachability/acyclicity, pins, Rado substrate, Lean hygiene, receipt, packet, and false-completion boundary passed |
| temporary `Statement.olean` compilation and `lake env lean ../../Stage1_Instances/THM-M-0819/ObligationTree.lean` with the temporary directory prepended to `LEAN_PATH` | 0 | statement stdout SHA-256 `abf1d640...3134`; harness stdout SHA-256 `005cb8a5...2419`; all declarations sorry-free; exact interfaces serialized; no recovery hole |
| `python3 -m json.tool` on the registry, graph bundle, validation specs, receipt, and worker packet | 0 | all structured artifacts parsed |
| Python `ast.parse` on builder/checker and `py_compile` with `PYTHONPYCACHEPREFIX=/tmp/stage1-m0819-obligation-pycache` | 0 | both scripts parsed and compiled without owned-path cache output |
| comment-aware prohibited-construct scan over `ObligationTree.lean` | expected no match | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `unsafe`, `opaque`, external implementation, native oracle, or placeholder declaration |
| `git diff --check -- Stage1_Instances/THM-M-0819 .stage1-worker-selftest.json` plus per-file `git diff --no-index --check /dev/null` for untracked files | 0 aggregate | no whitespace diagnostics |

The Lean harness reports only `propext` for `zeroWidth_of_statement` and the combined
`root_of_positiveWidth`; its other five checked composition declarations report no axioms.
`PositiveWidthPackage` is an explicit premise for which no inhabitant is supplied or credited. Thus
the run checks exact conditional
composition and the local zero boundary, not Dilworth's positive-width theorem.

## Status Boundary

Accepted closed obligations and accepted receipts are empty. The minimal open machine proof cut is
`M0819-B-WIDTH-POSITIVE`. The root remains `[H1, M3, R3]`; `audit_complete=false` and
`theorem_complete=false`. Primary-source `H0`, the finite proof tail, an exact positive-width proof,
the Rado successor provenance audit, complete composition/provenance/TCB, reviewed `R0`, hermetic
replay, independent verification, validation, release, and master acceptance remain open.
