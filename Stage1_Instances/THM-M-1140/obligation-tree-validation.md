# Obligation-tree validation record

Item: `S56-M-1140-OBLIGATION_TREE`  
Base revision: `24c7a19c1a6033b0aed791e0127a3b3e3564a7b0`  
Validation date: 2026-07-12

## Result

Registry version 1 freezes 16 obligations and seven separate typed graphs. The structural checker
recomputes both source hashes and the canonical denominator, checks node schemas, typed-edge
reciprocity and reachability, validates recipe coverage, and fails if the Lean composition source
contains a prohibited proof token.

The narrow Lean run elaborates the exact conditional composition and reports only `propext`,
`Classical.choice`, and `Quot.sound`. This is evidence for the composition interface, not the two
premises. `M1140-T-LOCAL-PACKAGE` and `M1140-T-PROPAGATION-PACKAGE` remain the root cut set; the
root remains `M3` and theorem completion remains false.

## Commands and exact results

| Command | Exit | Result |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-1140/build_obligation_artifacts.py` | 0 | Wrote 16 obligations and the frozen denominator |
| `python3 Stage1_Instances/THM-M-1140/check_obligation_tree.py` | 0 | `PASS THM-M-1140 obligation tree`; 16 obligations and all typed edges validated |
| `LEAN_PATH_BASE=$(cd Formalizations/Lean && lake env printenv LEAN_PATH); LEAN_BIN=$(cd Formalizations/Lean && lake env which lean); cd Stage1_Instances/THM-M-1140; LEAN_PATH="$LEAN_PATH_BASE" "$LEAN_BIN" -o Statement.olean Statement.lean; LEAN_PATH=".:$LEAN_PATH_BASE" "$LEAN_BIN" ObligationTree.lean; rm Statement.olean` | 0 | Narrow temporary statement olean plus conditional composition elaborated; axiom report was `propext`, `Classical.choice`, `Quot.sound`; temporary olean removed |
| `python3 -m json.tool` on all three generated JSON artifacts | 0 | All structured artifacts parsed |
| scoped prohibited-token scan of `ObligationTree.lean` | 1 | No match; exit 1 is ripgrep's expected clean result |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets validated |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-1140` | 0 | Rank 345; planned; L0/rework-required; theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-1140 .stage1-worker-selftest.json` | 0 | No scoped whitespace errors |

Existing pinned `.lake` artifacts were reused. No update, build, clone, fetch, or dependency mutation
was performed. The untracked `.lake` link was pre-existing and is outside the owned target path.
