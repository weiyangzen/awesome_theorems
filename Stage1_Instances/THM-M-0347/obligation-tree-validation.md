# Obligation-tree validation

Item: `S56-M-0347-OBLIGATION_TREE`  
Base revision: `396f523f7db5499e43d86728d9cfe073ac081dfa`

The registry freezes 15 canonical obligations and seven separate typed graphs. The required machine
denominator contains the exact root, statement interface, convolution reduction, kernel construction,
four analytic packages, conditional assembly, and foundation boundary. Source, provenance,
documentation, trust, and workflow nodes cannot be counted as proof premises.

## Commands and results

All commands ran inside this worker clone. The Lean check used the pinned executable and dependency
path from `Formalizations/Lean`. It wrote only temporary `/tmp/Statement.olean` import artifacts and
removed them afterward; it did not update or modify `.lake`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-0347/build_obligation_artifacts.py` | 0 | Generated registry, seven typed graphs, and structured recipes; denominator SHA-256 `01ec6fc2f46c410770093c63f64aacff21537af51959956e4c041faa20c80bde`. |
| `python3 Stage1_Instances/THM-M-0347/check_obligation_tree.py` | 0 | Validated 15 unique obligations, all required node fields and budgets, 73 typed reciprocal/indexed edges, proof DAG reachability, recipe coverage, frozen input hashes, and open-root boundary. |
| `LEAN_DEPS=$(cd Formalizations/Lean && lake env printenv LEAN_PATH); LEAN_BIN=$(cd Formalizations/Lean && lake env which lean); cd Stage1_Instances/THM-M-0347; LEAN_PATH="$LEAN_DEPS" "$LEAN_BIN" -o /tmp/THM-M-0347-Statement.olean Statement.lean; cp /tmp/THM-M-0347-Statement.olean /tmp/Statement.olean; LEAN_PATH="/tmp:$LEAN_DEPS" "$LEAN_BIN" ObligationTree.lean; rm -f /tmp/Statement.olean /tmp/THM-M-0347-Statement.olean` | 0 | Exact statement and conditional composition elaborated; `#print axioms` reported `propext`, `Classical.choice`, and `Quot.sound`. |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Standard structure accepted all 1546 uniform-L0 targets. |
| `python3 scripts/stage1_target.py check` | 0 | Manifest accepted 1546 unique targets at ranks 1 through 1546. |
| `python3 scripts/stage1_target.py show THM-M-0347` | 0 | Confirmed rank 840, planned L0/rework-required target, with theorem completion false. |
| `git diff --check -- Stage1_Instances/THM-M-0347 .stage1-worker-selftest.json` | 0 | No whitespace errors. |

## Status boundary

Only the architecture and the child-to-root interface are self-tested. `UniformFejerEstimate` is an
explicit premise, not an axiom or proof body. The convolution identity, kernel construction,
positivity, mass, concentration, uniform-continuity estimate, source map, complete provenance/trust
closure, readable reconstruction, and release receipts remain open. Root machine debt remains `M3`;
`theorem_complete` remains false. Master acceptance is still required for this obligation-tree item.
