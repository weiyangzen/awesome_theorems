# THM-M-0005 obligation-tree validation

Item: `S56-M-0005-OBLIGATION_TREE`  
Base revision: `921c8426cee302d0d5c6cd7fe2037c94db1db75f`  
Validation date: 2026-07-12 (Asia/Shanghai)

## Frozen result

Registry version 1 freezes 18 obligations and 51 directed typed edges across separate proof,
refinement, provenance, evidence, trust, documentation, and workflow graphs. Fifteen obligations
are root-relevant machine obligations and three are informational overlays. The denominator SHA-256
is `563eac891739af1e2468c4fd23e7465013f9e5791e069a03e22ccdf67119a762`.

The Lean harness checks that the ten explicit structure fields assemble into
`NaturalKunnethSequence` and that a family of those structures yields the exact root. It assumes
all mathematical fields and closes none. The root remains open at `[H1, M3, R3]`.

## Commands and results

Commands ran from the repository root unless stated otherwise. The canonical pinned `.lake`
closure was reused. No update, build, clone, fetch, or dependency mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets with ranks 1 through 1546 passed. |
| `python3 scripts/stage1_target.py show THM-M-0005` | 0 | Rank 100, planned hard-mathlib lane, theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0005/build_obligation_artifacts.py` | 0 | Deterministically wrote 18 obligations and 51 typed edges with the denominator above. |
| `python3 Stage1_Instances/THM-M-0005/check_obligation_tree.py` | 0 | Input hashes, denominator, node budgets/debts, seven graphs, reciprocal composition, acyclicity, recipes, prohibited tokens, and open-root boundary passed. |
| temporary-source copy followed by `cd Formalizations/Lean && lake env lean -R /tmp/thm-m-0005-olean -o /tmp/thm-m-0005-olean/KunnethStatement.olean /tmp/thm-m-0005-olean/KunnethStatement.lean` | 0 | Built only a temporary statement olean; four known unused-variable warnings. |
| `cd Formalizations/Lean && LEAN_PATH=/tmp/thm-m-0005-olean lake env lean ../../Stage1_Instances/THM-M-0005/ObligationTree.lean` | 0 | Both conditional composition declarations elaborated; `#print axioms` reported only `propext`, `Classical.choice`, and `Quot.sound`. |
| `python3 -m json.tool` on the registry, graph bundle, validation specs, intake, and worker manifest | 0 | All structured artifacts parsed. |
| `git diff --check -- Stage1_Instances/THM-M-0005 .stage1-worker-selftest.json` | 0 | No whitespace errors. |

The temporary olean procedure is necessary because the statement is outside the Lake package root;
all temporary output was placed under `/tmp`, not `.lake`. The pre-existing untracked
`Formalizations/Lean/.lake` link makes this nonrelease evidence.

## Status boundary

This receipt supports only the frozen registry, typed graphs, structured recipes, readable tree,
and conditional composition harness, pending master acceptance. It does not accept a proof node,
source/readability review, transitive trust closure, audit completion, theorem completion, or
release.
