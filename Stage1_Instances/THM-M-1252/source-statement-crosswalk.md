# Source-statement crosswalk

## Candidate primary sources

- Laurent Schwartz, *Theorie des distributions*, Hermann, Paris, first edition volumes (1950-51),
  is the historical primary-source candidate. The precise volume, edition, section, proposition,
  page, wording, and errata have not yet been inspected.
- Laurent Schwartz, *Theorie des distributions*, new edition, Hermann (1966), is a later
  authorial source candidate whose pagination and formulation must not be conflated with the first
  edition.

These bibliographic anchors are discovery leads, not `H0` evidence. The next phase must inspect a
stable scan or edition and transcribe the exact proposition and definitions.

## Provisional crosswalk

| Repository wording | Mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "support of a distribution" | complement of the largest open zero region | distribution, restriction/vanishing, relative complement | subject included; exact definition open |
| "localization of a distribution" | behavior determined on open subsets by supported tests | compactly supported smooth test functions and evaluation | intended family only; root wording open |
| open zero region | restriction is the zero functional | restriction map or an equivalent supported-test predicate | API and equivalence open |
| support disjoint from an open set | local vanishing characterization | set support, disjointness, relative topology | boundary conventions open |

## Exact-statement blocker

The repository metadata is not a proposition and the two phrases admit several neighboring
results. Exact statement identity therefore remains blocked until a primary-source theorem anchor
is inspected. This fail-closed decision prevents the intake from inventing a theorem or upgrading
the untrusted `已验证` label. A future statement artifact must record a row-by-row source transcription,
assumptions, definitions, errata check, and checked Lean encoding.
