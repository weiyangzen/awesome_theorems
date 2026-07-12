# THM-M-0330 obligation-tree validation

Item: `S56-M-0330-OBLIGATION_TREE`. Base revision:
`3d8dd27e4ff1200a2d9c8daaa9cae8072eca6241`.

Validation ran from the worker clone on 2026-07-12. Existing pinned Lake
artifacts were reused; no dependency update, fetch, clone, or build was run.

```text
python3 Stage1_Instances/THM-M-0330/build_obligation_artifacts.py
  exit 0
  f173d7dfb3e01916776f2e78183615c1d439b1041e1918c14a1dd719032ea29a

python3 Stage1_Instances/THM-M-0330/check_obligation_tree.py
  exit 0
  PASS THM-M-0330 obligation tree: 19 obligations, 40 typed edges
  registry denominator sha256: f173d7dfb3e01916776f2e78183615c1d439b1041e1918c14a1dd719032ea29a
  root closure: open (M4); exact forward and converse packages remain open

cd Formalizations/Lean &&
  lake env lean ../../Stage1_Instances/THM-M-0330/ObligationTree.lean
  exit 1
  input file must be contained in the Lake root directory

cd Stage1_Instances/THM-M-0330 &&
  LEAN_PATH=$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
    lake env lean -o Statement.olean Statement.lean
  exit 1
  error: no default toolchain configured

LEAN=$(cd Formalizations/Lean && lake env which lean) &&
LP=$(cd Formalizations/Lean && lake env printenv LEAN_PATH) &&
cd Stage1_Instances/THM-M-0330 &&
LEAN_PATH="$LP" "$LEAN" -o Statement.olean Statement.lean &&
LEAN_PATH=".:$LP" "$LEAN" ObligationTree.lean
  exit 0
  root_of_direction_packages depends on axioms:
    [propext, Classical.choice, Quot.sound]
  Statement.olean removed after the scoped check
```

The two failed invocations are retained as evidence rather than hidden. The
successful retry uses the exact pinned executable returned by `lake env which
lean` and the pinned dependency path returned by `lake env printenv
LEAN_PATH`; it does not configure or mutate Elan or Lake.

This validates registry hashes and denominators, all required node fields,
typed reciprocal proof edges, adjacency, proof-DAG reachability, recipe
coverage, exact directional interfaces, exact root output, placeholder
hygiene, elaboration, and the conditional composition's axiom surface. It
does not prove either direction. There is no accepted receipt; master
acceptance remains required.

Final repository checks also passed: `python3
Docs/tools/check_stage1_standard.py`, `python3 scripts/stage1_target.py check`,
`python3 scripts/stage1_target.py show THM-M-0330`, and `git diff --check --
Stage1_Instances/THM-M-0330` all exited 0. The target remains rank 823,
uniform `L0 / rework_required`, `planned`, and `theorem_complete: false`.
