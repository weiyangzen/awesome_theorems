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
| `L^2` functions | square-integrable functions modulo almost-everywhere equality | `hf : MemLp f 2 volume` and `hf.toLp f` | repository-scope formal target frozen |
| Fourier transform | normalized transform and its `L^2` extension | `𝓕 (hf.toLp f)` from pinned `LpSpace` | repository-scope formal target frozen; historical normalization crosswalk open |
| isometry | preservation of the `L^2` norm for every input | equality `‖𝓕 (hf.toLp f)‖ = ‖hf.toLp f‖` | canonical formal conclusion frozen |
| inner-product form | preservation of the `L^2` inner product | `MeasureTheory.Lp.inner_fourier_eq` | not credited as an alternate encoding at statement gate |
| Michel Plancherel / 1910 | historical attribution | no Lean proof credit | primary-source candidate identified |
| `已验证` | inventory metadata | no proposition or proof evidence | explicitly untrusted |

## Existing formal boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.Analysis.Fourier.LpSpace` defines the `L^2` Fourier transform as a linear isometry
equivalence and exposes norm and inner-product preservation. A repository-local legacy wrapper in
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_153.lean` also invokes `norm_fourier_eq`, but it
belongs to another theorem target and supplies no accepted evidence here.

The statement artifact now freezes the norm equality for complex functions on
`EuclideanSpace Real (Fin n)`, including `n = 0`, and mutation-tests its hypothesis, domain, binder
scope, and boundary. This settles repository-scope statement identity, not historical source
identity: source-normalization, terminal-body, axiom, provenance, and independent-review audits
remain downstream tasks.
