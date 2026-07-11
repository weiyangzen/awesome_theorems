# Obligation-tree validation

Item: `S56-M-0441-OBLIGATION_TREE`  
Base revision: `5b896ef8cd453b31d9dfc6f96e8db864ae521cfa`

The registry is content-bound to `Statement.lean` SHA-256
`a0a7c75b5402d43a447bfc5e5c4f42a2989ae2ee4c126ed0a33e507873db563b` and
`anchor-audit.json` SHA-256
`976ebdaf0a586900bbe418dbc769bcc2d2a580feed4e9718eb5fb21459f145b2`.

## Validation

| Command | Exit | Result |
|---|---:|---|
| `lake env lean -R ../.. -o /tmp/thm-m-0441-obligation/Statement.olean ../../Stage1_Instances/THM-M-0441/Statement.lean && LEAN_PATH="/tmp/thm-m-0441-obligation:${LEAN_PATH:-}" lake env lean -R ../.. ../../Stage1_Instances/THM-M-0441/ObligationTree.lean` from `Formalizations/Lean` | 0 | statement and obligation module elaborated; `engine_compose` reports only `propext`, `Classical.choice`, and `Quot.sound` |
| `python3 Stage1_Instances/THM-M-0441/check_obligation_tree.py` | 0 | PASS: 21 obligations, 18 proof edges, root open |
| `python3 -m json.tool Stage1_Instances/THM-M-0441/obligation-registry.json` | 0 | registry JSON parsed |
| `python3 -m json.tool Stage1_Instances/THM-M-0441/typed-graphs.json` | 0 | typed graph JSON parsed |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546-target coverage passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique uniform-L0 targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-0441` | 0 | rank 87, planned, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-0441 .stage1-worker-selftest.json` | 0 | no whitespace errors |

The validator intentionally requires `root_closed=false`, no credited closed
obligations, a unique human-only source exclusion, seven distinct graph
families, acyclic proof reachability, and all numeric leaves at 100 steps or
fewer. Validation of this phase is not validation of a Pila-Wilkie proof.

Phase verdict: the obligation registry and typed graphs are self-tested pending
master acceptance. Known failures are deliberate and substantive: the exact
root has no proof body, all four mathematical engine inputs are uninhabited,
and human-source, readable reconstruction, transitive trust, hermetic replay,
and independent-review gates remain open.
