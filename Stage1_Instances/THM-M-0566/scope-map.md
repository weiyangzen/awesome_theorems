# Scope map

## Literal repository scope

The only theorem-specific source text is the Chinese label `庞特里亚金示性类`, the attribution
to Lev Pontryagin, the year 1942, and the gloss `实向量丛的整系数示性类` (integral
characteristic classes of real vector bundles). This identifies mathematical subject matter but is
not a theorem: a characteristic class is an assignment/construction, and several distinct
propositions express its defining properties.

## Candidate claim family

A conventional modern construction assigns to a real vector bundle `E` classes
`p_i(E) in H^(4i)(X; Z)` via even Chern classes of its complexification, commonly normalized as
`p_i(E) = (-1)^i c_(2i)(E tensor C)`. A source-located statement may instead target pullback
naturality, the Whitney product formula for total Pontryagin class, stability, vanishing by rank,
or comparison with classifying-space universal classes. These are separate targets until the
statement phase selects one.

## Decisions required before a formal target

- Choose topological, smooth, or numerable real vector bundles and the hypotheses on the base `X`.
- Fix ordinary integral cohomology, grading/index conventions, complexification, and the sign
  normalization; state whether torsion-sensitive equality or rationalized equality is intended.
- Choose exactly one conclusion and ordered binders, including rank restrictions and the range of
  `i`.
- Specify the zero bundle, trivial bundle, empty base, `i = 0`, pullbacks, direct sums, and degrees
  above the bundle rank.
- Inspect a stable source edition and map every premise and conclusion before creating Lean syntax.

## Explicit exclusions

- Pontryagin duality, the Pontryagin square/operation, Pontryagin product, Pontryagin-Thom theory,
  and the maximum principle.
- Chern classes or Stiefel-Whitney classes presented as substitutes for the real-bundle class.
- A record or hypothesis that contains the desired characteristic class/property as data.
- A rational Chern-Weil differential-form representative substituted for the requested integral
  class without a checked comparison theorem.
- Any one standard property chosen merely because it is easier to encode in the current library.

The later statement must use concrete bundle, complexification, and integral cohomology interfaces,
or record the precise missing API as a statement blocker.
