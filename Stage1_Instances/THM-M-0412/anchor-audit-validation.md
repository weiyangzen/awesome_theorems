# Anchor Audit Validation Record

Item: `S56-M-0412-ANCHOR_AUDIT`

Worker base revision: `307c34d30fc3763c82a944a142ae922b48ff18aa`

Frozen inventory: `M0412-anchor-inventory-2026-07-17-1`

## Result

The complete v2 hard-parent, transitive-ancestor, hard-edge, reuse-hint, and shared-group closure is
empty. The supplied parent inspection order was therefore traversed exactly once as an empty list.
The refreshed schema-1.1 ledger records that result and consumes no proof body, receipt, or checkbox
credit.

All seven prescribed discovery lanes have content-bound results. The repo-local catalog still does
not identify a proposition. The legacy `S1_M_021.lean` module is an abstract Nagell-Lutz-shaped
interface with projection and gate lemmas, not a concrete theorem or terminal proof. Pinned mathlib
lists Nagell-Lutz in `docs/1000.yaml` without `decl` or `decls`; its Weierstrass, discriminant,
two-torsion, and affine-point declarations are support infrastructure only. The tracked public
search observations identify no immutable external Lean 4 candidate. Historical evidence instead
exposes an unresolved identity conflict between the catalog's topic and date.

Classification is complete for the frozen six-candidate inventory. This is a truthful negative
anchor audit, not a proof or saturation result. The root remains `H5 / M4 / R4`; the exact source
identity, canonical target, H0 review, proof architecture, proof body, audit completion, and theorem
completion remain open.

## Validation Commands

The worker handoff records these exact commands and their exit results:

| Command | Result |
|---|---|
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0412/check_anchor_audit.py` | exit 0; exactly one typed semantic JSON result with `phase_predicate_proven=true`, `audit_complete=false`, and `theorem_complete=false` |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0412/AnchorAudit.lean` | exit 0; six pinned adjacent APIs elaborated, with no target or proof credit |
| `python3 Docs/tools/check_stage1_standard.py` | exit 0 before target-owned audit outputs were added; rev-5.6 structural authorities and contract passed. Final replay exits 1 only because fresh derived-DAG generation observes the new target-owned JSON/receipt inventory while the worker cannot edit that projection. |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | exit 0 before target-owned audit outputs were added; 1546 nodes and acyclicity passed. Final replay exits 1 on the same expected integration projection drift. |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique uniform-L0 targets |
| `python3 scripts/stage1_target.py show THM-M-0412` | exit 0; rank 21, planned, legacy artifacts unaccepted, theorem incomplete |
| JSON parsing for the ledger, protocol, evidence, inventory, receipt, and handoff | exit 0 |
| `git diff --check -- Stage1_Instances/THM-M-0412 .stage1-worker-selftest.json` | exit 0 |

The current phase contract requires final HEAD tracking and SHA-256/Git-blob binding for selected
roles, exactly one authority-owned base validator, independent review, replay, and SSOT CAS. This
worker can bind its output bytes and identify the declared validator candidate, but it cannot make
the validator exist at the already fixed base revision. The integration lane must truthfully apply
that base-existence gate; no worker command or receipt can infer master `phase_accepted` from exit
zero.
