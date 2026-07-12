# Obligation-tree validation record

Item: `S56-M-1060-OBLIGATION_TREE`  
Validation date: `2026-07-12`  
Base revision: `d2ae10f04ec1ce6f3602351f9b9d9a36e4ccec6e`

## Frozen architecture

Registry version 1 contains 21 unique semantic obligations. Nineteen are
machine-required; `M1060-X-SOURCE` and `M1060-X-PROVENANCE` are informational
overlays and cannot earn proof credit. The required route is the classical
dyadic polygonal-approximation architecture: finite Gaussian LDP, interpolation,
Brownian exponential approximation, transfer to path space, exact rate
identification, and compact Cameron-Martin sublevels.

The frozen denominator digest is
`32d2df11f1dd7faa40b53ee0ae86fc93d52317f80c4d3e9c1f8bcbe00b2a3f74`.
The root fingerprint is the SHA-256 of the exact printed elaboration from
`Statement.lean`, and `typed-graphs.json` separately binds the source file hash
`d2bfdc20fcb2cd7c3de27588917dad689056d73e05880814590ab1e3c604581a`.

Seven typed graphs contain 83 reciprocal edges. Proof, refinement, provenance,
evidence, trust, documentation, and workflow semantics remain separate. The
structural checker verifies unique IDs, complete schemas, denominator derivation,
source binding, reciprocal edges, acyclic proof reachability to the root, step
budgets, composition records, and the fail-closed completion boundary.

`ObligationTree.lean` kernel-checks only the two child-to-parent composition
interfaces. Its lower-bound, upper-bound, and goodness arguments are explicit
hypotheses representing open registered children. It is not a Schilder proof.

## Commands and results

All Lean commands reused the existing pinned closure. No dependency update,
build, clone, or fetch was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-1060/build_obligation_artifacts.py` | 0 | built 21 obligations; printed denominator digest above |
| `python3 Stage1_Instances/THM-M-1060/check_obligation_tree.py` | 0 | PASS; 21 obligations, 83 typed edges, open M4 root |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1060/ObligationTree.lean` | 0 | both exact composition-interface declarations elaborated |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1060/Statement.lean \| sha256sum` | 0 | `a5d3c4...ab7f8  -` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1,546 uniform-L0 targets valid |
| `python3 scripts/stage1_target.py check` | 0 | 1,546 unique targets, ranks 1 through 1,546 |
| `python3 scripts/stage1_target.py show THM-M-1060` | 0 | rank 503; planned; theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-1060 .stage1-worker-selftest.json` | 0 | no output |

## Open root boundary

No obligation has a terminal proof-body ID or accepted closure evidence. The
minimal reported implementation cut contains finite Gaussian LDP, Brownian
modulus tails, exponential-equivalence transfer, rate identification, rate
lower semicontinuity, and sublevel equicontinuity. Root debt is conservatively
`M4`; human pinpoint review remains `H2`; readability remains `R4`.

This packet self-tests only the architecture freeze pending master acceptance.
It does not claim `H0`, `M0`, `R0`, `AUDIT-Z`, root closure, or theorem completion.
