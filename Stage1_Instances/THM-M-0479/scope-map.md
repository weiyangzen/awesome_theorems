# Scope map

## Preserved catalog scope

The received claim is exactly "there are infinitely many primes in arithmetic progressions."
Together with the title, attribution, and date, it identifies Dirichlet's theorem on primes in
arithmetic progressions. It does not say whether one progression is fixed or all admissible
progressions are quantified, nor does it state the conditions that make a progression admissible.
Intake preserves the classical family without silently resolving those missing binders and
hypotheses.

The likely mathematical components, none yet credited as the canonical proposition, are:

- a positive natural-number modulus `q`;
- a residue representative or class `a` coprime to `q`;
- natural primes lying in the class `a` modulo `q`; and
- infinitude of that set, equivalently existence of such a prime above every natural bound.

## Proposition-changing decisions

An approved source and independent review must settle the following before statement execution:

1. Whether the result quantifies over every modulus and reduced residue class, and the exact
   ordered binders for the modulus, class, coprimality evidence, bound, and prime.
2. Whether the modulus is a positive natural, nonzero natural, or positive integer, and whether the
   residue is a natural representative, an integer, or an element of `ZMod q`.
3. Whether admissibility is stated by `Nat.Coprime a q`, integer `IsCoprime a q`, or
   `IsUnit (a : ZMod q)`, including checked transports among any credited encodings.
4. Whether progression membership is divisibility of `p - a`, natural `Nat.ModEq`, integer
   `Int.ModEq`, or equality in `ZMod q`, with all coercions and sign conventions explicit.
5. Whether infinitude is a `Set.Infinite` conclusion, existence above every bound, or another
   source-selected formulation, and which logical relationship connects alternate forms.
6. The selected foundation, classical-choice, trusted-computing-base, and computation policies.

These choices are not mere spelling changes. In particular, omitting coprimality makes the usual
universal conclusion false, while proving one fixed progression would be strictly weaker than the
standard theorem family.

## Boundary and mutation cases

Statement review must explicitly resolve `q = 0`, `q = 1`, `a = 0`, negative integer
representatives, representatives outside the conventional interval, non-coprime pairs, and the
progression's first term and indexing convention. The likely nonzero-modulus encoding excludes
`q = 0` and includes `q = 1`, while the unit/coprime hypothesis excludes non-reduced classes, but
intake does not adopt those decisions without a reviewed source crosswalk. Later mutations must
test removed coprimality, changed prime or residue domain, binder scope, and modulus boundary.

## Explicit non-substitutions

- Do not replace the universal reduced-residue-class theorem by infinitude of all primes, one
  chosen progression, primes congruent to one, or a finite computation.
- Do not replace infinitude by the prime number theorem for arithmetic progressions, asymptotic
  equidistribution, density, or an error estimate; those are stronger and differently typed.
- Do not omit coprimality or treat a non-coprime residue class as a general conclusion-bearing
  case.
- Do not replace natural primes by signed integers counted twice, prime ideals, irreducibles in
  another ring, or prime powers.
- Do not treat the separate `THM-M-0500` dossier, a theorem name, module documentation, the catalog
  label `已验证`, or a successful API probe as source identity or theorem completion evidence.
- Do not encode the result as an axiom, opaque premise, certificate, or hypothesis that already
  contains the desired infinitude conclusion.

## Formal discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.NumberTheory.LSeries.PrimesInAP` explicitly presents Dirichlet's theorem. It exposes
`Nat.infinite_setOf_prime_and_eq_mod`, unbounded-existence forms for `ZMod`, integer congruence, and
natural congruence, and `Nat.infinite_setOf_prime_and_modEq`. The discovery-only probe checks these
declarations and adjacent predicates. They are direct candidates, not a frozen source transport or
an anchor-audit receipt. Minimal import confirmation, canonical expression elaboration, expression
and environment fingerprints, checked transports, mutations, proof-body provenance, and trust
closure remain downstream.
