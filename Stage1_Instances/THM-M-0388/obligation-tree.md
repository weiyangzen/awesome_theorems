# THM-M-0388 Frozen Obligation Tree

## Root and composition

`M0388-ROOT` is exactly the fingerprinted `PellEquationStatement`. Its two direct premises are the
local-to-mathlib nonsquare transport (`M0388-S-PREDICATE`) and the exact imported existence theorem
(`M0388-X-PELL`). `ObligationTree.lean` treats the imported predicate and theorem as explicit
hypotheses and checks that both are consumed to produce the exact root. It asserts neither premise.

## Statement and transport layer

The local predicate is `not exists k : Int, k*k=D`; mathlib spells this `not IsSquare D`. The
adapter proof unpacks the `IsSquare` witness and uses equality symmetry. It is a required transport,
not a second copy of Pell existence. Statement boundary cases and the alternate conjunctive form
remain recorded by the statement phase and do not enlarge this proof denominator.

## Imported proof-body expansion

The body of `Pell.exists_of_not_isSquare` at pinned mathlib revision `8a178386` is not treated as a
one-line primitive. The registry exposes its substantive route:

1. derive irrationality of `sqrt D` from nonsquareness;
2. obtain infinitely many sufficiently close rational approximants;
3. pigeonhole their bounded integral norm into an infinite nonzero norm fiber;
4. choose two distinct rationals with numerator and denominator congruent modulo the norm;
5. turn those congruences into divisible bilinear numerators and integral quotient coordinates;
6. prove the quotient norm is one and its second coordinate is nonzero.

The typed refinement graph records this flow. The proof graph makes each package root-relevant.
The approximation theorem, finite `ZMod` pigeonhole step, and tactic-heavy terminal identity remain
explicit review and provenance boundaries. Every current semantic ledger is at most four steps,
but that number is not an R0 or machine-closure claim.

Normalization by signs, separate mathematical case branches, choice-dependent auxiliary objects,
and a transport back from a different theorem orientation are not additional layers in this exact
proof body. They are not marked excluded obligations: the frozen architecture simply does not
introduce them. The norm-zero contradiction is retained as `M0388-B-NORM` rather than hidden.

## Trust and status boundary

`M0388-X-TRUST` owns the transitive import, axiom, tactic, finite-computation, and replay boundary.
The source has an explicit proof body and no visible placeholder or custom axiom, but the worker's
pinned cache lacks `Mathlib.NumberTheory.Pell.olean`. Source inspection is therefore E3 evidence,
not kernel closure. No `.lake` update or build is permitted for this handoff.

The frozen denominator has eleven required obligations and zero exclusions. Aliases, the stronger
biconditional, and the repository-local legacy wrapper share the imported terminal proof-body ID and
receive no duplicate credit. This phase claims architecture self-test only: H0, M0, R0, audit
completion, theorem completion, validation, release, and master acceptance all remain open.
