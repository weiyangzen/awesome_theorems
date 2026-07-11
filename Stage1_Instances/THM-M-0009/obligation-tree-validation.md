# THM-M-0009 obligation-tree validation

Item: `S56-M-0009-OBLIGATION_TREE`

Base revision: `b7719b39b5595e187b4d2ecf832d3922a916d38b`

Validation date: `2026-07-12` (Asia/Shanghai)

## Frozen result

Registry version 1 freezes 15 obligations and 33 directed typed edges across separate proof,
refinement, provenance, evidence, trust, documentation, and workflow graphs. Twelve obligations are
root-relevant machine requirements and three are informational overlays. The denominator SHA-256 is
`3e293a10107673671a53438c02b6d3bbc3d5a3fa90d2f0e2967c12689821e438`.

`root_compose` consumes the two exact variance branches and returns the exact conjunction. It does
not instantiate those premises. The root remains open at `M1`, with frozen cut set
`M0009-L-COV-EXACT` and `M0009-L-CONTRA-EXACT`.

## Commands and results

Commands ran from the repository root except where stated. The existing pinned `.lake` closure was
reused; no update, build, clone, fetch, or dependency mutation was performed.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546
  uniform-L0 Lean 4 targets validated

python3 scripts/stage1_target.py check
  exit 0: 1546 unique ordered targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0009
  exit 0: rank 102, lifecycle planned, legacy artifacts unaccepted,
  theorem_complete=false

python3 Stage1_Instances/THM-M-0009/build_obligation_artifacts.py
  exit 0: wrote 15 obligations and 33 typed edges; denominator digest
  3e293a10107673671a53438c02b6d3bbc3d5a3fa90d2f0e2967c12689821e438

python3 Stage1_Instances/THM-M-0009/check_obligation_tree.py
  exit 0: source hashes, denominators, node identities, seven graph classes,
  reciprocal composition, proof acyclicity, recipes, budgets, prohibited tokens,
  and the open-root boundary passed

python3 -m json.tool Stage1_Instances/THM-M-0009/obligation-registry.json
python3 -m json.tool Stage1_Instances/THM-M-0009/typed-graphs.json
python3 -m json.tool Stage1_Instances/THM-M-0009/validation-specs.json
  exit 0 for all three files: valid JSON

cd Formalizations/Lean && lake env lean \
  ../../Stage1_Instances/THM-M-0009/ObligationTree.lean
  exit 0: conditional root composition and both pinned declaration probes elaborated;
  #print axioms root_compose reported [propext, Classical.choice, Quot.sound]

python3 Stage1_Instances/THM-M-0009/check_statement.py
  exit 0: statement digest a5f8f018376a768901a6580f7a4fbfe593d73cfb89d71420b79f268b15d083be;
  four statement mutations distinguished; pinned mathlib revision agreed

git diff --check -- Stage1_Instances/THM-M-0009 .stage1-worker-selftest.json
  exit 0: no whitespace errors
```

An exploratory invocation of the non-existent
`Stage1_Instances/THM-M-0009/check_anchor_audit.py` exited 2. The prerequisite anchor audit instead
has its own recorded Lean and immutable-source evidence; no such checker is claimed by this phase.
The pre-existing untracked `Formalizations/Lean/.lake` link makes all evidence nonrelease.

## Status boundary

This receipt supports only the frozen registry, typed graphs, structured recipes, readable outline,
and conditional composition harness, pending master acceptance. No proof obligation is closed.
Primary-source and readable reviews, transitive provenance/trust, independent replay, `AUDIT-Z`,
`THEOREM-Z`, and release remain open.
