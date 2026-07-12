# Obligation-tree validation

Assigned item: `S56-M-0536-OBLIGATION_TREE`. Base revision:
`ed4c9bd55f9fcfd10e711dd571aceaedd188fbcc`.

The registry contains 15 unique semantic obligations and 37 typed edges. Its frozen denominator is
`93dfa3abec1ea8cc493fd90ed12ad7a90b1439bcc5bff218573e112bf80487c9`.
The structural validator recomputes that hash, verifies all required node fields, reciprocal proof
edges, endpoints, indices, proof acyclicity and root reachability, validation-spec coverage, source
and anchor hashes, and the fail-closed root boundary.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-0536/build_obligation_artifacts.py` | 0 | Wrote 15 obligations and 37 typed edges; printed the frozen denominator hash. |
| `python3 Stage1_Instances/THM-M-0536/check_obligation_tree.py` | 0 | Structural, hash, reciprocity, DAG, schema, and open-root assertions passed. |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0536/ObligationTree.lean` | 0 | Standalone exact-target restatement and conditional composition elaborated; axioms were `propext`, `Classical.choice`, and `Quot.sound`. |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0536/Target.lean` | 0 | Canonical target still elaborated. |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets accepted. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets in ranks 1 through 1546. |
| `python3 scripts/stage1_target.py show THM-M-0536` | 0 | Rank 593; planned; L0/rework-required; theorem incomplete. |
| JSON parsing of all owned JSON artifacts | 0 | All files parsed. |
| prohibited-token scan over owned Lean files | 1 | Expected no-match exit: no `sorry`, `admit`, `axiom`, or `sorryAx`. |
| `git diff --check -- Stage1_Instances/THM-M-0536 .stage1-worker-selftest.json` | 0 | No whitespace errors. |

Status boundary: this receipt supports the frozen obligation denominator, typed architecture, and
conditional composition only. `InducedInverseLaws` remains the first proof-phase cut; no accepted
root proof, H0, R0, audit completion, theorem completion, hermetic release, or independent review is
claimed.
