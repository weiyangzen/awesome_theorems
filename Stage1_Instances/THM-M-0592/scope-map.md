# Scope map

## Available claim boundary

The repository supplies only the name "Connes cyclic cohomology" and the gloss "cohomology of
noncommutative geometry." Cyclic cohomology is a mathematical theory/invariant, not a proposition
with determined binders, hypotheses, and conclusion. This intake therefore freezes the ambiguity
rather than silently choosing an easy fact about a cochain complex.

The plausible subject is algebraic cyclic cohomology of an associative algebra as introduced by
Connes. The following are distinct candidate roots:

- construction of a cochain complex whose cohomology is cyclic cohomology;
- equivalence between cyclic-cochain and bicomplex/mixed-complex presentations;
- Connes's SBI periodicity exact sequence relating Hochschild and cyclic (co)homology;
- Morita invariance or matrix stability;
- the pairing of cyclic cocycles with algebraic or topological K-theory.

No candidate is canonical merely because it is formalizable. The statement phase must select one
exact source proposition and, if necessary, record a target-correction decision.

## Required domain decisions

The selected proposition must freeze the coefficient ring or field, associative algebra and
unitality assumptions, algebraic versus continuous/topological cochains, normalized versus
unnormalized complexes, grading and sign conventions, and all finiteness/completeness hypotheses.
It must also decide the treatment of nonunital algebras, degree zero, periodic cyclic cohomology,
zero objects, and positive-characteristic coefficients.

On the Lean side, it must name concrete cochain objects, differentials with a checked square-zero
law, (co)homology construction, exactness or pairing interfaces as applicable, ordered binders,
universes, imports, foundation profile, and checked transports for alternate encodings.

## Explicit exclusions

- A definition of cyclic cohomology presented as though it were a theorem.
- The tautology that the cohomology of an assumed complex exists.
- Hochschild cohomology, group cohomology, de Rham cohomology, or ordinary singular cohomology as a
  substitute.
- A finite-dimensional or commutative special case unless the corrected target explicitly selects
  it and records the scope change.
- Combining the SBI sequence, Morita invariance, and K-theory pairing into one unsupported slogan.
- The separate manifest target `THM-M-0337`, despite its near-duplicate Chinese name; target IDs and
  proof credit remain independent unless the master performs an explicit deduplication migration.
- The repository `已验证` label as source, Lean, or theorem-completion evidence.

## Intake classification

The root vector is `[H5, M4, R4]`. `H5` records that the current wording is not a stable proposition,
not that cyclic cohomology is refuted. `M4` records no canonical Lean target or proof body. `R4`
records that no source-anchored proof reconstruction exists. A corrected target can receive a new
vector only after exact source and statement review.
