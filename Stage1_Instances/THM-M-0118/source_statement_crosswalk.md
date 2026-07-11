# Source-statement crosswalk

| Claim component | Source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Repository identity | `Docs/researches/math_theorems.md`, "Nakano vanishing theorem", Yoshikazu Nakano, 1957 | none | Metadata source only; its one-line vector-bundle wording is not proof evidence |
| Positive vector-bundle root | S. Nakano, *On complex analytic vector bundles*, J. Math. Soc. Japan 7 (1955), 1-12, DOI `10.2969/jmsj/00710001` | planned expression only | Bibliographic primary-source candidate; exact theorem/page, terminology translation, edition hash, and errata audit are open |
| Modern cohomological formulation | J.-P. Demailly, *Complex Analytic and Differential Geometry*, chapter VII, sections on Bochner-Kodaira-Nakano identity and vanishing theorems | planned sheaf/Dolbeault formulations | Expository discovery anchor only; version/page and premise crosswalk are open |
| Positive line-bundle specialization | Standard Kodaira-Akizuki-Nakano formulation | no exact mathlib declaration located during repository-local intake search | Must not replace the vector-bundle root without an explicit checked specialization/identification |

The canonical intake interpretation is the Nakano-positive vector-bundle vanishing
statement, because it matches both the theorem name and the repository phrase
"vector-bundle cohomology." This remains a provisional freeze at `H2`: Nakano's
paper uses historical analytic notation, and a later source audit must establish
the precise positivity convention, dual/sign convention, degree range, and
cohomology model before the Lean statement gate can close.

The repository-local search `rg -n "Nakano|KodairaNakano|kodaira.*nakano"
.lake/packages/mathlib/Mathlib Formalizations/Lean` found no exact Nakano
vanishing declaration. It found only a Kodaira-vanishing planning note in
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_034.lean`; that note is neither
an anchor nor a proof. No public machine-checked result is claimed.

Required next work: authenticate and hash the primary source; pinpoint theorem
and pages; audit errata and conventions; choose the exact Lean geometric and
cohomology APIs; elaborate the expression; and check transports and mutations.
