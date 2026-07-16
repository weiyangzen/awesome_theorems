# Anchor audit validation record

Item: `S56-M-0390-ANCHOR_AUDIT`
Worker base revision: `c5037228977a81948bbd6119e1728b4b65b9924e`
Frozen inventory: `M0390-anchor-inventory-2026-07-17-2`

## Result

The immutable local closure contains no terminal Catalan/Mihailescu theorem. Pinned mathlib's
`Q174955` row has no declaration anchor. `Polynomial.flt_catalan` is a checked polynomial theorem
with a mismatched carrier and conclusion. The other identified declarations are support APIs only.

The replayed protocol covers the required lanes in order: repo-local, pinned mathlib, official
primary projects, other immutable public projects, statement-only collections, historical or other
provers, and primary human sources. Every lane has content-bound evidence, an access boundary, and a
reopen condition. Classification is complete for the frozen six-candidate inventory, but discovery
saturation is not claimed.

At Formal Conjectures revision `7871d8fc7a8164a1ac16c3765b40c25ce015b681`,
`Catalan.catalans_conjecture` ends in `by sorry`; it is `M5`, not upstream closure. The project's
`Nat.IsPerfectPower` is support infrastructure. No dependency was fetched or added. The canonical
root is `M3/E4`: its proposition elaborates locally, but no terminal proof body was found.

The v2 hard-parent and transitive-ancestor closure is empty, so the required parent inspection order
is the empty list and was traversed exactly once. The sole weak shared-module group,
`SHARED-MODULE-32f9c9eb1b52d871`, was checked through member `THM-M-0133` and classified
`not_applicable`: co-mention of `Mathlib.NumberTheory.FLT.Polynomial` supplies neither an exact body
nor a checked transport, and no provider checkbox, receipt, or proof credit transfers.

## Commands and results

| Command | Result |
|---|---|
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0390/check_anchor_audit.py` | exit 0; exactly one typed semantic JSON result, `phase_predicate_proven=true`, `audit_complete=false`, `theorem_complete=false` |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets |
| `python3 scripts/stage1_target.py show THM-M-0390` | exit 0; rank 4, planned, incomplete |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0390/Statement.lean` | exit 0; canonical statement surface re-elaborated |
| JSON parsing of all anchor outputs and `.stage1-worker-selftest.json` | exit 0 |
| `git diff --check -- Stage1_Instances/THM-M-0390 .stage1-worker-selftest.json` | exit 0 |
| `python3 Docs/tools/check_stage1_standard.py` | exit 1; expected worker-integration boundary: fresh deterministic graph generation sees new target-owned JSON/receipt inventory while the checked-in derived DAG remains unchanged |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | exit 1; same target-scoped projection drift; master must track outputs, regenerate the derived DAG, and replay transactionally |

Known limitation: public-project discovery is not claimed exhaustive because prior anonymous
queries were access-limited. The pinned mathlib source revision is inspectable, but its module oleans
are absent, so no new mathlib import probe was fabricated. These limits do not prevent truthful
classification of the frozen inventory, but they prevent saturation and `AUDIT-Z` claims.
Final HEAD role/blob binding, independent review, SSOT CAS, H0/R0, proof, hermetic validation, and
release remain the responsibility of integration or downstream phases.
