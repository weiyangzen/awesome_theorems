# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` identifies Edgar Brown, 1962, and states only
`广义上同调论的可表性` ("representability of generalized cohomology theories").
`Docs/Stage0_Blueprint.md` repeats that phrase. This fixes the topic but not a unique proposition;
its `已验证` metadata is explicitly untrusted under rev-5.6.

## Primary-source discovery anchors

- Edgar H. Brown, Jr., "Cohomology Theories," *Annals of Mathematics*, second series, volume 75,
  issue 3 (May 1962), beginning at page 467, DOI `10.2307/1970209`.
- Edgar H. Brown, Jr., "Correction to Cohomology Theories," *Annals of Mathematics*, second
  series, volume 78, issue 1 (July 1963), page 201, DOI `10.2307/1970510`.

The bibliographic fields above were checked against Crossref on 2026-07-12. They are discovery
anchors, not `H0`: the full article page range, exact theorem number/page, definitions, assumptions,
proof dependencies, stable document hashes, and effect of the correction remain unverified.

## Claim crosswalk

| Claim component | Intended source component | Required Lean component | Intake assessment |
|---|---|---|---|
| generalized cohomology theory | reduced graded functors with suspension/exactness structure, subject to the source's conventions | a concrete bundled theory or an explicitly quantified family of functors | included; exact bundle open |
| homotopy domain | pointed CW complexes or the exact homotopy category used by Brown | concrete category, morphism quotient, universes, and CW predicate | included; source boundary open |
| wedge axiom | wedges are carried contravariantly to products in the source-specified sense | indexed coproduct comparison and bijectivity/isomorphism | included; cardinality open |
| excision/Mayer-Vietoris | exactness or weak-pushout condition controlling cell attachment | exact formal diagram and exactness predicate | included; formulation open |
| representing space | an object `Y` and natural bijections with pointed homotopy classes into `Y` | existence of `Y` plus a natural equivalence to a representable functor | intended conclusion |
| degreewise representation | one representing object for each cohomological degree | indexed family `E n` and degreewise natural equivalences | repository-facing candidate |
| Omega-spectrum compatibility | suspension isomorphisms relate successive representing spaces | structure maps and checked equivalences | possible strengthening; not credited |

## Existing Lean boundary

The pinned mathlib search performed for intake found general categorical representability APIs but
no declaration named for Brown representability. The repository file
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_139.lean` explicitly says its universal-element
criterion and adjoint-functor bridges do **not** prove Brown representability. Those artifacts are
useful interface discovery only and receive no statement or proof credit for this target.

Before `H0`, an independent reviewer must inspect a stable copy of the article and correction,
pinpoint the exact selected result and all imported definitions, map every premise and conclusion,
record corrections or later errata, and approve the source-to-Lean crosswalk.
