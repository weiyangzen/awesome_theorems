# THM-M-0982 obligation-tree validation

Item: `S56-M-0982-OBLIGATION_TREE`  
Base revision: `47d9662b1dbcf58d16808c52127e54b6fadb444c`

Validation ran in the worker clone on 2026-07-12. The existing pinned Lake environment was reused;
no update, build, clone, fetch, or dependency mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-0982/build_obligation_artifacts.py` | 0 | generated denominator `e7e587af7868a029493fd68e95b913630d7c0225f2b50d52b5afe10e8008456b` |
| `python3 Stage1_Instances/THM-M-0982/check_obligation_tree.py` | 0 | 11 unique obligations and 23 typed edges; hashes, eligibility projections, node schema, reciprocal proof edges, adjacency, acyclicity, reachability, recipe coverage, and open-root boundary passed |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0982/ObligationTree.lean` | 0 | conditional root composition, measurable-to-null-measurable transport, and probability finite-member lemma elaborated; axiom reports contain `propext`, `Classical.choice`, and `Quot.sound`, with no `sorryAx` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0982` | 0 | rank 262, planned, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0982/{task-dag,instance}.json` (run separately for each file) | 0 | both JSON files parsed |
| `git diff --check -- Stage1_Instances/THM-M-0982` | 0 | no output |

An initial Lean check failed because `NullMeasurableSet` did not specify its measure and the
extended-real top was written with the wrong symbol. Those signatures were corrected; the exact
command above then passed. A first combined shell command also continued from `Formalizations/Lean`
and therefore could not find root-relative scripts; validation was rerun from the repository root
as recorded above.

This phase freezes the below and above branches, both terminal mathlib anchors, the two explicit
above-branch bridges, statement boundaries, foundation, source, and provenance overlays. The root
remains `M3`: proof-module integration, accepted branch receipts, H0, R0, hermetic replay,
independent validation, and theorem completion remain open. Master acceptance is still required.
