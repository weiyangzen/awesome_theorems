# Scope map

## Preserved theorem family

The intake preserves the theorem family actually indicated by the catalog: Ngo Bao Chau's proof of
the Langlands-Shelstad Fundamental Lemma for Lie algebras. It does not interpret the entry as a
general Langlands correspondence, the group version of the Fundamental Lemma, or an arbitrary
result bearing the words "fundamental lemma."

The strongest inspected source lead is arXiv `0801.0446v3`, *Le lemme fondamental pour les
algebres de Lie*. Its introductory Theorem 1 concerns a complete discrete valuation ring `O` with
finite residue field `k` of cardinality `q`, fraction field `F`, a reductive group scheme `G/O`
whose Weyl-group order is not divisible by `char(k)`, endoscopic data and associated group `H`, and
matching stable regular semisimple classes. It asserts an equality between the normalized
kappa-orbital integral of the characteristic function of `g(O)` and the corresponding stable
endoscopic orbital integral. The detailed source form is Theorem 1.11.1.

This paragraph is a source-family map, not the frozen canonical proposition.

## Decisions required at statement freeze

An accepted statement review must decide all of the following:

1. Whether the root is introductory Theorem 1, detailed local Theorem 1.11.1, or a checked
   equivalence between those formulations.
2. Every incorporated source definition: the quasi-split reductive group scheme, pointed
   endoscopic datum, Chevalley bases, regular-semisimple loci, matching map, regular centralizers,
   kappa-orbital integrals, stable orbital integrals, discriminants, and measure transport.
3. The exact local-field regime. Ngo's article proves the equal-characteristic case; its sentence
   about unequal characteristic depends on Waldspurger and must be modeled as a separate source and
   transport obligation rather than silently attributed to Ngo's local proof.
4. The characteristic restriction that `char(k)` not divide the Weyl-group order, together with
   any additional restrictions imported by the detailed definitions and transfer theorem.
5. Whether the conclusion uses the introductory discriminant-normalized equation or the detailed
   `q^r` equation, and the checked bridge between their Haar-measure and transfer-factor
   conventions.
6. The exact ordered binders, universes, typeclasses, hypotheses, conclusion, foundation profile,
   and any alternate Lean encoding with a checked transport.
7. Whether `THM-M-0099` and the metadata-duplicate `THM-M-0434` are intentionally separate roots,
   aliases requiring deduplication, or a catalog collision requiring correction.

These choices affect source ownership, the proposition, or its proof boundary. Intake does not
choose them without master and independent source review.

## Boundary cases

Source review must explicitly preserve or resolve: equal versus unequal characteristic; residue
characteristic dividing the Weyl-group order; ramified versus unramified data; regular semisimple
versus singular elements; matching versus nonmatching stable classes; normalization and choice of
Haar measures; characteristic functions of integral Lie algebras versus arbitrary test functions;
split versus merely quasi-split groups; trivial or degenerate endoscopic data; and the relation
between the Lie-algebra and group formulations.

No case is excluded or generalized before the canonical proposition is selected.

## Excluded substitutions

- The group Fundamental Lemma is related through additional reductions; it is not identical to
  the source's Lie-algebra statement.
- The nonstandard, weighted, twisted, stable-base-change, or special-group Fundamental Lemmas do
  not replace the ordinary Lie-algebra root.
- A theorem for one low-rank group, an unramified torus, or another special case cannot replace the
  general source-scoped result.
- Arbitrary test functions cannot replace the characteristic functions of the specified integral
  Lie algebras without a separately sourced theorem.
- The unequal-characteristic conclusion cannot be credited solely to Ngo's equal-characteristic
  proof; the Waldspurger transfer boundary must be explicit.
- A structure containing the desired integral identity as a field, or an implication assuming the
  identity, supplies no proof.
- Nearby mathlib APIs, the legacy `S1_M_083.lean` surrogate, a theorem name, `#check`, or the
  catalog's untrusted verified label supplies no H or M credit.

## Neighbor ownership

`THM-M-0098` has a conflicting title/gloss record and does not determine this target. `THM-M-0434`
has essentially duplicate metadata and a separate owned dossier. Its source selection, legacy
files, receipts, and state are discovery inputs only and cannot be copied. Duplicate resolution
must preserve both target IDs until the master records a catalog decision; coverage must not count
the same terminal theorem body twice.

## Formal boundary

No canonical Lean expression is frozen. At pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, the probe checks local-field, scheme, and Haar-measure
interfaces. A bounded exact-topic search found only unrelated uses of "fundamental lemma" and no
endoscopy, transfer-factor, stable-conjugacy, or orbital-integral target. This is scoped intake
evidence, not an exhaustive external anchor audit or proof of global absence.
