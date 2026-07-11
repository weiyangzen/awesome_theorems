# THM-M-0420 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the Hilbert class field theorem. The legacy
`S1_M_075.lean` file is a discovery input only and supplies no accepted statement or proof credit.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | For every number field `K`, existence of a finite abelian extension `H/K` unramified at every finite prime and maximal among finite unramified abelian extensions | Exact Lean elaboration and expression fingerprint belong to the statement phase |
| Reciprocity | The Artin map identifies `Gal(H/K)` with the ideal class group of `K` | Included in the intended characterization; direction/convention must be frozen later |
| Maximality | Every finite everywhere-unramified abelian extension of `K` admits a `K`-embedding into `H` | A candidate encoding exists in the legacy file but is not accepted here |
| Uniqueness | Any two fields satisfying the characterization are isomorphic over `K` | Consequence/companion obligation, not silently substituted for existence |
| Ramification boundary | Unramified at all finite primes | Infinite-place convention is explicitly outside this intake root pending source audit |
| Foundations | Lean 4 kernel plus pinned mathlib, with classical/choice/quotient use audited | Exact toolchain, imports, axioms, and dependency closure remain open |

The human claim, binders, candidate formal surface, degenerate boundaries, and trust profiles are
structured in `intake.json`. The relationship between repository wording, mathematical sources,
and the legacy Lean candidate is recorded in `source_statement_crosswalk.md`.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M3, R3]`. The first failed theorem gate is
the exact Lean statement gate: there is no rev-5.6 elaborated expression hash, environment
fingerprint, accepted transport, or mutation evidence. No theorem completion is claimed.

## Validation

The exact intake-only checks and their results are recorded in `validation.md`. They establish
target membership, repository-standard consistency, JSON syntax, and dossier reference integrity
only. Master acceptance and every dependent phase remain outstanding.
