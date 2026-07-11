# THM-M-0002 obligation-tree validation

Item: `S56-M-0002-OBLIGATION_TREE`

Base revision: `54f98aadb01e4a34f690bf4bc453a37147961481`

Validation date: `2026-07-12` (Asia/Shanghai)

## Frozen result

Registry version 1 freezes 14 obligations and 31 directed typed edges across separate proof,
refinement, provenance, evidence, trust, documentation, and workflow graphs. Eleven obligations are
root-relevant machine obligations and three are informational overlays. The denominator SHA-256 is
`7f9860d62d4ef3911e7e005e518aa22a00ebb2f1a3c57ea4703be539c057a342`.

The checked composition harness consumes explicit middle-mono and middle-epi families and returns
the exact five-lemma root. It does not establish either premise. The root remains open at `M1`; its
frozen proof-phase cut set is `M0002-B-MONO` and `M0002-B-EPI`.

## Commands and results

Commands ran from the repository root unless a working directory is stated. The canonical
pre-existing `.lake` closure was reused; no update, build, clone, fetch, or dependency mutation was
performed.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546
  uniform-L0 Lean 4 targets validated

python3 scripts/stage1_target.py check
  exit 0: 1546 unique ordered targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0002
  exit 0: execution rank 97; planned; legacy artifacts unaccepted;
  theorem_complete=false

python3 Stage1_Instances/THM-M-0002/build_obligation_artifacts.py
  exit 0: wrote 14 obligations and 31 typed edges; denominator digest
  7f9860d62d4ef3911e7e005e518aa22a00ebb2f1a3c57ea4703be539c057a342

python3 Stage1_Instances/THM-M-0002/check_obligation_tree.py
  exit 0: source-input hashes, frozen denominators, node schema, seven graph classes,
  reciprocal proof/composition edges, proof acyclicity, recipes, budgets, prohibited
  Lean tokens, open-root boundary, and cut set pass

python3 -m json.tool Stage1_Instances/THM-M-0002/obligation-registry.json
python3 -m json.tool Stage1_Instances/THM-M-0002/typed-graphs.json
python3 -m json.tool Stage1_Instances/THM-M-0002/validation-specs.json
  exit 0 for all three files: valid JSON

cd Formalizations/Lean && lake env lean \
  ../../Stage1_Instances/THM-M-0002/ObligationTree.lean
  exit 0: root_compose elaborated from explicit MiddleMono and MiddleEpi premises;
  both four-lemma probes and the upstream five-lemma probe passed; #print axioms
  reported [propext, Classical.choice, Quot.sound]
```

The pre-existing untracked `Formalizations/Lean/.lake` link makes this nonrelease evidence.

## Status boundary

This receipt supports only the version-1 registry, typed graphs, structured recipes, readable tree,
and conditional composition harness, pending master acceptance. No obligation is marked closed.
Proof-node acceptance, primary-source review, readable reconstruction review, transitive trust,
independent replay, `AUDIT-Z`, `THEOREM-Z`, and release remain open.
