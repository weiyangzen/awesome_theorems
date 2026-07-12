# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` contains two records with the gloss `H^1空间的原子分解`. One is
titled `哈代空间原子分解` and becomes `THM-M-0300`; the other is titled `原子分解定理` and becomes
this target, `THM-M-0362`. Both attribute the item to Charles Fefferman and Elias Stein, give 1972,
importance "high", and the status `已验证`. Stage0 adds no definitions, assumptions, source, proof,
or formal artifact. The duplicate-like records are distinct manifest targets; neither may silently
supply a more precise statement to the other.

The manifest correctly preserves `已验证` only as `source_status_untrusted`. It is not evidence of
an exact human proof crosswalk or a machine proof.

## Candidate source work

Fefferman-Stein publications from the stated period and later authoritative harmonic-analysis
treatments are candidate locators, not accepted sources at intake. The source audit must identify
the intended primary publication, immutable edition, theorem and page, definitions, hypotheses,
normalizations, constants, proof boundaries, and errata, and must independently review every
crosswalk row. Assigning a specific 1972 paper or formulation without that inspection would be
speculation rather than `H0` evidence.

## Crosswalk

| Repository phrase | Possible mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| `H^1` space | real-variable Hardy space, likely on Euclidean space | exact carrier, measure, maximal-function/distribution definition, normed-space encoding | unidentified |
| atom | localized integrable function with size and cancellation conditions | predicate containing support, measurability, integral/moments, and norm bound | convention open |
| atomic decomposition | countable representation with summable coefficients | sequence of atoms/scalars, summability, series convergence, equality modulo a.e. if appropriate | conclusion open |
| decomposition theorem | equality/characterization of spaces, often with norm estimates | both implications and checked quantitative bounds | source wording insufficient |
| `已验证` | untrusted inventory label | no Lean proposition and no proof credit | explicitly rejected |

## Pinned Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded intake
probe checks `MeasureTheory.Lp`, `MemLp`, `Integrable`, Bochner `integral`, Haar `volume`,
`Filter.Tendsto`, and `Summable`. These are only possible substrate for an encoding. A bounded name
search did not locate a Hardy-space or atomic-decomposition root in pinned mathlib. This negative
search is not the later immutable anchor audit and provides no proof credit.

