# THM-M-0388 Obligation-Tree Validation

Item: `S56-M-0388-OBLIGATION_TREE`

Base revision: `10cd0fbeb2835ecd6e547655cb024ca78727fbb9`

Validation date: `2026-07-12` (Asia/Shanghai)

## Frozen result

The registry freezes eleven required root-relevant obligations and zero exclusions. Separate typed
proof, refinement, provenance, evidence, trust, documentation, and workflow graphs bind the exact
root to the predicate transport, the pinned mathlib theorem, the substantive internal proof-body
packages, and the still-open release trust boundary. Wrapper and stronger-theorem aliases share one
terminal proof-body identity.

## Commands and results

All commands ran from the repository root unless the command begins with `cd`.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546
  uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0388
  exit 0: execution_rank=3; lifecycle_mode=planned; theorem_complete=false

python3 Stage1_Instances/THM-M-0388/check_obligation_tree.py
  exit 0: obligation_tree: ok (11 obligations; 7 typed graphs; dependency DAG
  and ledgers validated)

python3 -m json.tool Stage1_Instances/THM-M-0388/obligation-registry.json
python3 -m json.tool Stage1_Instances/THM-M-0388/obligation-nodes.json
python3 -m json.tool Stage1_Instances/THM-M-0388/typed-graphs.json
  exit 0 for each file: valid JSON

cd Formalizations/Lean && lake env lean \
  ../../Stage1_Instances/THM-M-0388/ObligationTree.lean
  exit 0: root_compose elaborated and printed; Lean reported that root_compose
  does not depend on any axioms

git diff --check -- Stage1_Instances/THM-M-0388
  exit 0: no whitespace errors
```

Artifact SHA-256 values at self-test:

```text
46fe5c6ecce251c6a0d866112081bbc7483046d1d3e83f15fe3886e4453786f9  obligation-registry.json
d9f1f4beafe89ddc42dc651b4f9803ff2c5b712baa1a0f0ec21bed9f74b046f9  obligation-nodes.json
f7c0ea3a2845e4fe9a567fa550e48d256e209323efffa67928a562c689bf995c  typed-graphs.json
4415e5b627ec9dc620b0c9e075e777a04fee720341aa29788b0f41fddc5ad7c0  obligation-tree.md
f8064329af85c3330cf13b9bd1aaffa385d20b202925113e06d74e04040fdbce  ObligationTree.lean
c69ef0b66c167dcf14e89f6064376a659bf1e5d3e6f1fedfc8eb51268accc6ad  check_obligation_tree.py
```

The worker reused the existing pinned toolchain and did not update, build, fetch, clone, or mutate
`.lake`. The canonical cache still lacks `Mathlib.NumberTheory.Pell.olean`, so the imported theorem
and adapter cannot receive kernel, axiom, or trust closure in this phase.

## Status boundary

This receipt supports only the obligation architecture freeze and its conditional composition
harness. The imported proof body, exact root, H0/R0 review, transitive trust closure, independent
validation, audit completion, theorem completion, and master acceptance remain open.
