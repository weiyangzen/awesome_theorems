# THM-M-1091 obligation-tree validation

Item: `S56-M-1091-OBLIGATION_TREE`

Base revision: `00641d8cecb3ce45e4fa66318bc97c9a63bb176e`

Validation date: `2026-07-12` (Asia/Shanghai)

## Frozen result

Registry version 1 freezes twelve obligations and sixteen edges across separate proof, refinement,
provenance, evidence, trust, documentation, and workflow graphs. Nine obligations are machine
eligible and three are informational assurance overlays. The canonical denominator digest is
`4ec2b5d5aec067b17fb083be5130977395b153baea6cd37e4403439e6ddf0a0f`.

The exact conditional composition certificate consumes `M1091-L-POWADD` at swapped indices and
uses `add_comm` to return the frozen root. It does not inspect or adopt the audited mathlib proof
body, so root closure remains open for the proof phase.

## Commands and results

All commands ran in this worker clone. The Lean command used the existing pinned Lake artifacts;
no update, build, clone, fetch, or dependency mutation was performed.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-1091
  exit 0: rank 533, planned lifecycle, theorem_complete=false

python3 Stage1_Instances/THM-M-1091/build_obligation_artifacts.py
  exit 0: wrote 12 obligations and 16 typed edges; denominator digest matched

python3 Stage1_Instances/THM-M-1091/check_obligation_tree.py
  exit 0: input hashes, denominator, full node schema, ledgers, seven graph
  classes, reciprocal proof edges, validation recipes, placeholder scan, and
  open-root boundary passed

python3 -m json.tool Stage1_Instances/THM-M-1091/obligation-registry.json
python3 -m json.tool Stage1_Instances/THM-M-1091/typed-graphs.json
python3 -m json.tool Stage1_Instances/THM-M-1091/validation-specs.json
  exit 0 for all three files: valid JSON

cd Formalizations/Lean && lake env lean \
  ../../Stage1_Instances/THM-M-1091/ObligationTree.lean
  exit 0: compose_root and both zero-step boundaries elaborated; each #print
  axioms reported exactly propext, Classical.choice, and Quot.sound

git diff --check -- Stage1_Instances/THM-M-1091 .stage1-worker-selftest.json
  exit 0: no whitespace errors
```

The worktree also contains a pre-existing untracked `Formalizations/Lean/.lake` link/artifact, so
this evidence is nonrelease evidence as required by the worker protocol.

## Status boundary

This receipt supports only the frozen obligation denominator, typed graphs, structured recipes,
conditional root composition, and zero-step boundaries. Proof-phase adoption of the central
bridge, H0/R0 review, transitive trust, hermetic replay, independent validation, audit completion,
theorem completion, and master acceptance remain open.
