# Source-statement crosswalk

## Repository sources inspected

`Docs/researches/math_theorems.md` records the Chinese title, attributes it to Shou-Wu Zhang,
gives 1997, and says only "higher-dimensional generalization of the Gross-Zagier formula".
`Docs/Stage0_Blueprint.md` repeats that gloss and explicitly leaves exact definitions, hypotheses,
equivalent formulations, axioms, and machine artifacts open. The rev-5.6 manifest carries the
repository's `已验证` label as `source_status_untrusted`; it grants no source or proof credit.

## Primary-source discovery candidate

Shou-Wu Zhang, *Heights of Heegner cycles and derivatives of L-series*, Inventiones Mathematicae
130 (1997), 99-152, is a strong bibliographic candidate matching the author, year, and subject.
It is only a discovery locator in this intake. A stable copy was not inspected here to select an
exact theorem or equation, so the theorem/page, wording, assumptions, normalization, proof
boundaries, corrections, and errata remain open. The citation is not `H0` evidence.

## Crosswalk

| Repository/source phrase | Candidate mathematical component | Required Lean surface | Intake status |
|---|---|---|---|
| "Gross-Zagier" | comparison of a Heegner object with an L-series derivative | explicitly constructed cycle, height pairing, L-function, derivative | family identified; exact objects open |
| "higher-dimensional" | higher-weight form and a Heegner cycle on a Kuga-Sato or related variety | schemes/varieties, cycles, projector, intersection or height theory | meaning and dimension convention open |
| "formula" | equality with normalization constants | equality in a fixed scalar field, with every factor represented | no equation supplied |
| Shou-Wu Zhang / 1997 | bibliographic locator | source provenance only | candidate paper located; pinpoint not inspected |
| `已验证` | untrusted inventory status | no proposition or proof credit | explicitly rejected as evidence |

## Source and machine boundary

No theorem-specific Lean source or declaration is asserted at intake. A repository text search is
not a complete mathlib or external-project audit, and that downstream work must not begin until the
exact statement is selected. Before `H0`, an independent source reviewer must approve the edition,
pinpoint theorem/equation, definitions, each hypothesis and constant, proof boundaries, and errata.
Before statement credit, the approved rows must map to a kernel-elaborated Lean expression, with
checked transports for any alternate normalization.
