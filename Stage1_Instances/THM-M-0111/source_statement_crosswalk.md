# Source-statement crosswalk

## Primary source identified

K. Kodaira, "On Kahler varieties of restricted type (an intrinsic
characterization of algebraic varieties)," *Annals of Mathematics*, Second
Series 60 (1954), no. 1, pp. 28-48. DOI: `10.2307/1969701`.

This bibliographic identification does not establish `H0`. The exact numbered
theorem/page, edition scan, terminology, normalization, assumptions, and errata
remain mandatory work for the anchor/source audit. Until then the full article
page range is recorded rather than inventing a theorem locator.

## Crosswalk

| Source-side concept | Frozen target meaning | Lean status at intake |
|---|---|---|
| Kahler variety/manifold of restricted (Hodge) type | compact complex manifold carrying a Kahler form with integral cohomology class | native API unresolved |
| integral fundamental two-form/class | class lies in the image of integral cohomology in real/de Rham cohomology, subject to normalization audit | comparison API unresolved |
| imbedding in projective space | holomorphic embedding into finite-dimensional complex projective space | projective-space and embedding APIs unresolved |
| projective algebraic conclusion | not substituted for the embedding conclusion without a checked Chow/comparison transport | explicitly excluded from canonical target |

## Legacy crosswalk

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_024.lean` defines
`StatementShape`, but its manifold hypotheses and embedding properties are
uninterpreted propositions. Thus it preserves a rough quantifier skeleton only.
Its checked wrappers do not close Kodaira embedding and receive no rev-5.6
proof or statement credit.

## Fidelity risks

The words "Hodge manifold," "restricted type," and "integral Kahler class"
can hide a `2*pi` normalization. Older sources may assume connectedness or use
"variety" for a complex analytic manifold. These are open source-audit items,
not permissions to select the easiest formal variant.
