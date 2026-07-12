# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records the title `Littlewood-Paley理论`, attributes it to John
Littlewood and Raymond Paley, gives the year 1931, and states only `函数的频率分解` ("frequency
decomposition of functions"). `Docs/Stage0_Blueprint.md` repeats that metadata. The rev-5.6
manifest carries `已验证` only in the explicitly untrusted source-status field. None supplies a
definition, theorem, hypotheses, conclusion, proof reference, edition, page, errata, or formal
artifact.

The same research inventory contains another similarly titled record, represented by the distinct
manifest target `THM-M-1298`, whose gloss uses `函数的频域分解` and whose category is PDE. This
duplication reinforces that the present ID must be scoped from its own source rather than merged by
title.

## Candidate source work

The original Littlewood-Paley papers and authoritative harmonic-analysis texts are candidate
locators, but no edition, paper section, theorem number, or page has been accepted during intake.
The source-audit phase must locate the intended statement, record its exact bibliographic identity,
notation, hypotheses, constants, proof boundary, later corrections or endpoint qualifications, and
obtain independent review. Naming a familiar modern square-function theorem now would not establish
that it is the repository claim.

## Crosswalk

| Repository phrase | Possible mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "function" | periodic function, Euclidean function, or tempered distribution | a concrete `Lp`, function, or distribution type and measure | exact domain open |
| "frequency" | Fourier coefficient or Fourier transform variable | circle Fourier basis or Euclidean Fourier transform with fixed normalization | pinned APIs probed; choice open |
| "decomposition" | sharp/smooth dyadic projections and possibly a low-frequency block | multiplier/cutoff definitions plus support and partition-of-unity conditions | absent from source record |
| "theory" | square-function inequality, norm equivalence, or reconstruction theorem | a concrete `Prop` with ordered binders and constants | absent from source record |
| `已验证` | untrusted inventory label | no Lean proposition and no proof credit | explicitly rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded intake
probe imports the `L^2` Fourier transform, circle Fourier series, tempered-distribution Fourier
multiplier, and `L^p` modules. It checks the `L^2` Fourier isometry and norm theorem, the circle
Fourier basis and `L^2` series convergence theorem, the multiplier API, and `MemLp`/`eLpNorm`.
These are nearby encoding ingredients only. No dyadic projections, partition of unity, square
function, exponent-range theorem, or exact declaration for the repository wording is credited.
The bounded repository/mathlib name search is discovery evidence, not the later immutable anchor
audit.

