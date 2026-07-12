# Source-statement crosswalk

## Repository record

The authoritative inventory supplies the Chinese title "Thom isomorphism", Rene Thom's name, the
year 1954, and only the gloss "the Thom isomorphism for vector bundles". Its fields for precise
definitions, prerequisites, proof history, dependencies, axioms, and existing formal artifacts are
all unfilled. Its `已验证` label is explicitly untrusted by rev-5.6 and supplies no statement or
proof credit.

## Candidate mathematical sources

- Rene Thom, *Quelques proprietes globales des varietes differentiables*, **Commentarii
  Mathematici Helvetici** 28 (1954), 17-86. This is the historical primary-source candidate. The
  exact result, page, notation, hypotheses, and relationship to the modern vector-bundle theorem
  have not yet been inspected and approved.
- John W. Milnor and James D. Stasheff, *Characteristic Classes*, Annals of Mathematics Studies 76,
  Princeton University Press (1974), the chapter on oriented vector bundles and the Thom
  isomorphism. This is a stable modern source candidate, but the exact edition locator,
  coefficient conventions, assumptions, and errata remain to be checked.
- Allen Hatcher, *Vector Bundles and K-Theory*, the characteristic-classes chapter and its Thom
  isomorphism proposition. This is a useful modern comparison source, not a replacement for
  primary-source review or independent acceptance.

These entries are discovery anchors only. They justify `H1`, not `H0`: no immutable edition has
yet received an exact theorem/page/assumption/errata crosswalk and independent review.

## Crosswalk

| Repository/source phrase | Mathematical component to freeze | Required Lean component | Intake status |
|---|---|---|---|
| "vector bundle" | category, rank, base, and regularity hypotheses | concrete bundle and base-space structures | family identified; exact domain open |
| orientation | coefficient-dependent fibre generators or local system | orientation datum/predicate and coefficient ring | included; convention open |
| Thom class | relative or compact-support class restricting fibrewise to a generator | explicit cohomology class and restriction property | included; theory/API open |
| cup product | pull back a base class and multiply by the Thom class | pullback, graded product, degree shift | intended map identified |
| "isomorphism" | bijective graded map in every degree | bundled graded/module equivalence or pointwise bijectivity | conclusion identified; encoding open |
| Thom space | quotient of disk bundle by sphere bundle | quotient plus reduced/relative cohomology transport | equivalent form only; transport required |
| 1954 / Rene Thom | historical attribution | no machine-proof credit | exact primary locator open |

## Human and machine boundary

A repository-wide name search at intake found no target-owned Lean artifact and only the metadata
and scheduling records for this theorem. This is not the later exhaustive pinned-mathlib/external
anchor audit. The statement phase must first select the exact mathematical variant; the anchor
phase must then record candidate declarations, exact types, revisions, dependencies, placeholders,
axioms, and terminal proof-body provenance.

Before `H0`, an independent reviewer must approve the selected immutable edition, exact theorem
and page, definitions, all assumptions, coefficient and support conventions, proof boundary, and
errata. Before statement credit, every approved row must map to an elaborated Lean expression, with
checked transports for relative-cohomology and Thom-space encodings.
