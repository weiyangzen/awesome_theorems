# Scope map

## Preserved theorem family

This intake preserves exactly the family named by the catalog: Brauer characters in modular
representation theory. In the standard finite-group setting, such characters depend on a prime
and modular coefficient data and are evaluated on the prime-regular part of a finite group. Those
facts orient source discovery; they are not silently promoted into a canonical proposition.

The catalog's phrase "properties of characters" does not say which property is the theorem. A
statement phase cannot choose a familiar result merely because it is true or bears Brauer's name.

## Decisions required at statement freeze

1. Preserve and independently review an authoritative source edition, exact theorem/page,
   incorporated definitions, proof boundary, translation, corrections, and errata.
2. Identify the theorem identity: construction/well-definedness of Brauer characters, a relation
   with ordinary characters, irreducibility or completeness, a decomposition-number theorem, a
   block theorem, a lifting theorem, or another explicitly sourced proposition.
3. Reconcile the catalog's `1956` date with the discovered 1941 modular-character papers and any
   later source that actually supplies the selected result.
4. Fix the acting finite group and its finiteness encoding, the prime, the prime-regular subset,
   and the convention for prime-regular elements.
5. Fix the modular system or coefficient data: characteristic-zero fraction field, valuation ring,
   residue field of characteristic `p`, splitting and algebraic-closure assumptions, embeddings,
   and root-of-unity lifts.
6. Fix whether the inputs are modules, matrix representations, ordinary characters, Brauer
   characters, simple modules, or Grothendieck-group classes, with all finite-dimensionality and
   equivalence conventions.
7. Fix the codomain and equality convention for character values, ordered binders, universes,
   hypotheses, conclusion, foundation/TCB/computation profiles, and checked alternate encodings.

## Boundary cases

Source and statement review must explicitly dispose of the trivial group, a prime not dividing the
group order, characteristic zero versus characteristic `p`, the identity and other prime-regular
elements, non-prime-regular elements where a Brauer character may be outside its domain, zero and
reducible modules, nonsplitting coefficient fields, equivalent but not definitionally equal
representations, empty/simple-module indexing choices, and all degenerate conclusions. No case is
excluded at intake.

## Explicit substitutions excluded

- Ordinary complex representation characters are adjacent infrastructure, not Brauer characters.
- Mathlib's `MeasureTheory.Measure.modularCharacter` is a Haar-measure scaling homomorphism for
  locally compact groups; the shared word "modular" does not make it modular representation theory.
- Brauer induction and Brauer's theorem on Artin L-functions concern ordinary or virtual
  characters and analytic continuation, not this unspecified modular-character root.
- The Brauer group of central simple algebras, Brauer-Siegel results, the Brauer fixed-point
  theorem, Brauer-Witt, and Cartan-Brauer-Hua are different targets.
- Maschke's theorem, Schur's lemma, character orthogonality, and block theory may become
  dependencies or neighbors only after an exact source theorem is selected.
- A theorem about one special group, one prime, one coefficient field, or one precomputed character
  table cannot replace an unstated general result.
- A structure, hypothesis, certificate, or table storing the desired property is circular.
- The catalog's `已验证` label, a name match, a source URL, or this intake probe supplies no source
  or proof credit.

## Formal boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, bounded searches found
ordinary representation-character APIs in `Mathlib.RepresentationTheory.Character`, but no
finite-group Brauer-character definition or theorem and no prime-regular modular-representation
surface. The only matching `ModularCharacter` module is the explicitly unrelated Haar-measure API.
The canonical Lean module, expression, and fingerprint remain null. Exact-source selection,
exhaustive anchor discovery, provenance/trust audit, and proof credit all belong downstream.
