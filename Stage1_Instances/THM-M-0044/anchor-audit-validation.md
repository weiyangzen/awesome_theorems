# THM-M-0044 anchor-audit validation

Item: `S56-M-0044-ANCHOR_AUDIT`

Base revision: `72f928bdf1a47d7c119826db45575bd02a3a63ce`

Validation date: `2026-07-13` (`Asia/Shanghai`)

## Result

The node-scoped audit classified three immutable candidate packages. Pinned mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95` supplies exact singular-value, Hermitian spectral,
basis-extension, unitary-matrix, and matrix/linear-map interfaces. All eleven selected interfaces
elaborate in the existing pinned environment. Their proof-bearing declarations report only
`propext`, `Classical.choice`, and `Quot.sound`; the elementary Gram-Hermitian theorem omits choice.
None constructs both unitary factors or proves the frozen rectangular equality.

`facebookresearch/atlas-lean@34ffed396f376454c1a9b297f3fd74c5c801fb50` defines a Real-only
rank-indexed `SVD` record and reconstruction predicate, but its vector families are unconstrained by
orthonormality and it contains no theorem proving the record exists for every matrix. The project
uses matching Lean/mathlib pins, but the statement mismatch, absent existence proof, adjacent
placeholders, and restrictive license prevent proof credit.

`mrdouglasny/gaussian-field@d63a28568a75d99f6cb27af1f888a49a69855a66` proves
`GaussianField.nuclear_sequence_svd` from a compact self-adjoint spectral theorem. Its inspected
direct source chain is placeholder-free, but it concerns summable sequences into an
infinite-dimensional real Hilbert space. It provides neither the finite Real-and-Complex matrix
domain nor two square unitary factors and the explicit rectangular equality. It also uses Lean
4.30.0 and a different mathlib pin. It is therefore a source-level near-miss, not `M1` evidence.

The accepted root remains `[H1, M3, R3]`. This completes the assigned bounded anchor-inventory phase
only, pending master acceptance; no broader audit or theorem-completion claim is made.

## Commands and exact outcomes

| command | exit | outcome |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets and ranks 1..1546 passed |
| `python3 scripts/stage1_target.py show THM-M-0044` | 0 | rank 1084, planned, L0/rework-required, theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | `8a178386...ea95`, tree `bdc39a...e5c2b` |
| all-materialized-package `rg` search for `singular value decomposition`, word `SVD`, and `singularValues` | 0/1 as query-dependent | only mathlib singular-value properties were found; no installed exact SVD declaration |
| immutable Atlas archive/source inspection and SHA-256 validation | 0 | revision `34ffed...fb50`; Real-only underconstrained record, no all-matrix existence theorem; archive `925cc0...9aa2` |
| immutable gaussian-field archive/source inspection and SHA-256 validation | 0 | revision `d63a28...5a66`; real infinite-dimensional nuclear-sequence mismatch; archive `3d0504...961c` |
| bounded Sourcegraph and GitHub repository searches | 0 | no exact public candidate identified; response hashes are frozen in `anchor-audit.json` |
| GitHub code-search request | 0 as HTTP capture | HTTP 403 anonymous rate-limit response; recorded as a limitation, not negative evidence |
| `lake env lean ../../Stage1_Instances/THM-M-0044/AnchorAudit.lean` from `Formalizations/Lean` | 0 | eleven interfaces elaborated and ten exact axiom reports matched; stdout SHA-256 `1b0e9a...245b` |
| `python3 -B Stage1_Instances/THM-M-0044/check_anchor_audit.py` | 0 | all pins, source hashes, exact candidate boundaries, archive members, probe output, and unchanged M3 root agreed |
| `python3 -m json.tool` on the audit, receipt, and worker packet | 0 | all structured artifacts parsed |
| prohibited-construct scan over target-owned Lean modules | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, bodyless declaration, `opaque`, or `unsafe` construct |
| `git diff --check -- Stage1_Instances/THM-M-0044 .stage1-worker-selftest.json` | 0 | no whitespace diagnostics |

No `lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation was performed. The
automation-provided canonical pinned `.lake` artifacts were used read-only. External candidates were
inspected through content-addressed immutable archives under `/tmp`, never added as dependencies.

## Status boundary

This is provisional node evidence. Public-code search is bounded and discovery saturation is false.
No exact terminal body or local integration route was found. Obligation freezing, proof construction,
H0/R0 review, accepted transitive trust, hermetic and independent validation, `AUDIT-Z`, and
`THEOREM-Z` remain open.
