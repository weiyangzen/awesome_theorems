# Obligation-tree validation receipt

Node: `S56-M-1244-OBLIGATION_TREE`. Base revision:
`58cde546113e54bfa95299c69db6ee1508316872`. Date: 2026-07-12. The pre-existing
untracked `Formalizations/Lean/.lake` link was reused read-only. No Lake update, build, dependency
clone, or fetch was run.

## Commands and exact results

| Command | Exit | Result |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-1244/build_obligation_artifacts.py` | 0 | generated 18 obligations; denominator `edecb957b6903682647ae02dbfff3d6bdd693e6ddf2decd18721fdcae702c297` |
| `python3 Stage1_Instances/THM-M-1244/check_obligation_tree.py` | 0 | PASS: 18 obligations, 36 typed edges; exact root remains open M4 |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets with ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1244` | 0 | rank 425; planned; L0/rework-required; theorem incomplete |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1244/ObligationTree.lean` | 1 | expected module-path setup failure: `Statement` was outside Lake's package search root; no validation credit |
| `LEAN=$(cd Formalizations/Lean && lake env which lean); BASE=$(cd Formalizations/Lean && lake env printenv LEAN_PATH); TARGET=Stage1_Instances/THM-M-1244; LEAN_PATH="$BASE:$TARGET" "$LEAN" -R "$TARGET" "$TARGET/Statement.lean" -o "$TARGET/Statement.olean"; LEAN_PATH="$BASE:$TARGET" "$LEAN" -R "$TARGET" "$TARGET/ObligationTree.lean"; rm -f "$TARGET/Statement.olean" "$TARGET/Statement.ilean"` | 0 | pinned Lean 4.29.0 checked both conditional packages and exact child-to-root composition; `#print axioms` reported `[propext, Classical.choice, Quot.sound]`; temporary interface artifacts removed |
| `python3 -m json.tool Stage1_Instances/THM-M-1244/{obligation-registry.json,typed-graphs.json}` (run once per file) | 0 | both structured artifacts are valid JSON |
| placeholder scan over `Statement.lean`, `AnchorAudit.lean`, and `ObligationTree.lean` | 0 | no `sorry`, `admit`, or axiom declaration |
| `git diff --check -- Stage1_Instances/THM-M-1244 .stage1-worker-selftest.json` | 0 | no scoped whitespace errors |

## Result boundary

The registry projection hash, independent denominator lists, required node schema, typed endpoints,
reciprocity, proof reachability and acyclicity, and truthful open-root boundary are self-tested. Lean
checks only that the two explicit package premises compose to the exact frozen root. Neither package
is constructed, the external project is not imported, and no theorem-completion claim is made.
H0/R0, trust closure, hermetic replay, master acceptance, and theorem completion remain open.
