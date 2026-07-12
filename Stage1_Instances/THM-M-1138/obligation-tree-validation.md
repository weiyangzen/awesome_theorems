# THM-M-1138 obligation-tree validation

Item: `S56-M-1138-OBLIGATION_TREE`  
Base revision: `c37f5c9477ecee2c5ecf444e75e52be738eff1a8`  
Validation date: `2026-07-12` (`Asia/Shanghai`)

## Result

The deterministic builder froze 15 obligations and seven separate typed graphs. The structural
validator recomputed the denominator digest, bound the registry to the exact statement and anchor
audit inputs, required the full node schema, checked reciprocal proof/composition edges, checked
acyclic root reachability for every required machine obligation, and matched one structured recipe
to every node. The Lean probe checked the exact conditional terminal-to-root composition without
asserting the open analytic premise.

## Commands and exact outcomes

| Command | Exit | Outcome |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-1138/build_obligation_artifacts.py` | 0 | deterministically generated the registry, typed graphs, and 15 validation recipes |
| `python3 Stage1_Instances/THM-M-1138/check_obligation_tree.py` | 0 | 15 obligations and 36 typed edges passed; denominator SHA-256 `a2093825a633069dc09fc9bf1597396052d7f9272bb33f44ace551aa7ba1ca49`; root open at `M3` |
| `cd Formalizations/Lean && lake env lean -R ../../Stage1_Instances/THM-M-1138 -o /tmp/thm-m-1138-lean/Statement.olean ../../Stage1_Instances/THM-M-1138/Statement.lean` | 0 | compiled the exact statement into disposable output outside the repository |
| `cd Formalizations/Lean && LEAN_PATH=/tmp/thm-m-1138-lean lake env lean ../../Stage1_Instances/THM-M-1138/ObligationTree.lean` | 0 | exact conditional composition elaborated; axiom report was `propext`, `Classical.choice`, and `Quot.sound` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1138/Statement.lean` | 0 | exact target and five structural mutations re-elaborated |
| `python3 Stage1_Instances/THM-M-1138/check_statement.py` | 0 | statement expression and source hashes, all five distinguished mutations, and pinned environment passed |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets and ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-1138` | 0 | rank 343, planned, L0/rework-required, theorem incomplete |
| `python3 -m json.tool` on all three generated JSON files | 0 | all structured artifacts parsed |
| prohibited proof-token scan of `ObligationTree.lean` | 1 | clean no-match result for proof placeholders and custom axiom declarations |
| `git diff --check -- Stage1_Instances/THM-M-1138 .stage1-worker-selftest.json` | 0 | no whitespace errors |

The existing pinned `.lake` artifacts were reused without mutation. No dependency update, build,
clone, fetch, or installation was run.

## Status boundary

This self-test supports only the obligation-tree worker handoff. The local strong maximum lemma,
connected propagation, terminal analytic package, node proof bodies, source review, full trust
closure, readable review, hermetic replay, independent verification, `AUDIT-Z`, and `THEOREM-Z`
remain open. Master acceptance is required.
