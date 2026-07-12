# Obligation-tree validation

Base revision: `2eb836c21ebdba77082dcafd9222259988e44a54`.

The registry was frozen against canonical statement expression
`7a9628fca04eb72d787efad1f852517f4385377b3ad16f3eba662ccea4bb86a5` and the current immutable
anchor-audit artifact. It contains 30 unique obligations and a content-derived denominator
`9963eb2002e7418a51e79b3ed2dd651e2c29a701cdfa1e18f47123041207f9ac`. All required machine
obligations are reachable from the root through typed proof or refinement edges.

`ObligationTree.lean` is checked by concatenating it after the already validated `Statement.lean`
source in a temporary file. This is necessary because the worker invokes individual source files
without building a repository-local `.olean`; it does not mutate `.lake`. The resulting declaration
has the exact canonical target and explicitly consumes both root children. Its reported axioms are
`propext`, `Classical.choice`, and `Quot.sound`; no new custom axiom is introduced.

| Command | Result |
|---|---|
| `python3 Stage1_Instances/THM-M-0321/build_obligation_artifacts.py` | exit 0; wrote 30 obligations and 33 typed edges |
| `python3 Stage1_Instances/THM-M-0321/check_obligation_tree.py` | exit 0; denominator, schemas, eligibility projections, typed reciprocity, acyclicity, reachability, open closure boundary, and conditional Lean composition checked |
| `python3 -m json.tool Stage1_Instances/THM-M-0321/obligation-registry.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0321/typed-graphs.json` | exit 0 |
| `git diff --check -- Stage1_Instances/THM-M-0321` | exit 0; no whitespace errors |

This is scoped, dirty-tree, nonrelease worker evidence. Both substantive proof packages remain
open, primary-source pinpointing remains `H2`, readable review remains `R4`, and the root remains
`M3`. No obligation closure, accepted state, audit completion, or theorem completion is claimed.
