# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:9943-9948` supplies exactly the title `Lorenz系统`, Edward
Lorenz, 1963, the gloss `混沌的经典例子`, importance `high`, and status `已验证`. Git history
places all six uncited lines in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.
The record contains no bibliography, equation, parameters, definition, binder, hypothesis,
conclusion, proof route, correction, erratum, or formal artifact.

`Docs/Stage0_Blueprint.md:37101-37126` repeats the gloss while explicitly leaving the formal system,
foundation, exact definitions and premises, proof process, dependencies, alternate statements,
axioms, machine status, and artifact links open. The rev-5.6 manifest retains `已验证` only as
untrusted source metadata and resets the target to `L0 / rework_required`.

## Bibliographic discriminator

The author and date strongly match Edward N. Lorenz, *Deterministic Nonperiodic Flow*, **Journal of
the Atmospheric Sciences** 20(2) (1963), 130-141, DOI
`10.1175/1520-0469(1963)020<0130:DNF>2.0.CO;2`. Crossref metadata retrieved on 2026-07-13 confirms
the title, author, journal, volume, issue, pages, year, and DOI; the captured response had
SHA-256 `4972bd7d07af8983340449f8e11d24a8d1d86b162ac4bd68787f1eabba3846d0`.

This identifies a likely historical paper, not one catalog-selected theorem. The publisher PDF was
not accessible in this worker run, so no page/equation transcription, proof-boundary inspection, or
errata review is claimed. Even a complete reading would still require an accountable selection:
Lorenz's paper introduces a finite truncation, studies numerical solutions, and discusses
nonperiodic behavior, while later literature contains distinct analytic, geometric, symbolic, and
computer-assisted theorems. The catalog gives no locator selecting one of them. Crossref metadata is
therefore discovery evidence only and receives no H0 credit.

## Component crosswalk

| Catalog component | Source-family alternatives | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| `Lorenz系统` | original convection truncation, conventional polynomial vector field, parameterized family, or geometric Lorenz model | exact vector field, parameters, state/time types, integral curves or flow | mathematical object family recognized; target not selected |
| Edward Lorenz / 1963 | likely historical provenance for *Deterministic Nonperiodic Flow* | immutable source edition, pinpoint locator, incorporated definitions | paper metadata identified; exact passage and claim unresolved |
| "classic example" | informal historical/classificatory description | no proposition follows without a quantified property | not truth-valued as supplied |
| "chaos" | nonperiodicity, sensitivity, transitivity, dense periodic points, entropy, horseshoe, strange or singular-hyperbolic attractor | one exact predicate with metric/topology/measure, invariant set, and quantifier scope | all definitions and conclusion strength absent |
| classical parameters | often `sigma = 10`, `rho = 28`, `beta = 8/3`, but other papers prove interval or perturbative results | exact rationals/reals and parameter-domain hypotheses | catalog supplies no parameters |
| computer-assisted result | interval enclosures, return maps, cone conditions, or other certificate-driven proof | verified certificate semantics, sound checker, exact error bounds, oracle/TCB boundary | no source or computation contract selected |
| `已验证` | untrusted inventory field | no declaration or proof body | no H or M credit |

## Source gate

Before the target can leave `H5`, an accountable reviewer must lawfully preserve an immutable
primary or authoritative source, select one truth-valued root and all incorporated definitions,
pinpoint its exact equation/theorem/page, transcribe every domain, ordered binder, hypothesis,
conclusion, parameter, exceptional case, and computation boundary, inspect corrections and errata,
and explain why it represents `THM-M-1364` rather than neighboring chaos, horseshoe, entropy,
Lyapunov-exponent, or random-attractor targets. A second qualified reviewer must approve that
mapping. Human-proof status
must then be classified afresh rather than inherited from `已验证`.

## Formal crosswalk boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the discovery-only
probe checks generic integral-curve, flow, fixed-point, invariant-set, derivative, omega-limit, and
compactness interfaces. A bounded lexical search over repo-local Lean and pinned mathlib found no
declaration named for the Lorenz system, Lorenz equations, Lorenz attractor, or geometric Lorenz
flow. Matches for the surname-like string `Lorenz` referred to unrelated authors or bibliography.
This is not the downstream exhaustive formal-anchor audit and does not establish absence from
external Lean projects.

The statement phase must first resolve the source gate. Only then may it freeze a canonical Lean
expression, minimal imports, checked alternate-form transports, expression/environment
fingerprints, and statement mutations.
