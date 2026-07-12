# THM-M-0339 obligation-tree validation

Item: `S56-M-0339-OBLIGATION_TREE`

Base revision: `c9694802ae049af37973e49a65f11b833135333f`

Validation date: `2026-07-12` (Asia/Shanghai)

## Frozen result

Registry version 1 freezes 19 obligations and 35 directed typed edges across separate proof,
refinement, provenance, evidence, trust, documentation, and workflow graphs. Sixteen obligations are
root-relevant machine obligations and three are informational overlays. The denominator SHA-256 is
`29ab54f13bdf31d2d84b7eb0ac2a07fe21a19ac12587dae5e5e58d97374c4b62`.

The checked Lean harness consumes an explicit `PartitionEngine` premise and returns the exact frozen
root. It does not prove the engine. No obligation is credited closed; the root remains `M4`, and the
proof-phase critical cut is the formal MSS Theorem 1.4 obligation `M0339-L-THEOREM14`.

## Commands and results

Commands ran from the repository root unless a working directory is stated. The existing pinned
`.lake` artifacts were reused; no update, build, clone, fetch, or dependency mutation was performed.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546
  uniform-L0 Lean 4 targets validated

python3 scripts/stage1_target.py check
  exit 0: 1546 unique ordered targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0339
  exit 0: rank 832; planned; legacy artifacts unaccepted; theorem_complete=false

python3 Stage1_Instances/THM-M-0339/build_obligation_artifacts.py
  exit 0: wrote 19 obligations and 35 typed edges; denominator digest
  29ab54f13bdf31d2d84b7eb0ac2a07fe21a19ac12587dae5e5e58d97374c4b62

python3 Stage1_Instances/THM-M-0339/check_obligation_tree.py
  exit 0: input hashes, denominators, node schema, seven typed graphs, reciprocal
  proof/composition edges, acyclicity, recipes, budgets, prohibited Lean tokens,
  open-root boundary, and critical cut pass

python3 -m json.tool Stage1_Instances/THM-M-0339/obligation-registry.json
python3 -m json.tool Stage1_Instances/THM-M-0339/typed-graphs.json
python3 -m json.tool Stage1_Instances/THM-M-0339/validation-specs.json
  exit 0 for all three files: valid JSON

cd Formalizations/Lean && lake env lean \
  ../../Stage1_Instances/THM-M-0339/ObligationTree.lean
  exit 0: the conditional exact-root composition elaborated; the pinned rank-one
  norm probe passed; #print axioms reported [propext, Classical.choice, Quot.sound]

git diff --check -- Stage1_Instances/THM-M-0339
  exit 0: no whitespace errors
```

An initial narrow Lean run failed because the audit's positivity declaration is not exported by the
minimal `PiL2` import. The nonessential probe was removed; no dependency or import was broadened.

## Status boundary

This worker evidence supports only the version-1 registry, typed graphs, structured validation
recipes, readable tree, and conditional composition harness, pending master acceptance. It supplies
no proof of Theorem 1.4 or Corollary 1.5, no closed obligation, no H0/R0 result, no audit completion,
no release evidence, and no theorem-completion credit.
