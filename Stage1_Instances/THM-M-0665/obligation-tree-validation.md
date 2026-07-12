# THM-M-0665 obligation-tree validation

Item: `S56-M-0665-OBLIGATION_TREE`

Base revision: `b71f83d4787958a60592c6b79d99b9bb1b79b6c0`

Validation date: `2026-07-12` (Asia/Shanghai)

## Frozen result

Registry version 1 freezes 20 obligations and 48 directed edges across separate proof, refinement,
provenance, evidence, trust, documentation, and workflow graphs. Seventeen obligations are
root-relevant machine obligations and three are informational overlays. The frozen denominator
SHA-256 is `9aa4a6fe979874ca4baa46f7f6b12d9dd965206a2d05614e70330640ac4303e5`.

No obligation is marked closed. The root remains `M3`, no composition certificate is claimed, and
the first proof-phase cut set is `C-PARAM`, `L-DERIVATIVE`, `L-ARITHMETIC`, `L-DROP`, and `L-COUNT`.

## Commands and results

Commands ran from the repository root unless a working directory is shown. The pre-existing
canonical `.lake` closure was reused read-only. No update, build, clone, fetch, or dependency
mutation was performed.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546
  uniform-L0 Lean 4 targets validated

python3 scripts/stage1_target.py check
  exit 0: 1546 unique ordered targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0665
  exit 0: execution rank 709; planned; legacy artifacts unaccepted;
  theorem_complete=false

python3 Stage1_Instances/THM-M-0665/build_obligation_artifacts.py
  exit 0: wrote 20 obligations and 48 typed edges; denominator digest
  9aa4a6fe979874ca4baa46f7f6b12d9dd965206a2d05614e70330640ac4303e5

python3 Stage1_Instances/THM-M-0665/check_obligation_tree.py
  exit 0: source-input hashes, frozen denominators, required node schema,
  seven graph classes, reciprocal proof/composition edges, proof acyclicity,
  recipes, budgets, prohibited Lean tokens, and open-root boundary passed

python3 -m json.tool Stage1_Instances/THM-M-0665/obligation-registry.json
python3 -m json.tool Stage1_Instances/THM-M-0665/typed-graphs.json
python3 -m json.tool Stage1_Instances/THM-M-0665/validation-specs.json
  exit 0 for all three files: valid JSON

cd Formalizations/Lean && lake env lean \
  ../../Stage1_Instances/THM-M-0665/Statement.lean
  exit 0: exact root, checked expansion, mutations, and boundary declarations elaborated

python3 Stage1_Instances/THM-M-0665/check_statement.py
  exit 0: exact expression SHA-256 da66c715ce12af9ff6dfb55a721665c8240358c0ee547062b3d2fc10c7785944;
  three mutations distinguished; pinned mathlib revision agreed

git diff --check -- Stage1_Instances/THM-M-0665 .stage1-worker-selftest.json
  exit 0: no whitespace errors

rg -n '\b(sorry|admit|axiom)\b' Stage1_Instances/THM-M-0665 --glob '*.lean'
  exit 1 as expected: no forbidden Lean token found
```

The pre-existing untracked `Formalizations/Lean/.lake` link makes this nonrelease evidence.

## Status boundary

This receipt supports only the version-1 registry, typed graphs, structured validation recipes, and
readable architecture, pending master acceptance. It provides no proof-node closure, independent
primary-source review, readable reconstruction review, transitive trust audit, `AUDIT-Z`,
`THEOREM-Z`, or release evidence.
