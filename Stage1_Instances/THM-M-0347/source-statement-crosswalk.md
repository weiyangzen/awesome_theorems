# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records `费耶尔定理`, attributes it to Lipot Fejer, dates it to
1900, and gives the gloss `连续函数的Cesàro平均收敛` ("the Cesaro means for a continuous function
converge"). Stage0 repeats that text and leaves exact definitions, premises, equivalent forms,
axioms, and formal artifacts open. The rev-5.6 manifest retains `已验证` only as
`source_status_untrusted`; it supplies no proof credit.

The same research inventory contains a distinct real-analysis record, `THM-M-0291`, whose gloss
explicitly says "converge uniformly". That nearby metadata supports detecting a possible omitted
qualifier, but it is not an authoritative source and cannot be substituted for this target.

## Primary-source work

The historical attribution and date suggest Fejer's original 1900 work on Fourier series, while a
stable modern Fourier-analysis text is likely better suited to freezing contemporary notation.
Neither an immutable edition nor a theorem/page passage was inspected during this bounded intake.
The source audit must record author, title, edition, theorem and page, all premises and conventions,
proof boundary, and known errata, followed by independent review. Until then the root is `H1`, not
`H0`.

## Crosswalk

| Repository phrase | Intended mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "continuous function" | continuous complex-valued function on a periodic domain | `C(AddCircle T, ℂ)` | included; scalar and period open |
| "Fourier" (implicit in theorem name/context) | normalized coefficients and symmetric partial sums | `fourierCoeff`, `fourier`, finite integer sums | family located; exact normalization open |
| "Cesaro means" | first-order arithmetic means of partial sums | finite sums and scalar division indexed by naturals | definition not frozen |
| "converge" | standard Fejer conclusion, expected uniform convergence to `f` | `Tendsto` in sup norm or `TendstoUniformly` | exact encoding and source qualifier open |
| `已验证` | untrusted inventory label | no Lean proposition or proof | explicitly rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the intake probe imports
`Mathlib.Analysis.Fourier.AddCircle` and checks the additive-circle Fourier ingredients plus the
uniform-limit predicate available through that import closure. Mathlib also has a stronger-hypothesis result
`hasSum_fourier_series_of_summable`, which assumes summability of the Fourier coefficients. It is
not Fejer's theorem for every continuous function and is not credited as a formal anchor or proof.
No declaration named for Fejer was found by the bounded repo-local name search; the later immutable
anchor audit remains open.
