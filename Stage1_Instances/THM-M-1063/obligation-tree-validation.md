# Obligation-tree validation record

Item: `S56-M-1063-OBLIGATION_TREE`  
Validation date: `2026-07-12` (`Asia/Shanghai`)  
Base revision: `c69176e94b59c24862294d8331b61eb1661c53bd`

## Frozen architecture

Registry version 1 contains 31 unique semantic obligations. Twenty-nine are
machine-required. `M1063-X-SOURCE` and `M1063-X-PROVENANCE` are informational
overlays and cannot earn proof credit. The selected route keeps finite-dimensional
convergence, finite-second-moment truncation, uniform tightness, subsequential
weak convergence, Brownian-law uniqueness, and final API transport as distinct
obligations. In particular, the pinned scalar CLT is only a bridge leaf.

The frozen denominator digest is
`a55c3e289a005535836506a2ce233e3dbb5fa0a7b84717b38c221583d26a7703`.
The root fingerprint is the SHA-256 of the exact printed elaboration from
`DonskerTarget.lean`, and the typed graph bundle separately binds the target
source file hash.

Seven typed graphs contain 125 reciprocal edges. The checker validates unique
IDs, the full node schema, denominator derivation, source binding, reciprocal
indexes, proof-DAG acyclicity and root reachability, leaf budgets, and the
fail-closed completion boundary. `ObligationTree.lean` checks only an exact-root
identity interface. Its hypothesis is the complete open Donsker proposition;
it is deliberately not proof evidence.

## Commands and exact results

All Lean commands reused the existing pinned closure. No Lake update, build,
clone, fetch, or dependency mutation was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-1063/build_obligation_artifacts.py` | 0 | built 31 obligations; denominator digest above |
| `python3 Stage1_Instances/THM-M-1063/check_obligation_tree.py` | 0 | PASS; 31 obligations, 125 typed edges, open M4 root |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1063/DonskerTarget.lean \| sha256sum` | 0 | `a5bb2e24...42c81  -` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1063/ObligationTree.lean` | 0 | exact-root identity interface elaborated at universes `u`, `v` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1,546 uniform-L0 targets valid |
| `python3 scripts/stage1_target.py check` | 0 | 1,546 unique targets, ranks 1 through 1,546 |
| `python3 scripts/stage1_target.py show THM-M-1063` | 0 | rank 506; planned; L0/rework-required; theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1063/obligation-registry.json` | 0 | valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-1063/typed-graphs.json` | 0 | valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-1063 .stage1-worker-selftest.json` | 0 | no output |

## Open root boundary

No obligation has a terminal proof-body ID or accepted closure evidence. The
reported implementation cut includes the weighted triangular-array CLT,
finite-second-moment modulus control, Arzela-Ascoli compact containment,
Prokhorov subsequence extraction, continuous-path law uniqueness, and the final
`TendstoInDistribution` bridge. Root debt remains `H2 / M4 / R4`.

This packet self-tests only the obligation architecture pending master
acceptance. It claims no proof, `H0`, `M0`, `R0`, audit completion, root closure,
or theorem completion.
