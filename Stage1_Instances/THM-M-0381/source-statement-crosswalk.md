# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records the Chinese title `Strichartz估计`, attributes it to
Robert Strichartz, dates it to 1977, and gives only `色散方程解的时空估计` ("space-time estimates
for solutions of dispersive equations"). A duplicated inventory entry uses the nearly identical
phrase `色散方程的时空估计`. Stage0 repeats the former gloss while leaving exact definitions,
assumptions, proof route, axioms, and artifacts open. The rev-5.6 manifest retains `已验证` only as
`source_status_untrusted`. None of these records supplies a mathematical proposition.

## Candidate source work

Robert S. Strichartz, *Restrictions of Fourier transforms to quadratic surfaces and decay of
solutions of wave equations*, Duke Mathematical Journal 44 (1977), 705-714, is a historical
primary-paper candidate consistent with the attribution and year. It is recorded only as a
discovery locator. No exact theorem/page, equation variant, exponent range, assumptions, later
correction, or errata has been accepted during intake, so the citation is not `H0` evidence.

The later statement/source audit must inspect an immutable copy, select a precise theorem, map its
notation and every premise, record edition/page and errata, distinguish later endpoint extensions,
and obtain independent review.

## Crosswalk

| Repository/source phrase | Possible mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "dispersive equation" | wave, Schrodinger, or another evolution | exact solution predicate or propagator with domain/codomain | equation open |
| "space-time" | an iterated `L^q_t L^r_x` norm | time/space measures, sections, measurability, `Lp`/`eLpNorm` encoding | pinned ingredients probed; norm convention open |
| "estimate" | a bound by an initial-data or forcing norm | inequality, constant, input norm, and constant dependencies | conclusion open |
| admissible exponents | scaling and range constraints | exponent parameters and exact side-condition predicate | absent from record |
| endpoint | included or excluded boundary pairs | finite/infinite exponent and exceptional-case branches | policy open |
| 1977 / Strichartz | bibliographic locator | no Lean proposition or proof credit | candidate paper only |
| `已验证` | untrusted inventory label | no proposition and no proof credit | explicitly rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, `IntakeProbe.lean`
checks concrete APIs for `Measure`, product measures, `MemLp`, `Lp`, `eLpNorm`, time sections, and
the `L2` Fourier-transform isometry. These are encoding ingredients only. The bounded local search
found Strichartz-named declarations only in a legacy Stage1 interface for another theorem, where
the estimates are assumed fields and explicitly remain formalization debt. This is neither a
theorem-specific immutable anchor audit nor closure evidence for `THM-M-0381`.
