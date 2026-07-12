# THM-M-0509 rev-5.6 dossier

This directory is the fail-closed `planned` intake dossier for Chen's theorem. The repository gloss
says that every sufficiently large even number is a sum of a prime and an almost prime. This fixes
the broad theorem family but does not define "almost prime" or supply a primary-source theorem,
quantifier threshold, multiplicity convention, or boundary conditions.

The provisional scope is the classical `P + P_2` result: every sufficiently large even natural
number is a prime plus a positive natural number having at most two prime factors counted with
multiplicity. Whether the selected source includes primes themselves among the `P_2` numbers, and
the exact formulation of "sufficiently large", remain statement-phase decisions. The provisional
root is `[H1, M4, R4]`.

The statement phase now freezes the intake-selected classical convention: `P2` means a prime or a
product of two primes, with repeated prime factors permitted. `Statement.lean` elaborates the exact
uniform-threshold `Nat` target using only `Mathlib.Data.Nat.Prime.Basic`; `statement.json` and
`statement-validation.md` record its expression hash, mutations, boundary cases, pins, and exact
commands. Primary-source pinpoint acceptance remains for the source/anchor audit. No proof, audit
completion, or theorem completion is claimed.
