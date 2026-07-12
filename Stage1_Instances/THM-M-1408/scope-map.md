# Scope map

## Included theorem family

- Bernoulli shifts built from a source-specified discrete probability base and product measure.
- A source-specified shift action, most likely the invertible two-sided integer shift.
- The exact entropy invariant selected by the source, with its logarithm and endpoint conventions.
- A measurable, measure-preserving isomorphism modulo null sets that intertwines the shifts in the
  source's stated direction and has the required inverse properties.
- The source's precise classification direction: equal entropy implies isomorphism, or a full
  equivalence only when the converse entropy-invariance theorem is separately mapped and checked.

These bullets delimit the intended family. They do not select or assert a canonical proposition.

## Decisions required at statement freeze

1. Whether alphabets are finite, countable with finite entropy, or in a more general standard
   probability-space class; whether zero-mass symbols are retained or removed.
2. Whether paths are indexed by `Int` or `Nat`. A two-sided invertible automorphism must not be
   replaced by a one-sided noninvertible endomorphism.
3. Whether entropy means the base distribution's Shannon entropy, the shift's
   Kolmogorov-Sinai entropy, or a checked equality transporting between them; also the logarithm
   base, `0 log 0` convention, and finite/infinite codomain.
4. Whether the theorem is the sufficient equal-entropy direction or an iff classification. The
   converse needs an explicit entropy-invariance result rather than being folded into the name.
5. The exact measure-space category: standard/Lebesgue probability spaces, completed sigma
   algebras, maps defined everywhere or only off null sets, and how an almost-everywhere inverse is
   represented.
6. The intertwining equation and orientation of the shift, including whether it is required
   pointwise, almost everywhere, or in the quotient category of measure-preserving systems.
7. Boundary cases: singleton or empty alphabets, zero entropy, countably many zero weights,
   infinite entropy, non-full support, and null-set changes to the coding map.

## Explicit exclusions

- Entropy invariance under an already-given isomorphism as a substitute for constructing the
  Ornstein isomorphism.
- Topological conjugacy of full shifts, symbolic-dynamics coding, orbit equivalence, weak
  isomorphism, factor equivalence, or equality in distribution in place of measure conjugacy.
- A one-sided Bernoulli endomorphism silently substituted for a source theorem about invertible
  two-sided shifts.
- The binary entropy function alone, or equality of scalar entropy values, as a proof that the
  corresponding dynamical systems are isomorphic.
- A structure that assumes the requested isomorphism or conjugacy as an input and then returns it.
- The separate physics-corpus target `THM-P-0889` as authority for silently sharpening this
  mathematics target's literal source slogan.
- The repository label `已验证`, a paper title, or an API availability probe as human-source or
  kernel-proof evidence.

No canonical Lean target is frozen at intake because the repository record and uninspected
bibliographic candidate do not resolve these proposition-changing choices.

