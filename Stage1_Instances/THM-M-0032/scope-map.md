# THM-M-0032 scope map

## Preserved claim

The admissible root is the catalog's universal statement: every regular local ring is a unique
factorization domain. The 1959 paper's Theorem 5 is a direct statement locator. At intake this
remains a mathematical scope locator rather than a frozen canonical Lean proposition.

## Decisions required at statement freeze

An immutable source packet and independent review must freeze all proposition-changing choices:

1. The paper's convention for a ring, including commutativity, identity, and nontriviality.
2. The exact definition of local ring and its distinguished maximal ideal.
3. The Noetherian premise and the homological or dimension-theoretic definition of regularity used
   by the paper, with a checked transport to a modern equivalent definition.
4. Whether integrality is an explicit premise or a theorem derived from regular localness.
5. The exact UFD definition, including existence and uniqueness up to units, and its relationship
   to modern atomic/prime-element and height-one-prime formulations.
6. The ordered ring and structure binders, universe parameters, typeclass dependencies, and
   conclusion encoding.
7. The treatment of fields and zero-dimensional rings, the zero ring, positive-dimensional rings,
   and any use of completion or localization in source dependencies.
8. The foundation, choice, quotient, localization, TCB, and computation profiles.

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
`UniqueFactorizationMonoid R`. A natural schematic binder shape is therefore
`(R : Type u) [CommRing R] [IsRegularLocalRing R] : UniqueFactorizationMonoid R`, but intake does
not freeze or credit this expression. The exact
source transport, domain consequence, imports, elaborated expression, and mutations are open.

No canonical Lean target, expression fingerprint, checked alternate encoding, discovery protocol,
obligation registry, typed graph, proof state, or proof credit is frozen at intake.
