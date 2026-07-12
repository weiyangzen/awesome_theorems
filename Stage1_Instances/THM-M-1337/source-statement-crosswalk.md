# Source-statement crosswalk

## Repository source record

`Docs/researches/math_theorems.md:9754-9759`, originating at repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`, records only the title, Thomas Gronwall, 1919, the
gloss `微分不等式的积分形式`, importance "high," and status `已验证`.
`Docs/Stage0_Blueprint.md:36372-36397` repeats that gloss while explicitly leaving exact definitions
and premises, proof route, equivalent forms, axioms, and machine artifacts unresolved. The manifest
carries `已验证` only as `source_status_untrusted`, so none of these fields establish `H0` or an
exact proposition.

## Historical discovery candidate

Crossref metadata corroborates this plausible original source:

T. H. Gronwall, "Note on the Derivatives with Respect to a Parameter of the Solutions of a System
of Differential Equations," *The Annals of Mathematics* 20(4) (July 1919), starting at page 292,
DOI `10.2307/1967124`.

The article text was not obtained or inspected during intake. Crossref supplies bibliography, not
the theorem passage. The page range, exact numbered result, notation, assumptions, proof, relation
to the later Gronwall-Bellman integral formulation, corrections, and independent review remain
open. This is discovery evidence consistent with `H1`, not a primary-source receipt or H0
crosswalk.

## Component crosswalk

| Repository phrase | Mathematical component to freeze | Required Lean surface | Intake disposition |
|---|---|---|---|
| "differential inequality" | scalar, norm, integral, derivative, Dini, or liminf-slope premise | exact function types and premise predicate | family identified; exact premise open |
| "integral form" | integrand, coefficient, measure, bounds, orientation, and pointwise/a.e. semantics | concrete interval integral and regularity hypotheses | no formula supplied |
| initial term | constant `A`, value `u(a)`, or nondecreasing inhomogeneous function | ordered binder plus sign/regularity assumptions | absent from repository source |
| coefficient | constant `K` or function `b(t)` | scalar/function binder, sign and integrability | absent from repository source |
| exponential conclusion | constant-coefficient or integral-exponential bound | exact inequality and every side condition | absent from repository source |
| Thomas Gronwall / 1919 | historical provenance | source record only | metadata corroborated; theorem passage uninspected |

## Pinned Lean discovery candidates

At manifest-pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.Analysis.ODE.Gronwall` contains:

```text
gronwallBound
le_gronwallBound_of_liminf_deriv_right_le
norm_le_gronwallBound_of_norm_deriv_right_le
```

The first theorem uses a scalar continuous function, an abstract right-slope/liminf witness, a
constant coefficient and additive forcing. The second uses a normed real vector space and right
derivatives. Both conclude a `gronwallBound` estimate. The module cites Hubbard and West,
*Differential Equations: A Dynamical Systems Approach*, section 4.5, where the norm theorem is
called "Fundamental Inequality." It also records a TODO for a variable-coefficient derivative
version after suitable fundamental-theorem-of-calculus infrastructure.

`IntakeProbe.lean` checks those names and their types in the pinned environment. This is real `M3`
interface evidence but not an exact-statement match, an anchor/provenance audit, or `M0-W`. A
pinned-package text search found no integral-form Gronwall declaration. Later work must not infer
absence beyond the recorded bounded search or replace a source-selected integral theorem with these
nearby differential statements.

## Required follow-up

Before statement acceptance, an accountable source reviewer must preserve and hash a lawful
primary-source copy, pinpoint and transcribe the exact result and dependent definitions, settle its
genealogy and any translation or errata, map every binder, premise, conclusion, and boundary case,
and obtain independent approval. The statement phase must then choose the matching Lean domain,
elaborate and fingerprint the exact proposition, provide checked transports for every credited
alternate form, and run all required mutations. Until then there is no canonical statement or
proof credit.
