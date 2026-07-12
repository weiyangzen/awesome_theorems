# THM-M-1228 obligation-tree validation

Item: `S56-M-1228-OBLIGATION_TREE`

Base revision: `935f676246c95d817740248fb8588e8cea34c00d`

Validation date: `2026-07-12` (Asia/Shanghai)

## Frozen result

Registry version 1 freezes 15 obligations and 31 directed typed edges across separate proof,
refinement, provenance, evidence, trust, documentation, and workflow graphs. Eleven obligations
are root-relevant machine obligations and four are informational overlays. The denominator SHA-256
is `25704bee664136645e0481ae7d6273ac3fdfd2f1cd20fc5f82ba43f07066f41e`.

The standalone Lean harness mirrors the already-hashed statement interface and checks that an
explicit per-solution premise composes with the root's binder structure. It cannot import the
dossier's `Statement.lean` directly because that source is outside the Lake module root and no
compiled object exists; the checker instead binds the registry to the exact `statement.json` and
checks the shared interface tokens. This is structural evidence only, not an exact-type proof
wrapper. The root remains open at `M4`.

## Commands and results

Commands ran from the repository root unless noted. The canonical pre-existing `.lake` artifacts
were reused. No update, build, clone, fetch, or dependency mutation was performed.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 Lean 4 targets validated

python3 scripts/stage1_target.py check
  exit 0: 1546 unique ordered targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-1228
  exit 0: rank 156; planned; legacy artifacts unaccepted; theorem_complete=false

python3 Stage1_Instances/THM-M-1228/build_obligation_artifacts.py
  exit 0: wrote 15 obligations and 31 typed edges; denominator digest
  25704bee664136645e0481ae7d6273ac3fdfd2f1cd20fc5f82ba43f07066f41e

python3 Stage1_Instances/THM-M-1228/check_obligation_tree.py
  exit 0: input hashes, denominators, node schema, seven graph classes,
  reciprocal composition edges, acyclicity, recipes, budgets, and open boundary pass

cd Formalizations/Lean && lake env lean \
  ../../Stage1_Instances/THM-M-1228/ObligationTree.lean
  exit 0: structural composition harness elaborated; `#print axioms` reported
  `[propext, Classical.choice, Quot.sound]`

python3 Stage1_Instances/THM-M-1228/check_statement.py
  exit 0: expression SHA-256 `101ce8f2...8ecf58e5f`; four mutations distinguished

python3 Stage1_Instances/THM-M-1228/check_anchor_audit.py
  exit 0: M4 boundary, nine probes, mathlib pin, and four immutable trees agree

python3 -m json.tool Stage1_Instances/THM-M-1228/obligation-registry.json
python3 -m json.tool Stage1_Instances/THM-M-1228/typed-graphs.json
python3 -m json.tool Stage1_Instances/THM-M-1228/validation-specs.json
  exit 0 for all three files: valid JSON

git diff --check -- Stage1_Instances/THM-M-1228 .stage1-worker-selftest.json
  exit 0: no whitespace errors
```

## Status boundary

This receipt supports only the frozen architecture pending master acceptance. No obligation is
marked closed. Concrete analytic definitions, epsilon regularity, covering and measure proofs,
primary-source review, exact proof integration, transitive trust, independent replay, theorem
completion, and release remain open. The pre-existing untracked `.lake` link also makes this
nonrelease evidence.
