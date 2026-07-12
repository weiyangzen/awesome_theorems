# THM-M-0992 obligation-tree validation

Item: `S56-M-0992-OBLIGATION_TREE`. Base revision:
`ac680cc80e4b42c3cb2c59fc038ab8c5c5fb5e16`.

Validation ran in the worker clone on 2026-07-12. It reused the canonical
pinned Lake dependency environment. No update, build, fetch, or clone was run.

```text
python3 Stage1_Instances/THM-M-0992/build_obligation_artifacts.py
  exit 0
  264632006226a217d9201ddea30cef426514f8411eb5439e8063c67151392359

python3 Stage1_Instances/THM-M-0992/check_obligation_tree.py
  exit 0
  PASS THM-M-0992 obligation tree: 8 obligations, 16 typed edges
  registry denominator sha256: 264632006226a217d9201ddea30cef426514f8411eb5439e8063c67151392359
  root closure: open; exact anchor remains candidate pending downstream gates

cd Stage1_Instances/THM-M-0992
LEAN=/home/sansha-2/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean
DEPS=$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH)
LEAN_PATH="$DEPS" "$LEAN" -o Statement.olean Statement.lean
LEAN_PATH=".:$DEPS" "$LEAN" ObligationTree.lean
rm -f Statement.olean
  exit 0
  root_of_varianceAnchorPackage depends on axioms:
    [propext, Classical.choice, Quot.sound]

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 targets
python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required
python3 scripts/stage1_target.py show THM-M-0992
  exit 0: rank 272, planned, legacy artifacts unaccepted, theorem incomplete
git diff --check -- Stage1_Instances/THM-M-0992 .stage1-worker-selftest.json
  exit 0; no output
```

An initial direct check from `Formalizations/Lean` exited 1 because the local
`Statement` module was not on `LEAN_PATH`. A second attempt using `lake env
lean` inside the dossier also exited 1 because this clone has no Elan default.
The successful narrow check above uses the already installed pinned Lean
4.29.0 executable and the dependency path reported by Lake, first producing a
temporary local `Statement.olean` and then deleting it.

The checks cover frozen input hashes and denominators, required node fields,
seven separate graph types, unique typed edges and adjacency, reciprocal proof
composition, proof-DAG reachability, the 100-step ceiling, forbidden proof
construct hygiene, elaboration, and the conditional composition axiom report.
They do not accept the anchor as a proof node or close source, provenance,
trust, readability, hermetic, independent-verification, or theorem gates.
There is no accepted receipt; master acceptance remains required.
