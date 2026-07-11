# Source-statement crosswalk

## Candidate primary sources

- Olga A. Ladyzhenskaya, Vsevolod A. Solonnikov, and Nina N. Ural'tseva, *Linear and
  Quasilinear Equations of Parabolic Type*, AMS Translations of Mathematical Monographs 23 (1968),
  the chapters on linear parabolic equations and Holder estimates. Exact theorem/page, translation
  conventions, hypotheses, and errata have not yet been inspected.
- Gary M. Lieberman, *Second Order Parabolic Differential Equations*, World Scientific (1996),
  the chapters on Holder estimates. This is a modern source candidate; exact theorem/page and the
  choice between interior and boundary estimates remain open.

These bibliographic anchors are discovery evidence only, not `H0`. The statement phase must inspect
one fixed edition and transcribe a single theorem rather than synthesize a stronger claim from the
generic theorem name.

## Crosswalk

| Repository phrase | Intended mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "heat equation" | `partial_t u - Delta u = f` | time derivative, spatial Laplacian, pointwise or classical equality | included; domains open |
| "Schauder estimate" | quantitative parabolic Holder regularity | concrete Holder norms and inequality | included; exact norm open |
| parabolic regularity | two spatial derivatives and one time derivative | iterated Frechet derivatives and time derivative | included; encoding open |
| data term | Holder norm of `f` and variant-specific lower-order/boundary data | normed function spaces and restrictions/traces | included; variant open |
| estimate constant | uniform dependency-controlled constant | existential or explicit positive constant with dependency binders | included; dependencies open |

## Existing repository boundary

The legacy blueprint supplies only the Chinese name and the gloss "parabolic equation regularity";
it does not identify a theorem, page, formula, hypotheses, or an existing Lean declaration. Its
`source_status_untrusted` value is metadata and supplies no source or machine-proof credit.

Before `H0`, an independent reviewer must verify the selected edition, exact theorem/page and
formula, definitions, every assumption and constant dependency, boundary conventions, and errata,
then approve a row-by-row source-to-Lean mapping.
