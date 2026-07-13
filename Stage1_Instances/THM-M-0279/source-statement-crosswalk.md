# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:2006-2011` records the Chinese title `赫尔德不等式`, Otto
Holder, the year 1889, the gloss `L^p空间的乘积积分`, high importance, and status `已验证`.
Git history places all six uncited lines in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record supplies no formula, domain,
exponent range, assumptions, definition chain, theorem/page, proof passage, correction record,
reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:7711-7736` repeats the gloss while explicitly leaving the target system,
logical foundation, exact definitions and premises, proof route, dependencies, equivalent forms,
axioms, and machine artifact links open. The rev-5.6 manifest preserves the verified value only as
untrusted metadata and resets the theorem to `L0 / rework_required`.

## Human-source leads, not admitted

The version-addressed 2012 revision 28956 of the *Encyclopedia of Mathematics* entry "Holder
inequality" is a secondary bibliographic lead. It cites O. Holder, "Ueber einen Mittelwerthsatz",
*Nachrichten der Gesellschaft der Wissenschaften zu Gottingen* (1889), pages 38-47. The same entry
separately presents sum, integral, endpoint, multi-function, and generalized variants, confirming
that the theorem name alone does not select one proposition.

The institutional Gottingen scan was inspected under article identifier `GDZPPN00252421X`, volume
identifier `PPN252457072_1889`, printed pages 38-47 (IIIF images `00000044`-`00000053`). The scan's
title is "Ueber einen Mittelwerthssatz"; the METS catalog has the typo
"Ueber einen Mittelwerthabsatz". The article develops weighted finite Jensen/mean inequalities,
power-sum inequalities related to Rogers, weighted arithmetic-geometric means, and a positive-
series application. It does not state the modern measure-integral formula
`integral |f*g| <= normLp f * normLq g`. Holder also credits L. J. Rogers, so the catalog's simple
attribution needs historical review.

These leads are not H0 evidence for the catalog root. The historical scan is a primary attribution
and ancestor source, not a verbatim source for the modern integral claim. A modern exact proposition
or a reviewed derivation and equivalence chain, historical definitions, premise/conclusion/proof
mapping, translations, corrections or errata, and independent review remain open. The classical
published family plus these concrete unresolved leads supports only provisional `H1`.

## Literal component crosswalk

| Catalog component | Plausible readings | Pinned Lean surfaces | Intake result |
|---|---|---|---|
| `L^p空间` (`L^p` spaces) | raw measurable functions with finite `p`-norm; AE classes; seminorm notation | `AEMeasurable`, `AEStronglyMeasurable`, `MemLp`, `Lp`, `eLpNorm` | carrier and encoding open |
| `乘积` (product) | `f * g`, `abs (f * g)`, `norm f * norm g`, conjugate pairing, bilinear operation | pointwise `(f * g)`, norm product, abstract `b f g` | operation and scalar conventions open |
| `积分` (integral) | nonnegative extended integral, absolute integral, signed/Bochner integral, restricted integral | `lintegral`, `integral`, `eLpNorm` | integration convention open |
| implicit exponents | finite real `p,q > 1`; endpoint `1,infinity`; extended Holder triple | `Real.HolderConjugate`, `ENNReal.HolderConjugate`, `ENNReal.HolderTriple` | exponent and endpoint policy open |
| implicit hypotheses | measurability; strong measurability; `MemLp`; nonnegativity; measure assumptions | theorem-specific contexts below | ordered assumptions open |
| `已验证` | untrusted inventory label | accepted source and kernel receipts | no credit |

One conventional two-function prose candidate is:

```text
For conjugate exponents p and q, the integral of the pointwise magnitude (or product of norms) of
f and g is at most the Lp norm of f times the Lq norm of g.
```

This is only a family description. Parenthetical alternatives expose unresolved choices; it is not
a canonical statement or quotation.

## Pinned Lean candidate crosswalk

All rows below refer to pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. `IntakeProbe.lean` elaborates the displayed
interfaces and prints axiom reports for the five theorem candidates.

| Declaration | Exact-topic role | Statement-identity boundary |
|---|---|---|
| `ENNReal.lintegral_mul_le_Lp_mul_Lq` | arbitrary measure, `ENNReal` functions, real finite conjugates, AE measurability, explicit powered `lintegral` bound | close literal product-integral candidate; codomain and finite-exponent choices are not source-approved |
| `NNReal.lintegral_mul_le_Lp_mul_Lq` | analogous `NNReal` function inequality | changes carrier and coercion behavior; not automatically equivalent to the catalog root |
| `MeasureTheory.integral_mul_norm_le_Lp_mul_Lq` | normed-group functions with `MemLp`; bounds the Bochner integral of norm products | conventional normed variant, but value carrier, integrability, and integral choices remain open |
| `MeasureTheory.integral_mul_le_Lp_mul_Lq_of_nonneg` | nonnegative real functions with `MemLp`; bounds the signed product integral | requires nonnegativity and is not the usual absolute-value statement for arbitrary real functions |
| `MeasureTheory.eLpNorm_le_eLpNorm_mul_eLpNorm_of_nnnorm` | generalized bilinear `eLpNorm` inequality with an extended Holder triple | broader operation/exponent theorem; requires source-approved specialization before root use |
| `MeasureTheory.MemLp.mul` | closure of pointwise products in the expected extended exponent | useful consequence/interface, not the numerical product-integral inequality itself |

`Real.HolderConjugate p q` entails strict interior finite exponents. The extended
`ENNReal.HolderConjugate` regime includes the `(1, infinity)` endpoint. Therefore choosing a direct
finite-real theorem rather than an extended-exponent specialization changes the boundary behavior,
not merely notation.

Passing the probe authenticates only these candidate APIs in this pinned environment. It does not
establish a normalized source match, minimal imports for an absent target, checked transports,
terminal proof-body provenance, accepted transitive trust, or root proof credit.

## Neighbor-target boundary

`Docs/researches/math_theorems.md:2232-2237` contains another Holder record whose gloss is
`L^p空间的对偶性`; rev-5.6 assigns it `THM-M-0310`. Its existing fail-closed intake correctly
distinguishes boundedness of the product pairing from the stronger claim that continuous
functionals are represented by `L^q` elements. No statement, source, obligation, proof body, debt,
or receipt is shared between the two targets.

## Open gates

Before H0, an accountable reviewer must accept an exact modern source proposition or a complete
reviewed derivation from the scanned historical inequalities, transcribe all incorporated
definitions, map every premise, transition, and conclusion, resolve historical notation and the
Rogers priority boundary, audit translations and errata, and obtain independent approval. Before
statement acceptance, Lean work must freeze the exact domains, binders,
hypotheses, conclusion, minimal imports, expression and environment fingerprints, checked alternate
encodings, and required hypothesis, domain, binder-scope, and boundary mutations. Candidate,
proof-body, dependency, placeholder, axiom, provenance, and trust closure remain later-phase work.
