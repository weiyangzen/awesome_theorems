# THM-M-1258 obligation-tree validation

Item: `S56-M-1258-OBLIGATION_TREE`

Base revision: `8da22023e24f307fb21f41ed93f69f2b8fa82879`

Validation date: `2026-07-12` (Asia/Shanghai)

## Frozen result

Registry version 1 freezes nine obligations and 22 edges across separate proof, refinement,
provenance, evidence, trust, documentation, and workflow graphs. Five obligations are root-relevant
and machine eligible, two are explicit boundary analyses, and two are informational overlays. The
canonical denominator digest is
`aa2130aa5e8531ce471de8e404b0aa89deaaabb7dd45f950baa1a81e68feae9a`.

## Commands and results

All commands ran from the repository root except the explicitly prefixed Lean command.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546
  uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-1258
  exit 0: execution_rank=436; lifecycle_mode=planned; theorem_complete=false

python3 Stage1_Instances/THM-M-1258/build_obligation_artifacts.py
  exit 0: wrote 9 obligations and 22 typed edges; denominator digest matched

python3 Stage1_Instances/THM-M-1258/check_obligation_tree.py
  exit 0: statement/audit hashes, registry projection, denominators, node schemas,
  ledgers, seven graph classes, reciprocal proof edges, indices, and open-root
  boundary passed; M1258-L-SPAN is the generic root cut

python3 -m json.tool Stage1_Instances/THM-M-1258/obligation-registry.json
python3 -m json.tool Stage1_Instances/THM-M-1258/typed-graphs.json
  exit 0 for both files: valid JSON

cd Formalizations/Lean && lake env lean \
  ../../Stage1_Instances/THM-M-1258/ObligationTree.lean
  exit 0: compose_condition, empty_domain, and zero_dimension elaborated; each
  #print axioms reported exactly propext, Classical.choice, and Quot.sound

git diff --check -- Stage1_Instances/THM-M-1258 .stage1-worker-selftest.json
  exit 0: no whitespace errors
```

The existing pinned `.lake` artifact was reused. No update, build, clone, fetch, or dependency
mutation was performed. The pre-existing untracked `.lake` artifact makes this nonrelease evidence.

## Status boundary

This receipt supports only the frozen registry, typed graphs, and conditional/boundary composition
harness. The target is a predicate, so a generic inhabitant requires concrete fields and a proof of
the pointwise span equality. No obligation is marked closed. Exact proof bodies for a concrete
instance, H0/R0 review, transitive trust, independent validation, `AUDIT-Z`, `THEOREM-Z`, and master
acceptance remain open.
