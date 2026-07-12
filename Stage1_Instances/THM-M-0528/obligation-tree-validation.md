# THM-M-0528 obligation-tree validation

Item: `S56-M-0528-OBLIGATION_TREE`. Base revision:
`a43bd59b308cf4aade4b9f33c35e025b8c64e515`.

Validation ran from the worker clone on 2026-07-12. It reused the existing pinned Lake artifacts;
no update, build, dependency clone, or fetch was run.

```text
python3 Stage1_Instances/THM-M-0528/build_obligation_artifacts.py
  exit 0
  wrote 12 obligations and 18 typed edges
  953fb441526573d4db5c34d29d1f96bc097892ef060f1d943c0f3a1eb4f2826f

python3 Stage1_Instances/THM-M-0528/check_obligation_tree.py
  exit 0
  PASS THM-M-0528 obligation tree: 12 obligations, 18 typed edges
  registry denominator sha256: 953fb441526573d4db5c34d29d1f96bc097892ef060f1d943c0f3a1eb4f2826f
  root closure: open (M3); exact pinned anchor remains the proof-phase cut

cd Stage1_Instances/THM-M-0528 &&
  LEAN_PATH=$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
    /home/sansha-2/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean \
      -o Statement.olean Statement.lean &&
  LEAN_PATH=.:$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
    /home/sansha-2/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean \
      ObligationTree.lean
  exit 0
  root_of_exactPointwiseAnchor depends on axioms:
    [propext, Classical.choice, Quot.sound]
  Statement.olean removed after the scoped check.

python3 Docs/tools/check_stage1_standard.py
  exit 0: ok; 15 assurance groups, 1546 uniform-L0 targets

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0528
  exit 0: rank 585, planned, theorem_complete false

git diff --check -- Stage1_Instances/THM-M-0528 .stage1-worker-selftest.json
  exit 0; no output
```

The scoped Lean invocation uses the exact installed Lean 4.29.0 binary and the `LEAN_PATH` obtained
from the pinned Lake environment. It validates the canonical statement and the explicit
child-to-parent composition harness. The structural checker validates source hashes, the frozen
denominator, complete node schemas, graph separation, reciprocal proof edges, adjacency,
acyclic root reachability, validation-recipe coverage, and placeholder hygiene.

This is architecture evidence only. The explicit `ExactPointwiseAnchor` premise prevents the
conditional composition theorem from masquerading as root closure. There is no accepted master
receipt and no theorem-completion claim.
