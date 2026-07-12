# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` names Michel Plancherel, gives 1910, and describes the theorem as
the isometry of the Fourier transform on `L^2` functions. `Docs/Stage0_Blueprint.md` repeats the
short claim `L^2傅里叶变换的等距性` but leaves exact definitions, assumptions, proof history,
axioms, and artifacts open. The manifest preserves `已验证` only as `source_status_untrusted`.

A historical primary-source candidate is Michel Plancherel, *Contribution a l'etude de la
representation d'une fonction arbitraire par les integrales definies*, Rendiconti del Circolo
Matematico di Palermo 30 (1910), 289-335. This bibliographic locator has not been independently
inspected here. Its exact theorem passage, notation, assumptions, proof boundary, and errata must be
recorded before `H0`; the accent-free title here is not asserted as an edition-accurate quotation.

## Crosswalk

| Repository/source phrase | Mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| `L^2` functions | square-integrable functions modulo almost-everywhere equality | `MeasureTheory.Lp ... 2` with the selected measure | intended; exact domain/measure open |
| Fourier transform | normalized transform and its `L^2` extension | `MeasureTheory.Lp.fourierTransformₗᵢ` / `𝓕` | pinned candidate probed; normalization crosswalk open |
| isometry | preservation of the `L^2` norm for every input | `MeasureTheory.Lp.norm_fourier_eq` | exact semantic candidate, not yet canonical |
| inner-product form | preservation of the `L^2` inner product | `MeasureTheory.Lp.inner_fourier_eq` | candidate equivalent formulation |
| Michel Plancherel / 1910 | historical attribution | no Lean proof credit | primary-source candidate identified |
| `已验证` | inventory metadata | no proposition or proof evidence | explicitly untrusted |

## Existing formal boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.Analysis.Fourier.LpSpace` defines the `L^2` Fourier transform as a linear isometry
equivalence and exposes norm and inner-product preservation. A repository-local legacy wrapper in
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_153.lean` also invokes `norm_fourier_eq`, but it
belongs to another theorem target and supplies no accepted evidence here.

The bounded `IntakeProbe.lean` checks only the pinned declarations and a scalar Euclidean
specialization's type. It does not perform the required statement identity, source-normalization,
terminal-body, axiom, provenance, or independent-review audits. Those remain downstream tasks.
