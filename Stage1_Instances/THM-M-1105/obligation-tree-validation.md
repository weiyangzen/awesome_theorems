# Obligation-tree validation record

Item: `S56-M-1105-OBLIGATION_TREE`  
Validation date: `2026-07-12`  
Base revision: `646931af665a6683a1fa53db71b5416bee63abff`

## Frozen architecture

Registry version 1 contains 22 unique obligations. Twenty are machine-required; the source and
provenance nodes are informational overlays and cannot earn proof credit. The selected route is the
bounded-entry moment method: trace expansion, closed-walk classification, suppression of
non-pairings, Catalan leading terms, moment concentration and Borel-Cantelli, tightness, and
bounded-continuous approximation.

The frozen denominator digest is
`409c3f4a4bad0998936fc4dcaeb95488e680948e4e32c5ce542311e982326f0e`.
The root binds the exact statement elaboration output digest
`1f7809988010cf399cf6cabff27fd5630468e795b282002e6286a7f6a39d6769` and source digest
`b7e0e83c6cf2a596e34aa4e8b9b869a05700375a6a4f40b0d4ca3d99a1fdf75b`.

Seven separate typed graphs contain 108 edges. The checker validates schemas, derived
denominators, typed endpoints, proof acyclicity and root reachability, leaf step budgets, source
binding, open composition status, and the absence of placeholder or axiom declarations.
`ObligationTree.lean` checks only the final child-to-root interface: its `terminal` argument is the
open almost-sure weak-convergence obligation, not a proof of it.

## Commands and results

All Lean commands reused the existing pinned artifacts. No update, build, clone, fetch, or `.lake`
mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-1105/build_obligation_artifacts.py` | 0 | built 22 obligations; printed the denominator digest above |
| `python3 Stage1_Instances/THM-M-1105/check_obligation_tree.py` | 0 | PASS; 22 obligations, 108 typed edges; root open at M3 |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1105/ObligationTree.lean)` | 0 | exact terminal-to-root composition interface elaborated; only expected unused-hypothesis linter warnings |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1,546 uniform-L0 targets valid |
| `python3 scripts/stage1_target.py check` | 0 | 1,546 unique targets, ranks 1 through 1,546 |
| `python3 scripts/stage1_target.py show THM-M-1105` | 0 | rank 545; planned; theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1105/obligation-registry.json` | 0 | valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-1105/typed-graphs.json` | 0 | valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-1105 .stage1-worker-selftest.json` | 0 | no output |

## Open root boundary

No obligation has a terminal proof-body identity or accepted closure evidence. The immediate root
cut contains the non-pairing estimate, leading-pairing enumeration, summable concentration,
almost-sure tightness, and bounded-continuous approximation packages. Human pinpoint source review
also remains open. Root debt stays `M3`; this packet establishes architecture only and claims no
`H0`, `M0`, `R0`, audit completion, root closure, or theorem completion.
