# THM-M-0032 scope map

## Preserved claim

The admissible root is the catalog's universal statement: every regular local ring is a unique
factorization domain. The 1959 paper's Theorem 5 is a direct statement locator. Under pinned
mathlib's commutative-ring convention, the statement phase freezes this as
`forall (R : Type u) [CommRing R] [IsRegularLocalRing R], UniqueFactorizationMonoid R`.

## Statement decisions

The machine statement fixes these encoding choices:

1. `R : Type u` is universally quantified with `CommRing R` and `IsRegularLocalRing R` instances.
2. `IsRegularLocalRing` supplies local, Noetherian, and nontrivial structure; no redundant premise
   and no explicit domain premise is added.
3. The conclusion is `UniqueFactorizationMonoid R` on the same carrier.
4. Fields and dimension zero are included; `Rat` checks the field boundary. The zero ring is
   excluded by inherited nontriviality.
5. An explicit-hypothesis formulation is credited only through the checked iff in `Statement.lean`.

The exact transport from the primary paper's incorporated definitions to these modern definitions,
including the domain consequence and UFD conventions, remains open on H and blocks H0 rather than
M3 statement elaboration.

## Source proof boundary

The primary paper proves a dimension-at-most-three result and then invokes a reduction attributed
to Nagata for the unrestricted theorem. These are proof dependencies, not extra hypotheses on the
root. A dimension-three-only result or the complete-local reduction cannot replace Theorem 5.
The paper's use of homological dimension must be mapped to exact definitions before its proof can
support H0 or an obligation tree.

## Explicit exclusions

- Do not substitute the Auslander-Buchsbaum formula relating projective dimension and depth.
- Do not weaken the root to regular local rings of dimension at most three.
- Do not replace it with the reverse fact that a local principal ideal domain is regular.
- Do not prove only that a regular local ring is a domain, Noetherian, factorial in a selected
  special case, or has principal height-one primes without a checked equivalence to UFD.
- Do not add completeness, equicharacteristic, a coefficient field, finite dimension, or another
  premise absent from the accepted root.
- Do not use a structure field, typeclass premise, oracle, or unchecked certificate that already
  assumes unique factorization.
- Do not treat the catalog's `verified` label, a source citation, a declaration name, or successful
  API elaboration as proof credit.

## Formal feasibility boundary

Pinned mathlib's `IsRegularLocalRing R` extends `IsLocalRing R` and `IsNoetherianRing R` for a
commutative ring and uses the maximal-ideal span-rank/Krull-dimension equality. Its UFD interface is
`UniqueFactorizationMonoid R`. The exact binder shape is frozen by `Statement.lean` with the single
direct import `Mathlib.RingTheory.RegularLocalRing.Defs`. Its explicit expression, environment,
four mutation classes, and field boundary are fingerprinted in `statement.json`.

No discovery protocol, obligation registry, typed graph, target proof body, proof state, or proof
credit is frozen by the statement phase.
