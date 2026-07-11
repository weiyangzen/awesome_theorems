# Source-statement crosswalk

## Candidate sources

- Alexander Grothendieck, "Resume de la theorie metrique des produits tensoriels topologiques",
  *Boletim da Sociedade de Matematica de Sao Paulo* 8 (1953), 1-79. This is the historical primary
  source candidate. Its exact theorem/page, original terminology, normalization, and any errata
  have not yet been inspected.
- Gilles Pisier, *Grothendieck's Theorem, Past and Present*, Bulletin of the AMS 49 (2012), 237-323.
  This is a modern secondary discovery source for equivalent formulations, not yet H0 evidence and
  not a replacement for primary-source verification.

The bibliographic rows are discovery anchors only. Accents are transliterated here to keep this
ASCII artifact stable; citation spelling must be checked against the selected edition.

## Crosswalk

| Repository phrase | Intended component | Required Lean component | Intake status |
|---|---|---|---|
| "Grothendieck inequality" | universal comparison theorem | existential universal real constant | included; normalization open |
| finite real matrix | coefficients indexed by two finite sets | `Fintype` indices and `A : m -> n -> Real` | included; binder order open |
| scalar bound | supremum over scalar unit vectors/signs | finite sums plus absolute-value unit constraints | included; equivalent variant open |
| Hilbert bound | sum weighted by inner products | arbitrary real inner-product space and norm constraints | included; dimension convention open |
| universal constant | independent of all input data | outer existential with nonnegativity | included; strict positivity open |

## Existing Lean boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_214.lean` defines scalar and Hilbert matrix forms
and a candidate `StatementShape`. It explicitly says no terminal proof is claimed. Its pinned
revision, imports, source audit, universes, and equivalence to the selected source must be rechecked;
under the uniform L0 baseline it receives no accepted statement or proof credit.

Before H0, an independent reviewer must inspect a stable primary-source copy and record edition,
page/theorem, every hypothesis, real/complex convention, normalization, definitions used, and
errata, then approve the source-to-Lean mapping and any equivalence transports.
