# THM-M-0133 obligation-tree validation

Item: `S56-M-0133-OBLIGATION_TREE`

Base revision: `d202f3aedade691a692ec4162fc08e5f1d2694f9`

Validation date: `2026-07-12` (Asia/Shanghai)

## Frozen result

Registry version 1 freezes 38 obligations and 40 edges across separate proof,
refinement, provenance, evidence, trust, documentation, and workflow graphs.
Thirty-two obligations are root-relevant and machine/source eligible; six are
informational provenance or trust overlays. The denominator projection digest
is `2cc4ccb678ee0d51bad12618425c7e8237eff14fdd0897b00284d165313d26bd`.

## Commands and results

All commands ran at the repository root except the explicitly prefixed Lean command.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546
  uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0133
  exit 0: execution_rank=22; lifecycle_mode=planned; theorem_complete=false

python3 Stage1_Instances/THM-M-0133/build_obligation_artifacts.py
  exit 0: wrote 38 obligations and 40 typed edges

python3 Stage1_Instances/THM-M-0133/check_obligation_tree.py
  exit 0: registry digest, required schemas and denominators, seven graph
  classes, reciprocal indices, reachability, acyclicity, ledgers, and open-root
  boundary passed; root M2 with M0133-L-MOD and M0133-L-LOWER as the cut set

python3 -m json.tool Stage1_Instances/THM-M-0133/obligation-registry.json
python3 -m json.tool Stage1_Instances/THM-M-0133/typed-graphs.json
  exit 0 for both files: valid JSON

cd Formalizations/Lean && lake env lean \
  ../../Stage1_Instances/THM-M-0133/ObligationTree.lean
  exit 0: root_compose elaborated through FermatLastTheorem.of_odd_primes;
  #print axioms reported only propext, Classical.choice, and Quot.sound

git diff --check -- Stage1_Instances/THM-M-0133
  exit 0: no whitespace errors
```

The existing pinned `.lake` closure was reused. No update, build, clone, fetch,
or other dependency mutation was performed. The untracked `.lake` link/artifact
predated this phase and makes this evidence nonrelease evidence.

## Status boundary

This receipt supports only the frozen registry, typed graphs, and conditional
composition harness. No obligation is marked closed. Semistable modularity,
level lowering, exact proof bodies, source/readability review, transitive trust,
independent validation, `AUDIT-Z`, `THEOREM-Z`, and master acceptance remain open.
