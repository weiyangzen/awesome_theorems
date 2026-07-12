# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records the title `Mihlin乘子定理`, attributes it to Sigurdur
Helgason, gives the year 1956, and states only `奇异乘子的L^p有界性` ("L^p boundedness of singular
multipliers"). `Docs/Stage0_Blueprint.md` repeats this metadata. The rev-5.6 manifest preserves
`已验证` only as `source_status_untrusted`. None gives a definition, exact proposition, hypotheses,
proof source, edition, page, errata, or formal artifact.

The attribution is suspect rather than accepted: standard English usage calls this the
Mihlin/Mikhlin multiplier theorem after S. G. Mikhlin. The source-audit phase must inspect a primary
publication or a precisely identified authoritative edition, reconcile the name and date, quote
the exact theorem and assumptions, record errata and later qualifications, and obtain independent
review. This intake deliberately does not invent a bibliographic pinpoint.

## Crosswalk

| Repository phrase | Candidate mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "multiplier" | `T_m f = FourierInv (m * Fourier f)` initially on test functions | pinned Fourier transform and multiplier operator with fixed normalization | Schwartz/distribution API probed; exact operator open |
| "singular" | symbol smooth away from zero with scale-invariant derivative control | punctured domain, iterated derivatives/multi-indices, norm bounds | condition absent from source record |
| `L^p` | Lebesgue `L^p(R^n)` for a source-specified `1 < p < infinity` | `MemLp`/`Lp`, Lebesgue measure, exponent side conditions | general APIs probed; exact range open |
| "boundedness" | unique bounded extension and possibly `||T_m|| <= C` | continuous linear map on `Lp` or a quantified norm inequality | conclusion shape absent |
| "1956 / Helgason" | historical attribution | no Lean component | untrusted and requires correction review |
| `已验证` | repository inventory label | no Lean proposition and no proof credit | explicitly rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded intake
probe imports `Mathlib.Analysis.Distribution.FourierMultiplier` and the `L^p` basics. It checks the
Schwartz and tempered-distribution multiplier continuous linear maps, their apply theorem, the
temperate-growth predicate, `MemLp`, `Lp`, and `eLpNorm`. The multiplier module defines operators
on Schwartz functions and tempered distributions; it does not by itself supply the Mihlin
derivative criterion or the required `L^p` bounded extension.

A bounded pinned-mathlib text search found Fourier-multiplier infrastructure but no occurrence of
`Mihlin` or `Mikhlin`. This is feasibility and negative name-search evidence only, not the later
immutable anchor audit or a claim that no differently named formalization exists.

