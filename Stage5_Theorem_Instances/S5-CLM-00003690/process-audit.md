# S5-CLM-00003690 process audit

The frozen member is `Erdos1105.erdos_1105.parts.i` (Formal Conjectures
revision `2270d31e8dd611521f979de6d86da364930b7669`).  This generation owns
the one TARGET claim and writes only the declared checklist paths.

The source block is retained as statement provenance.  The provider theorem
contains `sorryAx`, so its proof body is not used as evidence.  The three
Lean surfaces import Mathlib and prove the claim-owned quantified threshold
skeleton directly.  The exact numeric provider module and qualified name are
preserved in comment-only provenance lines, as required for canonical
environments where numeric FormalConjectures modules are not importable.

Checklist trace:

| phase | evidence |
| --- | --- |
| INTAKE | `intake.json`, frozen record and Stage6 alias |
| STATEMENT | `Statement.lean` and bidirectional crosswalk |
| ANCHOR | `anchor-audit.json` and content-addressed fragments |
| TREE | `proof-units.json` typed DAG |
| MACHINE | `machine-closure.json`, M0-L, trust zero |
| READABLE | `readability-review.json`, R0 reverse ledger |
| VALIDATE | task-local `check_stage5_theorem_item.py --no-lean` |
| RELEASE | `release-decision.json`, provisional Master handoff |

Canonical Master must independently recompute the elaborated root,
transitive constant census, cold replay, mutation trace, and Lean closure.
