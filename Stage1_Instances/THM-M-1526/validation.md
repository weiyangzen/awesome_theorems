# Intake validation

Base revision: `594dbb735284e7b81f51ce813a9c3200fd55f610`.

Validation covers manifest consistency, dossier structure, scoped intake invariants, and whitespace.
No canonical Lean expression exists yet, so this intake records no kernel claim.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1526` | exit 0; rank 194, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-1526/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-1526/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-1526` | exit 0; no output |

Exact source inspection, canonical elaboration, anchor audit, proof, hermetic replay, and independent
review remain open. These are downstream gates, not claims of this planned intake.

## Validation-node execution

Item: `S56-M-1526-VALIDATION`. Base revision:
`446447c65190dc818b074bf543171f807e9b4651`.

The node validator replayed `Statement.lean`, `ObligationTree.lean`, and `Proof.lean` into a fresh
temporary output directory using the existing pinned Lean environment. `Validation.lean` separately
reconstructs the exact root directly from the frozen statement rather than importing either proof
module. Seven printed declarations reported exactly `propext`, `Classical.choice`, and `Quot.sound`;
the source scan found no `sorry`, `admit`, `sorryAx`, bodyless axiom, or unsafe declaration.

| Command | Exit | Result |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-1526/check_validation.py` | 0 | exact proof and separate exact-target reconstruction elaborated; input hashes and clean pinned mathlib agreed |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-1526` | 0 | rank 194, planned, L0/rework-required, theorem incomplete |
| `python3 Stage1_Instances/THM-M-1526/check_statement.py` | 0 | frozen exact statement and mutations revalidated |
| `python3 Stage1_Instances/THM-M-1526/check_anchor_audit.py` | 0 | target hashes, clean mathlib pin, and twelve probes revalidated |
| `python3 Stage1_Instances/THM-M-1526/check_obligation_tree.py` | 0 | 17 obligations, 34 typed edges, and conditional composition passed |
| `python3 Stage1_Instances/THM-M-1526/check_proof.py` | 0 | exact root elaborated without placeholders |
| `python3 -m json.tool Stage1_Instances/THM-M-1526/validation-spec.json` | 0 | structured recipe parsed |
| `python3 -m json.tool Stage1_Instances/THM-M-1526/validation-receipt.json` | 0 | provisional receipt parsed |
| `git diff --check -- Stage1_Instances/THM-M-1526 .stage1-worker-selftest.json` | 0 | no whitespace errors |

This is deliberately nonrelease evidence. The authoritative frozen graph remains `M3` with
`M1526-N-PRODUCT` and `M1526-L-SLASH-SQUARE` open pending master reconciliation. The shared warm
`.lake` is not a cold empty-cache build, no full TCB/SBOM/offline archive was produced, and the
separate reconstruction ran in this same clone and cache rather than on a distinct independently
provisioned runner. Thus hermetic release, independent verification, master acceptance, `AUDIT-Z`,
and `THEOREM-Z` fail closed; `audit_complete=false` and `theorem_complete=false`.
