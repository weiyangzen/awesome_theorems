# Source-statement crosswalk

| Claim component | Human source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Lie-algebra Fundamental Lemma | B. C. Ngo, *Le lemme fondamental pour les algebres de Lie*, Publications Mathematiques de l'IHES **111** (2010), 1-169, DOI 10.1007/s10240-010-0026-7; introductory theorem statement and its referenced definitions | no faithful declaration selected | Primary proof source identified; verbatim premise/notation transcription, edition hash, and errata review remain open (`H1`) |
| Matching regular semisimple data | Definitions and conventions in the same paper, including the endoscopic setup used by the theorem | legacy `RegularSemisimpleLocus`, `MatchingRegularSemisimpleData` | Legacy structures are unconstrained boundary carriers, not a source-faithful encoding |
| Orbital-integral equality | Source definitions of orbital integrals, stable orbital integrals, transfer factors, measures, and characteristic functions | legacy `OrbitalIntegralComparison` and `StatementShape` | Arbitrary functions and a directly assumed equality omit the mathematical definitions and cannot receive theorem credit |
| Characteristic regime | Ngo's theorem and the characteristic-transfer results it invokes | no Lean candidate | Exact quantifier/bound must be frozen in the statement phase |
| Group formulation | Langlands-Shelstad group Fundamental Lemma and the reduction from group to Lie algebra | no Lean candidate | Related target only; requires separately sourced, checked transports |

The catalog title alone does not determine group versus Lie-algebra formulation, normalization,
residual-characteristic range, or the precise endoscopic variant. This intake selects Ngo's proved
Lie-algebra result because it is the primary theorem named by the cited achievement, while retaining
those choices as explicit statement-review obligations rather than inventing a broader claim.

Discovery link (not an immutable evidence receipt):

- <https://doi.org/10.1007/s10240-010-0026-7>

No `H0` or machine-closure claim is made. Required follow-up is a pinned source copy and digest,
theorem/definition/page crosswalk, assumption and errata audit, exact Lean transcription, checked
group/Lie-algebra transports if used, and independent review.
