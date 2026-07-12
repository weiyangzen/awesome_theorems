# THM-M-1005 obligation-tree validation

Item: `S56-M-1005-OBLIGATION_TREE`  
Base revision: `bafc08f4d75222633812affc69d9f5b903037bea`  
Validation date: `2026-07-12` (`Asia/Shanghai`)

## Result

The deterministic builder froze 14 obligations and seven separate typed graphs. The validator
recomputed the denominator digest, checked the exact statement and anchor-audit input hashes,
required the full node schema, checked unique reciprocal graph edges, proved the combined
proof/refinement graph acyclic and root-reaching for every required machine obligation, and checked
one validation recipe per node. The Lean probe elaborated the exact conditional terminal-to-root
composition with no placeholder, custom axiom, or proof of the open analytic premise.

## Commands and exact outcomes

| command | exit | outcome |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets and ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-1005` | 0 | rank 285, planned, L0/rework-required, theorem incomplete |
| `python3 Stage1_Instances/THM-M-1005/build_obligation_artifacts.py` | 0 | deterministically generated registry, graph bundle, and 14 structured recipes |
| `python3 Stage1_Instances/THM-M-1005/check_obligation_tree.py` | 0 | 14 obligations and 48 typed edges passed; root open M3 |
| `(cd Formalizations/Lean && lake env lean -R ../../Stage1_Instances/THM-M-1005 -o /tmp/thm-m-1005-lean/Statement.olean ../../Stage1_Instances/THM-M-1005/Statement.lean)` | 0 | compiled the exact statement module to a disposable output outside the repository |
| `(cd Formalizations/Lean && LEAN_PATH=/tmp/thm-m-1005-lean lake env lean ../../Stage1_Instances/THM-M-1005/ObligationTree.lean)` | 0 | exact conditional composition elaborated; axiom report contained only `propext`, `Classical.choice`, and `Quot.sound` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1005/Statement.lean)` | 0 | exact frozen target and statement mutations re-elaborated |
| `python3 Stage1_Instances/THM-M-1005/check_statement.py` | 0 | statement fingerprint, mutations, and pinned environment passed |
| `python3 -m json.tool` on all three generated JSON files | 0 | valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-1005 .stage1-worker-selftest.json` | 0 | no whitespace errors |

The existing pinned `.lake` artifacts were reused without mutation. No `lake update`, `lake build`,
dependency clone, fetch, or installation was run.

## Status boundary

This self-test supports only the obligation-tree worker handoff. The strong analytic estimate,
node proof bodies, source review, full trust closure, readable review, hermetic reproduction,
independent verification, `AUDIT-Z`, and `THEOREM-Z` remain open. Master acceptance is required.
