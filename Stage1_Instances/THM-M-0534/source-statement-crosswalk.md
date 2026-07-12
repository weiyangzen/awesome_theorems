# Source-statement crosswalk

## Repository record

The repository inventory supplies the Chinese title "long exact sequence", the date "20th
century", the attribution "many mathematicians", and the gloss "a short exact sequence induces a
long exact sequence in homology". It supplies no edition, theorem number, coefficients, object
category, indexing convention, topological pair, or naturality clause. Its `verified` label is
untrusted under rev-5.6.

## Source candidates

- Charles A. Weibel, *An Introduction to Homological Algebra*, Cambridge Studies in Advanced
  Mathematics 38 (1994), section 1.3 on long exact sequences. This is a stable modern source
  candidate for the chain-complex theorem; exact theorem/page, wording, assumptions, and errata have
  not been independently inspected here.
- Allen Hatcher, *Algebraic Topology* (2002), the singular-homology chapter's long exact sequence of
  a pair. This is a candidate for the specifically topological specialization; exact proposition,
  page, coefficient convention, corrections, and its relation to the inventory wording remain open.
- The Stacks Project, tag `0111`, cited by pinned mathlib's
  `Mathlib.Algebra.Homology.HomologySequence` module. It is a useful living-source and proof-genealogy
  lead, but an immutable revision and node-by-node review have not been recorded.

These are discovery anchors, not `H0` evidence. An accountable review must select the intended root
and inspect an immutable edition before source fidelity can be accepted.

## Crosswalk

| Repository/source phrase | Mathematical component to freeze | Required Lean component | Intake status |
|---|---|---|---|
| "short exact sequence" | complexes, or the chain sequence attached to a pair/triple | `ShortComplex` of `HomologicalComplex` plus `ShortExact`, or checked topological construction | family included; domain open |
| "homology" | coefficients, target abelian category, reduced/relative convention | homology objects and induced `homologyMap`s | pinned general API elaborates; specialization open |
| "induces" | construction and naturality of the boundary map | `ShortComplex.ShortExact.delta` and any required naturality theorem | candidate API only |
| "long sequence" | all degrees and the shift direction | adjacent indices with a quantified family of exact local windows | indexing and whole-sequence encoding open |
| "exact" | image/kernel equality at every term | exact `ShortComplex` or `ComposableArrows` windows | candidate API elaborates; canonical target open |
| algebraic topology category | singular chains of spaces/pairs if intended | singular chain functor, quotient/relative complex, comparison maps | source decision and API crosswalk open |

## Existing Lean boundary

The pinned intake probe elaborates the general mathlib declarations
`ShortComplex.ShortExact.delta`, `ShortComplex.ShortExact.homology_exact1/2/3`,
`HomologicalComplex.HomologySequence.composableArrows5_exact`, and
`HomologicalComplex.HomologySequence.delta_naturality` (Lean surface names use the Unicode delta and
subscripted numerals shown in `IntakeProbe.lean`). This establishes only that relevant general
interfaces exist in the pinned environment. It does not select the source proposition, establish a
singular-homology pair/triple bridge, audit terminal bodies or axioms, or transfer proof credit from
the separately scheduled `THM-M-0001`.

Before `H0`, an independent reviewer must approve the exact source locator, definitions,
assumptions, signs, coefficients, boundary cases, proof boundaries, and errata. Before statement
credit, every approved row must map to one elaborated canonical Lean expression, with checked
transports for alternate encodings.
