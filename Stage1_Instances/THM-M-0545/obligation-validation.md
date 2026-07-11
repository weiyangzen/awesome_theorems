# THM-M-0545 obligation-tree validation

Item: `S56-M-0545-OBLIGATION_TREE`  
Base revision: `6ba79369e24bfba400ebdfd7dbacd4fd64e18d2c`  
Validation date: `2026-07-12` (`Asia/Shanghai`)

## Result

The deterministic builder froze 17 obligations and seven separately typed graphs. The validator
recomputed the registry denominator, bound the freeze to the exact statement and anchor-audit file
hashes, checked every required node field and semantic ledger, verified reciprocal graph indexes,
proved proof/refinement root reachability and acyclicity for all 15 required machine obligations,
and enforced an open `M4` root. There are 132 typed edges. The two informational overlays cannot
contribute machine proof credit.

The exact statement re-elaborated with the pinned Lean executable. The existing untracked
`Formalizations/Lean/.lake` link was reused and not modified. No dependency update, build, clone,
or fetch ran.

## Commands and exact outcomes

| Command | Exit | Outcome |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ranks and targets passed |
| `python3 scripts/stage1_target.py show THM-M-0545` | 0 | rank 105, planned, L0/rework-required, theorem incomplete |
| `python3 Stage1_Instances/THM-M-0545/build_obligation_artifacts.py` | 0 | wrote 17 obligations; denominator `52a39eb004a0689d978588caae3599283b4573967e97d66a8b8eb6caaae9896e` |
| `python3 Stage1_Instances/THM-M-0545/check_obligation_tree.py` | 0 | `PASS`: 17 obligations, 132 typed edges; root open M4 |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0545/Statement.lean)` | 0 | exact target and checked direct expansion elaborated |
| `python3 -m json.tool Stage1_Instances/THM-M-0545/obligation-registry.json` | 0 | valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0545/typed-graphs.json` | 0 | valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-0545 .stage1-worker-selftest.json` | 0 | no whitespace errors |

Final artifact hashes:

```text
7846553600eadbefe981c563071055292c6a714d38448cdc02d227a38d46fd04  obligation-registry.json
83bd6ca7107a2bed3d28660be0ed5139913079f1f17c50718cb64dd36d2e43e7  typed-graphs.json
```

## Status boundary

This self-tests only the obligation architecture freeze. It supplies no analytic construction,
composition certificate, primary-source acceptance, proof body, audit completion, or theorem
completion. The root remains `M4`; master acceptance is still required for this scheduler item.
