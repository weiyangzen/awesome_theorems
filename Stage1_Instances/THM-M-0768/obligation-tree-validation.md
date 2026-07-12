# THM-M-0768 obligation-tree validation

Item: `S56-M-0768-OBLIGATION_TREE`. Base revision:
`9864b47f2fbf53d0b642c54f12039877d4635056`.

Validation ran in the worker clone on 2026-07-12. It reused the existing pinned Lake closure and
did not update, fetch, clone, or build dependencies. A temporary `/tmp/thm-m-0768-lean` directory
held the statement `.olean`; no `.lake` artifact was written.

```text
python3 Stage1_Instances/THM-M-0768/build_obligation_artifacts.py
  exit 0; generated 16 obligations
  denominator: 8b23897a31e941e606b42a0a9a69a8701b468827be58a296903521a55b27f2ab

python3 Stage1_Instances/THM-M-0768/check_obligation_tree.py
  exit 0; PASS THM-M-0768 obligation tree: 16 obligations, 22 typed edges
  root closure: open (M3); relational bridge remains the minimal root cut

cd Formalizations/Lean
rm -rf /tmp/thm-m-0768-lean && mkdir -p /tmp/thm-m-0768-lean
lake env bash -c 'cd ../../Stage1_Instances/THM-M-0768 && lean -o /tmp/thm-m-0768-lean/Statement.olean Statement.lean'
lake env bash -c 'cd ../../Stage1_Instances/THM-M-0768 && LEAN_PATH=/tmp/thm-m-0768-lean:$LEAN_PATH lean ObligationTree.lean'
  exits 0, 0; exact statement elaborated and conditional composition reported no axioms

python3 Docs/tools/check_stage1_standard.py
  exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets
python3 scripts/stage1_target.py check
  exit 0; 1546 unique targets, ranks 1..1546
python3 scripts/stage1_target.py show THM-M-0768
  exit 0; rank 778, planned, theorem_complete false
python3 -m json.tool Stage1_Instances/THM-M-0768/{obligation-registry,typed-graphs,validation-specs}.json
  exit 0 for each expanded path; all structured artifacts parsed
git diff --check -- Stage1_Instances/THM-M-0768 .stage1-worker-selftest.json
  exit 0; no whitespace errors
```

The structural checker verifies input hashes, frozen denominators, eligibility, mandatory node
fields and budgets, typed adjacency, reciprocal composition edges, acyclic proof reachability,
validation-recipe coverage, the open-root boundary, and placeholder-token hygiene. It neither
imports nor credits the pinned mathematical bridge and therefore supplies no root proof or theorem
completion.
