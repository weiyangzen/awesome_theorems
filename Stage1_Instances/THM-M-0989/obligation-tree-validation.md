# THM-M-0989 obligation-tree validation

Item: `S56-M-0989-OBLIGATION_TREE`. Base revision:
`592758f4f7e1dc72b9862272624df38bd92621c2`.

Validation ran in the worker clone on 2026-07-12. Existing pinned Lake artifacts
were reused; no dependency update, build, fetch, or clone was run.

```text
python3 Stage1_Instances/THM-M-0989/build_obligation_artifacts.py
  exit 0
  c5d0b41c35c0759e11055611925021d6c2e38fc251da666e8f3afe238eccdc15

python3 Stage1_Instances/THM-M-0989/check_obligation_tree.py
  exit 0
  PASS THM-M-0989 obligation tree: 15 obligations, 32 typed edges
  registry denominator sha256: c5d0b41c35c0759e11055611925021d6c2e38fc251da666e8f3afe238eccdc15
  root closure: open (M3); row measurability and characteristic-function package remain open

LEAN=$(cd Formalizations/Lean && lake env which lean)
LP=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
cd Stage1_Instances/THM-M-0989
LEAN_PATH="$LP" "$LEAN" -o Statement.olean Statement.lean
LEAN_PATH="../..:$LP" "$LEAN" ObligationTree.lean
  exit 0; no diagnostics; temporary Statement.olean removed

python3 Docs/tools/check_stage1_standard.py
  exit 0; ok: 15 assurance groups and 1546 uniform-L0 targets
python3 scripts/stage1_target.py check
  exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required
python3 scripts/stage1_target.py show THM-M-0989
  exit 0; rank 269, planned, theorem_complete false
git diff --check -- Stage1_Instances/THM-M-0989 .stage1-worker-selftest.json
  exit 0; no output
```

An initial attempt to elaborate the external file directly from the Lake project
returned exit 1 because Lean requires an input file under its root directory.
The successful scoped command used the exact pinned executable and Lake-derived
`LEAN_PATH`, emitted a temporary local `Statement.olean`, and removed it.

The checks cover registry hashes and denominators, required node ledgers, recipe
coverage, typed reciprocal proof edges, adjacency, proof-DAG acyclicity and root
reachability, forbidden proof tokens, exact Lean elaboration, and conditional
composition through the pinned Levy theorem. They do not prove either explicit
input package or the theorem root. Master acceptance remains required.
