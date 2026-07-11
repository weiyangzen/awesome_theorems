# THM-M-0086 obligation-tree validation

Item: `S56-M-0086-OBLIGATION_TREE`

Base revision: `cd2070316d8a25117b90105fb1da2b6853a71999`

Validation date: `2026-07-12` (Asia/Shanghai)

## Frozen result

Registry version 1 freezes 19 obligations and 42 directed typed edges across separate proof,
refinement, provenance, evidence, trust, documentation, and workflow graphs. Sixteen obligations
are root-relevant machine obligations; three are informational overlays. The denominator SHA-256
is `3ef5a22e409dfe80fa0504d68038c05507040538a88d010910b121fc3c5a986d`.

The checked composition harness consumes the embedding, injective-cogenerator, and projective-
generator families and returns their exact nested conjunction. It does not instantiate those
premises. The root remains open at `M1`; its frozen proof-phase cut set is `M0086-L-EMBED`,
`M0086-L-INJECTIVE`, and `M0086-L-PROJECTIVE`.

## Commands and results

Commands ran from the repository root unless the working directory is explicitly `Formalizations/Lean`.
The canonical pre-existing `.lake` closure was reused; no update, build, clone, fetch, or dependency
mutation was performed.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546
  uniform-L0 Lean 4 targets validated

python3 scripts/stage1_target.py check
  exit 0: 1546 unique ordered targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0086
  exit 0: execution rank 134; planned; legacy artifacts unaccepted;
  theorem_complete=false

python3 Stage1_Instances/THM-M-0086/build_obligation_artifacts.py
  exit 0: wrote 19 obligations and 42 typed edges; denominator digest
  3ef5a22e409dfe80fa0504d68038c05507040538a88d010910b121fc3c5a986d

python3 Stage1_Instances/THM-M-0086/check_obligation_tree.py
  exit 0: source hashes, denominators, node schema, seven graph classes,
  reciprocal proof edges, acyclicity, recipes, budgets, prohibited tokens,
  and open-root boundary pass

python3 Stage1_Instances/THM-M-0086/check_anchor_audit.py
  exit 0: immutable pins, source hashes, three anchors, and M1 boundary pass

python3 -m json.tool Stage1_Instances/THM-M-0086/obligation-registry.json
python3 -m json.tool Stage1_Instances/THM-M-0086/typed-graphs.json
python3 -m json.tool Stage1_Instances/THM-M-0086/validation-specs.json
  exit 0 for all three files: valid JSON

cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0086/ObligationTree.lean
  exit 0: root_compose elaborated from three explicit branch premises; terminal
  probes passed; #print axioms reported [propext, Classical.choice, Quot.sound]

cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0086/Statement.lean
  exit 0: exact statement, checked equivalence, four expected mutation failures,
  and axiom report elaborated

cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0086/AnchorAudit.lean
  exit 0: three pinned terminal declarations and unfolded composition probe elaborated;
  all axiom reports were [propext, Classical.choice, Quot.sound]

git diff --check -- Stage1_Instances/THM-M-0086 .stage1-worker-selftest.json
  exit 0: no whitespace errors
```

The pre-existing untracked `Formalizations/Lean/.lake` link makes this nonrelease evidence.

## Status boundary

This receipt supports only the version-1 obligation registry, typed graphs, structured recipes,
readable architecture, and conditional composition harness, pending master acceptance. No
obligation is marked closed. Proof acceptance, primary-source review, readable reconstruction,
transitive trust closure, independent replay, `AUDIT-Z`, `THEOREM-Z`, and release remain open.
