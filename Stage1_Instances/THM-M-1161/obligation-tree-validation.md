# THM-M-1161 obligation-tree validation

Item: `S56-M-1161-OBLIGATION_TREE`

Base revision: `31b7ab5b3902c4a80878c2007218f90566a8b85c`

Validation date: `2026-07-12` (Asia/Shanghai)

## Frozen result

Registry version 1 freezes 19 obligations and 65 directed typed edges across separate proof,
refinement, provenance, evidence, trust, documentation, and workflow graphs. Seventeen obligations
are machine-required and two are informational overlays. The denominator SHA-256 is
`8a07bd14994ae4988b608e465665fd5360bb659474ed5915bbef01b2ae60533a`.

The Lean harness restates the canonical proposition and checks that the homogeneous-kernel
dichotomy plus both conditional analytic branch results compose to the complete root. It does not
instantiate those premises. No obligation is credited closed; the root remains `M4`, with frozen
analytic cut set `B-DICHOTOMY`, `L-BIJECTIVE`, `L-CLOSED-RANGE`, and `L-ORTHOGONAL`.

## Commands and results

Commands ran from the repository root unless a working directory is stated. The existing pinned
`.lake` artifacts were reused; no update, build, clone, fetch, or dependency mutation occurred.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and all 1546 uniform-L0 targets validated

python3 scripts/stage1_target.py check
  exit 0: 1546 unique ordered targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-1161
  exit 0: rank 364; planned; rework required; theorem_complete=false

python3 Stage1_Instances/THM-M-1161/build_obligation_artifacts.py
  exit 0: wrote 19 obligations and 65 typed edges; denominator
  8a07bd14994ae4988b608e465665fd5360bb659474ed5915bbef01b2ae60533a

python3 Stage1_Instances/THM-M-1161/check_obligation_tree.py
  exit 0: input hashes, frozen denominators, node schemas, seven graph classes,
  reciprocal proof/composition edges, proof acyclicity, recipes, budgets,
  prohibited Lean tokens, and the open-root boundary passed

python3 -m json.tool Stage1_Instances/THM-M-1161/{obligation-registry,typed-graphs,validation-specs}.json
  exit 0 for each file: valid JSON

cd Formalizations/Lean && lake env lean \
  ../../Stage1_Instances/THM-M-1161/FredholmIntegralEquationStatement.lean
  exit 0: the pre-existing canonical proposition re-elaborated

cd Formalizations/Lean && lake env lean \
  ../../Stage1_Instances/THM-M-1161/ObligationTree.lean
  exit 0: root_compose elaborated; pinned anchor probes passed; the axiom report was
  [propext, Classical.choice, Quot.sound]; only an unused-section-variable linter warning occurred
```

The pre-existing untracked `Formalizations/Lean/.lake` link makes this nonrelease evidence.

## Status boundary

This receipt supports only the version-1 registry, typed graphs, recipes, readable architecture,
and conditional composition harness, pending master acceptance. It does not support analytic proof
closure, primary-source review, `R0`, transitive trust closure, independent replay, `AUDIT-Z`,
`THEOREM-Z`, or release.
