# THM-M-1237 obligation-tree validation

Base revision: `c03519b15d342c7ab9b4fab75bfaa01ed0015c8e`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-1237/build_obligation_artifacts.py` | 0 | Deterministically built 10 obligations and 32 typed edges |
| `python3 Stage1_Instances/THM-M-1237/check_obligation_tree.py` | 0 | Registry hashes, required node fields, typed reciprocal proof edges, reachability, acyclicity, cut set, and open closure boundary passed |
| `lake env lean -R ../../Stage1_Instances/THM-M-1237 -o /tmp/thm-m-1237-lean/Statement.olean ../../Stage1_Instances/THM-M-1237/Statement.lean` (from `Formalizations/Lean`) | 0 | Built the already validated local statement module in disposable `/tmp`, without mutating `.lake` |
| `LEAN_PATH=/tmp/thm-m-1237-lean:$LEAN_PATH lake env lean ../../Stage1_Instances/THM-M-1237/ObligationTree.lean` (from `Formalizations/Lean`) | 0 | Exact child-to-root composition elaborated; axiom report was `[propext, Classical.choice, Quot.sound]` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Rev-5.6 standard and 1546-target projection passed |
| `python3 scripts/stage1_target.py check` | 0 | Ordered 1546-target manifest passed |
| `python3 scripts/stage1_target.py show THM-M-1237` | 0 | Rank 175, L0/rework-required, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-1237 .stage1-worker-selftest.json` | 0 | No whitespace errors |

This phase freezes architecture and checks composition only. The analytic premises are not proved;
theorem completion, audit completion, validation, release, and master acceptance remain outstanding.
