# THM-M-0392 Obligation-Tree Validation

Item: `S56-M-0392-OBLIGATION_TREE`  
Base revision: `fbc2d39d72ad14c2a116e6f9e3721b6e4af8218d`  
Validation date: `2026-07-12` (`Asia/Shanghai`)

## Frozen result

The registry freezes eight required root-relevant obligations and zero exclusions. Separate typed
proof, refinement, provenance, evidence, trust, documentation, and workflow graphs record the exact
root, curve construction, nonsingularity specialization, missing Lean 4 Siegel/integral-points
bridge, coordinate transport, finite-encoding transfer, primary-source boundary, and release trust
boundary. Each node has a substantive ledger of at most three steps.

`ObligationTree.lean` checks the exact conditional composition using explicit abstract premises. It
also kernel-checks the elementary transfer of finiteness along an injection. Lean reports that the
composition certificate depends on no axioms. This does not assert any abstract premise or prove
the Mordell finiteness root.

## Commands and exact results

All commands ran from the worker clone root unless the command begins with `cd`.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546
  uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0392
  exit 0: execution_rank=2; lifecycle_mode=planned; theorem_complete=false

python3 Stage1_Instances/THM-M-0392/check_obligation_tree.py
  exit 0: obligation_tree: ok (8 required obligations; 7 typed graphs; DAG and
  ledgers validated)

python3 -m json.tool Stage1_Instances/THM-M-0392/obligation-registry.json
python3 -m json.tool Stage1_Instances/THM-M-0392/obligation-nodes.json
python3 -m json.tool Stage1_Instances/THM-M-0392/typed-graphs.json
  exit 0 for each file: valid JSON

cd Formalizations/Lean && lake env lean \
  ../../Stage1_Instances/THM-M-0392/ObligationTree.lean
  exit 0: root_compose elaborated and printed; Lean reported that it does not
  depend on any axioms

git diff --check -- Stage1_Instances/THM-M-0392 .stage1-worker-selftest.json
  exit 0: no whitespace errors
```

The worker reused the existing pinned toolchain. No Lake update, build, clone, fetch, or `.lake`
mutation was performed.

## Status boundary

This receipt supports the frozen obligation architecture and conditional composition harness only.
The exact Lean 4 integral-points bridge is absent, so the root remains M2. Primary-source H0,
concrete curve adapters, terminal proof, trust closure, readable reconstruction, audit completion,
theorem completion, release, independent validation, and master acceptance remain open.
