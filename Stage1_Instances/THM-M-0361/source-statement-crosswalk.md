# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records the title `Fefferman-Stein定理`, attributes it to Charles
Fefferman and Elias Stein, gives the year 1972, and states only `H^p空间的实变刻画` ("a
real-variable characterization of H^p spaces"). `Docs/Stage0_Blueprint.md` repeats that metadata.
The rev-5.6 manifest carries `已验证` only as `source_status_untrusted`. None supplies a theorem
number, exact hypotheses, conclusion, proof reference, edition/page, errata, or formal artifact.

The attribution and date suggest Fefferman and Stein's 1972 work on several-variable Hardy spaces,
but that bibliographic clue is not enough to choose one of its several characterizations. No
primary-source passage was accepted during intake.

## Candidate source work

The statement/source audit must inspect an immutable copy of the relevant Fefferman-Stein paper and
authoritative later presentations, then select the exact intended theorem. It must record title,
journal/edition, theorem or section and page, original notation, ambient dimension, `p` range,
kernel/test-function conditions, equivalence constants, proof boundary, and any corrections. An
independent reviewer must confirm the mapping. Until then, naming a radial-maximal or area-function
theorem would be speculation rather than an `H0` crosswalk.

## Crosswalk

| Repository phrase | Possible mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| `H^p` space | a real Hardy space of functions or tempered distributions | an explicit structure/predicate, ambient measure space, exponent, and quasinorm | absent; exact model open |
| "real-variable" | maximal, grand maximal, area, or square functional | explicit convolution/extension, supremum/integral, kernel and normalization definitions | nearby APIs probed; functional open |
| "characterization" | membership equivalence and possibly two-sided quasinorm bounds | a concrete `Iff` and/or inequalities with constants and dependencies | absent from source record |
| Fefferman-Stein | 1972 Hardy-space results or other same-name inequalities | pinpoint source identity preventing theorem substitution | unresolved |
| `已验证` | untrusted inventory label | no Lean proposition and no proof credit | explicitly rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded intake
probe imports `Lp` infrastructure, convolution, Fourier transform, and Schwartz functions and
checks representative declarations. These are only ingredients from which a future formalization
might define distributions, dilations, maximal functions, and quasinorm conditions. The bounded
repository/mathlib search found no Hardy-space or Fefferman-Stein declaration to credit; this
negative name search is not the exhaustive immutable anchor audit required downstream.
