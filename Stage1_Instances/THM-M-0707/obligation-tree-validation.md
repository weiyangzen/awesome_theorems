# THM-M-0707 obligation-tree validation

Item: `S56-M-0707-OBLIGATION_TREE`. Base revision:
`3a479c703900e8096e6b239e7bf5b0da25472b8a`.

Validation ran in the worker clone on 2026-07-12. It reused the existing pinned
Lake closure and did not update, fetch, clone, or build dependencies.

```text
python3 Stage1_Instances/THM-M-0707/build_obligation_artifacts.py
  exit 0; generated 12 obligations and 34 typed edges
  denominator: f492ceafdb8211fa72b1345250e1f0d1777554fecd8ac3d921c158a4062e1a57

python3 Stage1_Instances/THM-M-0707/check_obligation_tree.py
  exit 0; PASS THM-M-0707 obligation tree: 12 obligations, 34 typed edges
  root acceptance remains open

cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0707/Statement.lean
  exit 0; printed the fully explicit canonical target

cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0707/ObligationTree.lean
  exit 0; all four declarations elaborated
  #print axioms for the embedding, restriction, composition, and instantiated
  root reported exactly Classical.choice, Quot.sound, and propext

python3 Docs/tools/check_stage1_standard.py
  exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets
python3 scripts/stage1_target.py check
  exit 0; 1546 unique targets, ranks 1..1546
python3 scripts/stage1_target.py show THM-M-0707
  exit 0; rank 748, planned, theorem_complete false
git diff --check -- Stage1_Instances/THM-M-0707
  exit 0; no whitespace errors
```

The structural validator checks exact input hashes, canonical denominator
serialization, eligibility projections, complete node schemas and ledgers,
budgets, edge endpoint and adjacency integrity, reciprocal proof edges, proof
acyclicity and root reachability, recipe coverage, open release boundaries,
and forbidden Lean proof tokens. The Lean check supplies real kernel evidence
for the typed composition but does not accept the source, TCB, provenance,
readability, independent-validation, or release gates.
