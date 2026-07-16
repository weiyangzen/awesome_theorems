# THM-M-0123 anchor-audit validation

Item: `S56-M-0123-ANCHOR_AUDIT`

Worker base: `307c34d30fc3763c82a944a142ae922b48ff18aa`

## Decision

The frozen ten-candidate inventory contains no valid exact Lean 4 proof anchor
for `Stage1Instances.THM_M_0123.MordellTarget`. The repo-local exact target is
statement-only (`M3`). The legacy `S1_M_042` shape and same-family
`THM-M-0395` dossier use materially different predicate packages and contain
no Mordell/Faltings root body. Their artifacts and checkbox states transfer no
acceptance or proof credit.

Pinned mathlib at
`8a178386ffc0f5fef0b77738bb5449d50efeea95` supplies the number-field,
scheme-morphism, sheaf-cohomology, Northcott, and descent substrate checked by
`AnchorAudit.lean`. The support wrapper has no axioms, but bounded-height
finiteness and abstract finite generation do not prove finiteness of all
rational points. Mathlib's `Q240950` row only names Faltings's theorem and has
no declaration.

The only direct public Lean declaration in the content-bound observations is
Atlas `faltings_theorem` at
`34ffed396f376454c1a9b297f3fd74c5c801fb50`. It is Q-only, stores genus as a
free natural number, lacks a checked transport to the frozen scheme/H1 target,
and ends in `by sorry`. It is `M5`, not a proof anchor. The recorded Formal
Conjectures tree has no Faltings/Mordell path. Public search saturation is not
claimed because anonymous code search was access-failed.

All seven prescribed lanes are classified in order: repo-local, pinned
mathlib, official primary projects, other immutable public projects,
statement-only collections, historical or other provers, and primary human
sources. The Faltings publication is a preliminary human-source anchor only;
exact wording, conventions, derivation, corrections, and independent review
remain open, so no H0 credit is assigned.

## Dependency context

The exact direct/transitive parent closure is empty. The supplied
`parent_inspection_order` is therefore `[]` and was traversed exactly once
before proof-related probing. Hard edges, reuse hints, and shared groups are
also empty. The schema-1.1 ledger records this complete empty audit without
claiming mathematical independence, reusing a declaration, or inheriting
acceptance.

## Commands

| Command | Result |
|---|---|
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0123/check_anchor_audit.py` | exit 0; exactly one typed semantic JSON result with `phase_predicate_proven=true`, `audit_complete=false`, and `theorem_complete=false` |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0123/Statement.lean` | exit 0; exact target and checked statement transports re-elaborated |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0123/AnchorAudit.lean` | exit 0; pinned support declarations elaborated and the Northcott wrapper reported no axioms |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique uniform-L0 targets |
| `python3 scripts/stage1_target.py show THM-M-0123` | exit 0; execution rank 42, planned, theorem incomplete |
| JSON parsing of the four anchor JSON outputs and receipt | exit 0 |
| `git diff --check -- Stage1_Instances/THM-M-0123 .stage1-worker-selftest.json` | exit 0; no whitespace errors |
| `python3 Docs/tools/check_stage1_standard.py` | exit 1; fresh deterministic theorem-DAG generation sees the unintegrated target-owned inventory and differs from the checked-in derived projection |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | exit 1; same target-scoped evidence-inventory projection drift; workers are forbidden to rewrite the generated authority |

The worker reused the existing pinned `.lake` closure read-only. It ran no
`lake update`, `lake build`, dependency clone/fetch, checkout, or package
mutation. The root remains `H4/M3/R3`; obligation-tree, proof, trust,
readability, hermetic, independent-review, release, `AUDIT-Z`, and `THEOREM-Z`
gates remain open. Final HEAD role/blob binding and dependency-ordered master
acceptance belong to the integration lane.
