# Scope map

## Preserved source scope

- Method/family: iteration associated with Jürgen Moser, dated 1960 by the repository inventory.
- Objects: weak solutions of an unspecified differential equation.
- Consequence: local boundedness, with no norm, region, or constant stated.
- Domain: the repository categorizes the entry as differential equations / PDE.

This is all the mathematical scope supported by the available record. In particular, "Moser
iteration" is a technique used in multiple inequivalent elliptic and parabolic results and is not
itself a uniquely quantified proposition.

## Decisions required before statement freeze

The statement phase must identify a primary theorem and freeze: elliptic/parabolic operator and
divergence form; dimension and domain; scalar/vector codomain; weak solution or subsolution
definition; coefficient ellipticity, boundedness and measurability; forcing terms; sign and boundary
conditions; Sobolev and integrability exponents; nested balls or cylinders; the exact supremum/norm
estimate; constant dependencies; and endpoint or degenerate cases.

## Explicit exclusions

- Choosing harmonic functions, a mean-value inequality, or a maximum principle merely because Lean
  APIs exist for them.
- Replacing weak-solution local boundedness by an abstract sequence iteration lemma.
- Treating a Sobolev embedding alone as the claimed PDE theorem.
- Treating the metadata label `已验证` or general knowledge of Moser's method as proof evidence.
- Claiming either an elliptic or parabolic formulation before a primary source fixes that choice.
