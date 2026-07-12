# THM-M-0509 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for Chen's theorem. The repository gloss
says that every sufficiently large even number is a sum of a prime and an almost prime. This fixes
the broad theorem family but does not define "almost prime" or supply a primary-source theorem,
quantifier threshold, multiplicity convention, or boundary conditions.

The provisional scope is the classical `P + P_2` result: every sufficiently large even natural
number is a prime plus a positive natural number having at most two prime factors counted with
multiplicity. Whether the selected source includes primes themselves among the `P_2` numbers, and
the exact formulation of "sufficiently large", remain statement-phase decisions. The provisional
root is `[H1, M4, R4]`.

A pinned Lean probe confirms only that prime predicates, natural-number factorization, finite
support cardinality, and eventual quantification are available. No canonical Lean expression,
source acceptance, proof, audit completion, or theorem completion is claimed. Exact checks are
recorded in `validation.md`.

