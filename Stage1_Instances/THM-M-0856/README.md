# THM-M-0856 rev-5.6 dossier

This directory is the fail-closed `planned` dossier for `THM-M-0856`, the repository's
`Tutte定理` (Tutte theorem). The catalog gives William Tutte, 1947, and only the gloss
`完美匹配存在的条件` (a condition for the existence of a perfect matching). Its `已验证`
field is untrusted metadata and supplies no source or proof credit.

## Intake result

The name, date, and gloss strongly identify Tutte's 1-factor theorem for finite graphs: a finite
graph has a perfect matching exactly when deleting every vertex subset `U` leaves at most `|U|`
connected components of odd order. The leading primary-source identity is W. T. Tutte, *The
Factorization of Linear Graphs*, Journal of the London Mathematical Society s1-22(2) (1947),
107-111, DOI `10.1112/jlms/s1-22.2.107`. Crossref and OpenAlex metadata confirm that identity, but
no full primary text, exact theorem locator, incorporated definitions, correction history, or
independent source review is admitted. The source mapping therefore remains `H1`, not `H0`.

## Formal boundary

Pinned mathlib contains a direct proof-bearing candidate in
`Mathlib.Combinatorics.SimpleGraph.Tutte`: `SimpleGraph.tutte` states that a finite simple graph has
a perfect matching if and only if it has no `IsTutteViolator`. The violator predicate unfolds to
strictly more odd connected components after deleting `U` than vertices in `U`. `IntakeProbe.lean`
checks these exact interfaces and records the candidate axiom report. This is unusually strong
intake discovery, but statement identity, minimal-import and mutation gates, terminal-body
provenance, and master acceptance belong to later ordered phases. The candidate is classified
provisionally as `M3`, not credited as `M0-W`.

The intake's provisional vector is `[H1, M3, R4]`. Its historical receipt supplies no canonical
Lean statement, accepted proof state, H0, M0, R0, audit completion, theorem completion, accepted
receipt, or master acceptance.

## Statement result

`Statement.lean` now freezes the intake-selected conventional claim as
`Stage1Instances.THM_M_0856.TutteOneFactorTarget`: every finite simple graph has a perfect matching
if and only if every vertex deletion leaves at most as many odd connected components as deleted
vertices. Its only direct import is `Mathlib.Combinatorics.SimpleGraph.Matching`, which provides the
statement vocabulary without importing the proof-bearing `SimpleGraph.Tutte` module.

`check_statement.py`, `statement.json`, `statement-validation.md`, and `statement-receipt.json`
record the explicit expression and environment fingerprints, two checked `Iff` transports, sole-
import deletion, and the four required structural mutations. `check_statement_artifacts.py`
replays and reconciles that packet. This is a worker-self-tested statement proposal pending
dependency-ordered master acceptance. The vector remains `[H1, M3, R4]`; no upstream proof body,
anchor audit, accepted state, audit completion, or theorem completion is claimed.
