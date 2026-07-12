# Scope map

## Metadata boundary

The repository supplies only the name `Ω-谱表示`, the attribution "many mathematicians", the
period "20th century", and the gloss "an Omega-spectrum for a generalized cohomology theory".
Those fields do not state a proposition. In particular, they do not decide which category supports
the theory, whether it is reduced, which exactness and wedge axioms it satisfies, or the strength
and direction of the claimed representation.

## Candidate intended subject

The standard subject is the passage from a suitably axiomatized generalized cohomology theory to a
sequence of representing pointed spaces `E_n` with natural representations of its graded functors
and compatible weak equivalences `E_n -> Omega E_(n+1)`. A source-selected statement must freeze:

- the input category, commonly pointed CW complexes or a homotopy category, and its size conditions;
- a reduced or unreduced, integer-graded cohomology theory and its precise axioms;
- whether representability is asserted for every degree and whether representing objects are based;
- the direction and status of the adjoint structure maps, and whether "Omega-spectrum" means
  equality, homotopy equivalence, weak equivalence, or fibrant-spectrum structure;
- the natural isomorphism between cohomology classes and homotopy classes into `E_n`, including
  grading and suspension conventions;
- whether uniqueness, multiplicative structure, or the converse construction is part of the root.

The statement phase must also decide boundary cases such as the zero theory, negative degrees,
nonconnected spaces, reduced degree zero, and theories defined only on finite CW complexes.

## Explicit exclusions

- Representability of only one functor or degree as a substitute for a compatible Omega-spectrum.
- Assuming representing spaces or loop equivalences as structure fields and returning them.
- The suspension-spectrum construction for a single space, Eilenberg-Mac Lane spectra alone, or
  the stable homotopy category equivalence as a silently broadened replacement.
- A spectrum in functional analysis or linear algebra.
- Treating the metadata `已验证`, Brown representability by name, or an unpinned external project as
  proof credit.

The later statement artifact must freeze ordered binders, universes, hypotheses, conclusion,
foundation/TCB/computation profiles, a canonical Lean expression and imports, checked transports,
environment fingerprint, and domain/hypothesis/boundary mutation tests.
