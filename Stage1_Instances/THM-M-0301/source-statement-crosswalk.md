# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:2160-2165` supplies the title `BMO空间对偶定理` ("BMO space
duality theorem"), the attribution Charles Fefferman, the year 1971, the gloss
`BMO是H^1的对偶` ("BMO is the dual of H^1"), importance `高` ("high"), and status `已验证`
(`verified`). Git blame places all six uncited lines in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record has no definitions, domain, ordered
binders, hypotheses, conclusion strength, proof boundary, errata, or formal artifact.

`Docs/Stage0_Blueprint.md:8305-8330` repeats the gloss while expressly leaving the exact definitions
and premises, proof route, dependencies, equivalent formulations, axioms, machine status, and
artifact links open. The rev-5.6 manifest retains `verified` only as untrusted metadata and resets
the target to `L0 / rework_required`.

## Inspected primary announcement

Charles Fefferman, "Characterizations of bounded mean oscillation," *Bulletin of the American
Mathematical Society* **77** (1971), no. 4, 587-588,
DOI `10.1090/S0002-9904-1971-12763-5`, is the inspected primary announcement. The official AMS
PDF locator is:

`https://www.ams.org/journals/bull/1971-77-04/S0002-9904-1971-12763-5/S0002-9904-1971-12763-5.pdf`

The inspected two-page PDF has SHA-256
`7352edb3d25ffcfd7473ad738751b5e0d8e7dccd13540b45a57647289405524d`.

On printed page 587, immediately before Theorem 1, Fefferman defines BMO as the locally integrable
functions on `R^n` for which

```text
sup_Q (1 / |Q|) * integral_Q |f(x) - avg_Q f| dx < infinity,
```

where the supremum is over cubes, and identifies two BMO functions when their difference is
constant. Theorem 1 then states that BMO is the dual of `H^1(R^n)` and gives the integral pairing
for a BMO function and an element of the dense subspace of smooth rapidly decreasing functions in
`H^1`. The following paragraph regards `H^1` as the `L^1(R^n)` functions whose Riesz transforms
are all in `L^1`.

Printed page 588 says that Fefferman and Stein's then in-preparation reference contains detailed
proofs. The two-page announcement does not itself spell out the complete Banach norms, all
normalizations, the extension argument, or quantitative norm comparison. A later complete source
candidate is C. Fefferman and E. M. Stein, "H^p spaces of several variables," *Acta Mathematica*
**129** (1972), 137-193, DOI `10.1007/BF02392215`; its exact proof nodes were not accepted or
crosswalked in this intake.

No linked correction appears in the inspected Crossref record, and a narrow bibliographic erratum
query found no correction for the 1971 article. That is negative discovery only. A comprehensive
errata check, complete-proof source audit, and independent source review remain open, so this is
`H1`, not `H0`.

## Component crosswalk

| Source component | Mathematical meaning | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| `R^n` | Euclidean space with Lebesgue measure | `Fin n -> Real` plus volume | dimension and scalar convention open |
| local integrability | BMO representatives are locally integrable | `MeasureTheory.LocallyIntegrable` | generic API present; target definition absent |
| cubes and averages | mean absolute oscillation over every cube | measurable cube sets, volume, restricted integral | cube and null-set conventions open |
| quotient by constants | BMO is normed only modulo constants | seminorm kernel and normed quotient | generic quotient support only |
| `H^1` | `L^1` functions with all Riesz transforms in `L^1` | new Riesz transforms, subspace, norm, completeness | concrete analytic API absent |
| dense test subspace | smooth rapidly decreasing `H^1` functions | Schwartz maps embedded in `H^1` | Schwartz API present; embedding/density absent |
| integral pairing | initially integrate `b(x) g(x)` | Bochner/Lebesgue integral and bounded bilinear map | well-definedness and extension absent |
| "is the dual" | representation, uniqueness modulo constants, bounded inverse | continuous-linear equivalence or paired representation theorems | exact packaging and norm constants open |

## Duplicate crosswalk

`Docs/researches/math_theorems.md:2640-2645` and `Docs/Stage0_Blueprint.md:9989-10014`
separately define `THM-M-0363`, "BMO duality theorem," with the gloss "BMO is the dual space of
H^1," the same attribution, and the same year. Its existing planned dossier maps to the same
Fefferman theorem family. This is compelling duplicate evidence, but target-set identity is an
integration-lane decision. The `THM-M-0363` artifacts are not source authority or shared proof
evidence for this ID.

## Formal boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the intake probe checks
generic local-integrability, `L^p`, integration, Schwartz-map integration, and continuous-linear-map
interfaces. A bounded exact-topic search found no concrete bounded-mean-oscillation, real Hardy
space, or analytic Riesz-transform declaration. These observations are intake discovery, not the
later immutable anchor audit and not a claim of global absence.

Before `H0`, accountable reviewers must select a complete immutable proof source, map every
incorporated definition, premise, proof boundary, transition, and conclusion with pinpoint
locators, resolve corrections and the duplicate identity, and independently approve the mapping.
Before the statement gate, the exact domain, scalars, norms, quotient, transforms, dense subspace,
pairing extension, norm comparison, binders, and boundary cases must be frozen and elaborated.
