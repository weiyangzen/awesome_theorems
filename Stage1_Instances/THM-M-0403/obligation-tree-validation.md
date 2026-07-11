# THM-M-0403 obligation-tree validation

Base revision: `36804d275bde22e8280cb304ab8b40dae4fd5c4e`.

This record validates only the frozen registry and typed architecture. It
does not prove a mathematical node. No dependency was fetched, built,
updated, or modified.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0403` | 0 | rank 16, lifecycle `planned`, baseline L0, legacy artifacts unaccepted, `theorem_complete=false` |
| `python3 Stage1_Instances/THM-M-0403/validate_obligation_tree.py` | 0 | 13 obligations and 22 typed edges; frozen denominator `f58c84024cb1c999c9e59b71040a9342010ae811ca1cd771c88d29e89d224e76` matched; root remained open `M4` |
| `python3 -m json.tool Stage1_Instances/THM-M-0403/obligation-registry.json >/dev/null` | 0 | valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0403/obligation-graphs.json >/dev/null` | 0 | valid JSON |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0403/Statement.lean)` | 1 | `unknown module prefix 'Mathlib'`; the reused canonical `.lake` source checkout lacks the compiled `Mathlib.olean` root |
| `git diff --check -- Stage1_Instances/THM-M-0403 .stage1-worker-selftest.json` | 0 | no whitespace errors |

The structural validator checks the canonical denominator hash, unique and
complete node records, typed endpoint legality, reciprocal adjacency, graph
acyclicity, required-node proof reachability, debt enums, leaf budgets,
eligibility counts, and the open-root boundary.

The Lean replay failure is the environmental known failure recorded by the
prerequisite anchor audit. Worker policy forbids repairing it with `lake
build`, `lake update`, clone, or fetch. It prevents a fresh elaboration replay
but does not invalidate the real structural check of this obligation-tree
deliverable. The root expression hash is inherited from the self-tested
statement receipt and is not promoted to new kernel evidence here.

This worker handoff proposes only `[_]` for
`S56-M-0403-OBLIGATION_TREE`. Master acceptance, all proof bodies,
composition certificates, audit completion, validation, and theorem release
remain outstanding.
