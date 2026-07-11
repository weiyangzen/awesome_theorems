# Obligation-tree validation record

Item: `S56-M-0390-OBLIGATION_TREE`  
Base revision: `7723e96072c1d3996a280b874d09cfd02a847417`

## Frozen result

Registry version 1 contains fourteen required root-relevant obligations and no exclusions. The
denominator includes the exact root, three exhaustive exponent branches, normalization, the two
special-exponent packages, the Cassels, double-Wieferich, cyclotomic construction, unit, class-group,
and residual-contradiction packages, plus the release trust boundary. Aliases and the one-way
consecutive-power presentation are explicitly non-denominator surfaces.

The typed bundle keeps proof, composition, refinement, provenance, evidence, trust, documentation,
and workflow meanings separate. The proof graph is acyclic. Every mathematical proof node is
reachable from the root; the trust node is connected by a separate `trusts` edge because it is a
release gate, not a proof premise. Only the exact three-branch-to-root composition has a checked
certificate. All child-to-branch compositions remain open.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 groups and 1546 uniform-L0 targets pass |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets pass |
| `python3 scripts/stage1_target.py show THM-M-0390` | 0 | rank 4, planned, L0/rework-required, theorem incomplete |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0390/ObligationTree.lean` | 0 | all branch types print; conditional composition elaborates with no diagnostics |
| `python3 Stage1_Instances/THM-M-0390/validate_obligation_tree.py` | 0 | 14 obligations, 14 proof edges, acyclic root reachability, ledgers at most 100 |
| `python3 -m json.tool` on the registry, graph bundle, and proof-unit manifest | 0 | all three parse as JSON |
| `git diff --check -- Stage1_Instances/THM-M-0390 .stage1-worker-selftest.json` | 0 | no whitespace errors |

An initial Lean attempt to import the sibling source by a filesystem-derived module prefix failed
with `unknown module prefix 'Stage1_Instances'`. No dependency or `.lake` artifact was changed to
work around it. The final standalone module instead repeats the already frozen canonical expression
and checks it by `rfl`; the successful command above is the evidence-bearing run.

Artifact SHA-256 values at validation were:

- `ObligationTree.lean`: `2ef69bba368d6de3453557db94265fa5dfc7fdaae622c2c2de7da5567eaeba1b`
- `obligation-registry.json`: `29127c7c1da0650cb150b7b15f194a624b5e37c0ef9c94e4214ebe8ea510da47`
- `typed-graphs.json`: `228ebac72a1b60b64941b42bf5ebf04b1894c6cb066d0f802203cfb76735e6d7`
- `proof-units.json`: `7881e3970a569d3de4fb8210969e2e43be3f64504dff05f176030d9fbc18ab33`

## Boundary

This self-test accepts the obligation-tree deliverable only. Planned interfaces are not theorem
declarations, and compact ledgers do not make the deep packages terminal leaves: recursive source
and proof expansion remains mandatory. The run is not a cold, hermetic, or independent release
replay. Root status remains `H2/M3/R4`; audit completion and theorem completion remain false.
