# THM-M-0415 obligation-tree validation

Item: `S56-M-0415-OBLIGATION_TREE`. Base revision:
`b7ba23ee9689d0325e52ef93ab00d5cfe61e4df6`.

Validation ran in the worker clone on 2026-07-12. It reused the canonical pinned Lake artifacts;
no update, fetch, clone, or dependency build was run.

```text
python3 Stage1_Instances/THM-M-0415/build_obligation_artifacts.py
  exit 0
  de9131012caeaaeb9723594ca8b9cd440a2d3ab21a61ce7f86c2f7fba815fb0e

python3 Stage1_Instances/THM-M-0415/check_obligation_tree.py
  exit 0
  PASS THM-M-0415 obligation tree: 15 obligations, 33 typed edges
  registry denominator sha256: de9131012caeaaeb9723594ca8b9cd440a2d3ab21a61ce7f86c2f7fba815fb0e
  root state: M3 pending full provenance/trust and master acceptance; theorem_complete=false

cd Stage1_Instances/THM-M-0415 &&
  LEAN_BIN=$(cd ../../Formalizations/Lean && lake env which lean) &&
  LEAN_PATH=$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) &&
  LEAN_PATH="$LEAN_PATH" "$LEAN_BIN" -o Statement.olean Statement.lean &&
  LEAN_PATH=.:"$LEAN_PATH" "$LEAN_BIN" ObligationTree.lean
  exit 0
  All three obligation-tree declarations reported exactly:
    [propext, Classical.choice, Quot.sound]
  The temporary Statement.olean was removed immediately after the check.

python3 Docs/tools/check_stage1_standard.py
  exit 0; 15 assurance groups and 1546 uniform-L0 targets passed
python3 scripts/stage1_target.py check
  exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required
python3 scripts/stage1_target.py show THM-M-0415
  exit 0; rank 70, planned, theorem_complete false
python3 Stage1_Instances/THM-M-0415/check_statement.py
  exit 0; statement digest 7597a79f...1590 and all four mutations killed
python3 Stage1_Instances/THM-M-0415/check_anchor_audit.py
  exit 0; three candidates classified and pinned source hashes verified
python3 -m json.tool Stage1_Instances/THM-M-0415/{obligation-registry,typed-graphs,validation-specs}.json
  exit 0 for each file
git diff --check -- Stage1_Instances/THM-M-0415
  exit 0; no output
```

The structural check binds the registry to exact statement and anchor-audit bytes, recomputes the
frozen denominator, checks every required node field and leaf budget, validates typed adjacency and
reciprocal proof/composition edges, rejects proof cycles, checks structured no-network recipes, and
scans the Lean interface for forbidden proof devices. The Lean check consumes the exact
`FintypePresentation` child and yields the canonical root, while the direct pinned wrapper also
elaborates.

The mathlib declarations remain provisional `M3` candidates in this phase rather than accepted
`M0-W`: complete transitive provenance/trust evidence, node-specific source review, H0/R0,
content-addressed receipts, independent validation, and master acceptance remain open. Thus
`audit_complete=false` and `theorem_complete=false`; this self-test supports only the frozen
obligation-tree phase.
