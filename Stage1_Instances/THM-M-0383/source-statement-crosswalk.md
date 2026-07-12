# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` contains the record twice with the Chinese title
`Bourgain限制性定理`, attribution Jean Bourgain, year 1991, and only the gloss
`高维Fourier限制性定理` ("higher-dimensional Fourier restriction theorem").
`Docs/Stage0_Blueprint.md` repeats that metadata and explicitly leaves exact definitions,
hypotheses, proof route, equivalent forms, axioms, and formal artifacts open. The rev-5.6 manifest
preserves `已验证` only as `source_status_untrusted`.

None of these repository surfaces supplies a paper title, journal/version, theorem or equation
number, page, dimension, hypersurface, exponents, hypotheses, conclusion, proof passage, errata, or
formal artifact. The two identical inventory occurrences do not constitute independent sources.

## Candidate source work

Bourgain's 1991 publications and authoritative restriction-theory histories are candidate locators,
but this intake does not guess which publication or theorem the compiler intended. The source-audit
phase must identify an immutable primary passage, record its bibliographic identity and exact
statement, distinguish theorem from conjecture and later reformulations, map all notation and
assumptions, check corrections and endpoint qualifications, and obtain independent review. A broad
citation to Bourgain or to restriction theory is not an `H0` crosswalk.

## Crosswalk

| Repository phrase | Possible mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "Fourier" | Euclidean transform or a discrete Fourier/exponential sum | fixed transform definition and normalization | pinned Euclidean API probed; choice open |
| "restriction" | trace of the transform on a hypersurface | surface, surface measure, representative/trace semantics, and a norm bound | absent from source record |
| "restriction" | dual extension operator estimate | oscillatory integral/Bochner integral and duality transport | alternative only |
| "higher-dimensional" | a specified ambient or surface dimension | a fixed `n` or quantified dimension range | absent from source record |
| "theorem" | global, local, discrete, or partial exponent-range result | concrete `Prop`, ordered binders, exponents, constants, and boundary cases | absent from source record |
| `已验证` | untrusted inventory label | no Lean proposition and no proof credit | explicitly rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded intake
probe checks the Euclidean Fourier transform, the `L^1` Fourier-transform map, `MemLp`, extended
`L^p` norm, metric spheres, and measure restriction. These are only nearby encoding ingredients.
They do not define canonical hypersurface measure or trace semantics and do not assert any Bourgain
estimate. A bounded source/name search found general Fourier infrastructure but is not the later
immutable formal-anchor audit and receives no negative-exhaustiveness claim.
