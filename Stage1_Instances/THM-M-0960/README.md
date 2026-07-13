# THM-M-0960 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for `THM-M-0960`, the repository label
`Ellenberg-Gijswijt定理` (Ellenberg-Gijswijt theorem). The catalog supplies Jordan Ellenberg and
Dion Gijswijt, the year 2017, and only the gloss `cap集的上界`, literally "an upper bound for cap
sets." Its `已验证` status is untrusted inventory metadata, not a source audit, an exact Lean
proposition, or proof evidence.

The primary published source lead is Jordan S. Ellenberg and Dion Gijswijt, *On large subsets of
F_q^n with no three-term arithmetic progression*, *Annals of Mathematics* 185 (2017), 339-343,
DOI `10.4007/annals.2017.185.1.8`. Theorem 4 gives a finite-field monomial-count bound for a more
general three-variable equation. Corollary 5 gives the cap-set specialization
`|A| = o(2.756^n)` in `(Z/3Z)^n`. Both were inspected in the publisher-hosted article, but the
catalog does not select between them or the surrounding qualitative exponential statement.

The canonical statement therefore remains null at intake. A source decision must still fix the
field and ambient space, the precise meaning of a cap set and a nontrivial progression, whether the
root is Theorem 4 or Corollary 5, the exact finite versus asymptotic bound, the monomial-count and
real-exponent conventions, the quantification over `n`, and all rounding and boundary cases.
Selecting one of these proposition-changing variants here would silently substitute mathematics
for the catalog gloss.

`IntakeProbe.lean` checks only pinned finite-vector-space, cardinality, and three-term-progression
interfaces. It defines a prospective cap-set predicate but no upper-bound theorem. A bounded
repo-local and pinned-mathlib search found Roth-style qualitative three-term-progression results,
but no Ellenberg-Gijswijt, slice-rank, cap-set, or exponential `2.756^n` declaration. This is intake
discovery only, not an exhaustive anchor audit or proof.

The provisional root vector is `[H1, M4, R4]`: a complete published proof lead is identified, but
the exact catalog-to-source proposition, corrections, errata, and independent source review are
open; no usable source-identical formal artifact is credited; and no source-faithful proof
reconstruction exists. All six downstream tasks remain open. No H0, M0, R0, accepted execution
state, audit completion, theorem completion, or master acceptance is claimed.
