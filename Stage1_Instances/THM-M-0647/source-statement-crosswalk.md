# Source-statement crosswalk

## Repository source boundary

The Stage0 record and its research precursor provide only the Chinese title, the year `1927`, the
attribution `Lowenheim/Skolem/Alfred Tarski`, and the gloss "an infinite model has elementarily
equivalent models of different cardinalities." They cite no edition, theorem, page, proof,
assumption list, or errata. They are secondary metadata (`E5`), not primary proof evidence and not
enough for `H0`.

The historical attribution itself needs review: Lowenheim's and Skolem's early results, Tarski's
elementary-substructure formulation, and modern combined upward/downward statements need not share
one literal proposition or the repository's date. The source phase must choose an immutable primary
edition or a precisely identified authoritative critical edition, inspect its wording and proof,
and record errata and an independent reviewer.

## Crosswalk

| Repository phrase | Provisional mathematical reading | Candidate Lean surface | Open exactness question |
|---|---|---|---|
| "model" | nonempty first-order `L`-structure `M` | `[L.Structure M]`, `[Infinite M]` | Does the selected source permit empty structures? |
| "infinite" | `#M` is infinite; target cardinals satisfy `aleph_0 <= kappa` | `Infinite M`, `aleph_0 <= kappa` | Which infinitude convention and lower bound? |
| "different cardinalities" | every admissible `kappa`, hence sizes on available sides of `#M` | `#N = kappa` | All cardinals, one unequal cardinal, or paired up/down claims? |
| "elementarily equivalent" | same truth value for every sentence | `M ≅[L] N` | Equivalence only, or a directional elementary embedding? |
| language-size condition | `#L <= kappa` with universe lifts | lifted comparison with `L.card` | Exact lift levels and whether `max(aleph_0, #L)` is stated explicitly? |

## Pinned formal candidate

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.ModelTheory.Satisfiability` contains
`FirstOrder.Language.exists_elementarilyEquivalent_card_eq`. Its documented and checked type says
that, for infinite `M`, every `kappa` satisfying `aleph_0 <= kappa` and the lifted language-cardinal
bound is the cardinality of a bundled `L`-structure elementarily equivalent to `M`.

This is an exact formal source anchor candidate (`E3`), not an accepted cross-source transport. The
statement phase must compare it to the selected human theorem binder by binder, elaborate a
canonical repo declaration, check any transport, and mutation-test hypotheses, domain, binder
scope, and boundary cases before the anchor can receive proof credit.
