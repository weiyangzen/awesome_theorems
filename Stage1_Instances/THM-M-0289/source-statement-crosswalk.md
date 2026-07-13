# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:2076-2081` supplies the title `Hardy-Littlewood maximal function
theorem`, attributes it to Godfrey Hardy and John Littlewood, gives the year 1930, and glosses the
claim as `weak-type estimate for the maximal function`. Git blame places all six uncited lines in
commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record provides no formula, definitions,
domain, ordered binders, hypotheses, conclusion strength, proof boundary, errata, or formal
artifact.

`Docs/Stage0_Blueprint.md:7981-8006` repeats the gloss while expressly leaving precise definitions,
premises, proof route, dependencies, alternate forms, axioms, machine status, and artifact links
open. The rev-5.6 manifest retains the source's `verified` label only as untrusted metadata and
resets the target to `L0 / rework_required`.

## Primary-source lead

Crossref metadata for DOI `10.1007/BF02547518` identifies:

> G. H. Hardy and J. E. Littlewood, "A maximal theorem with function-theoretic applications,"
> *Acta Mathematica* 54 (1930), 81-116.

The Crossref response was observed during this intake with SHA-256
`07fe6dcba8fe450170eafbbdb4a1ca4a8d62b0dcc214ce3d9e6d9db79a1ff8dc`. Its author, title,
journal, volume, year, pages, and DOI agree with the catalog's attribution and date. Direct
Project Euclid and Springer PDF requests returned access/HTML pages rather than an article PDF, so
the source text was not inspected. No pinpoint theorem locator, incorporated definition, premise,
conclusion, proof transition, correction status, or complete-proof boundary is credited. This is
an `H1` source lead, not `H0` evidence.

## Component crosswalk

| Catalog component | Mathematical component to freeze | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| Hardy-Littlewood maximal function | centeredness, averaging sets, radius range, normalization | a canonical definition using balls/cubes, measure, and integral APIs | absent |
| weak-type estimate | exact superlevel-set measure inequality, threshold and strictness | `Measure`, set comprehension, `ENNReal`/`Real` inequality | shape only; formula open |
| input function | codomain, representative, measurability, and finite `L1` size | `AEMeasurable`, `Integrable`, `L1`, `lintegral`, norm/enorm | open |
| ambient setting | dimension, metric/norm, Borel structure, Lebesgue measure | finite Euclidean space or source-selected generalization | open |
| estimate constant | explicit or existential constant and dimension dependence | a typed numeric term or quantified finite constant | open |
| `verified` | untrusted catalog status | no declaration and no proof credit | rejected as evidence |

## Duplicate crosswalk

`Docs/researches/math_theorems.md:2675-2680` and `Docs/Stage0_Blueprint.md:10124-10149`
separately define `THM-M-0368`, "maximal function theorem," with the gloss "Hardy-Littlewood
maximal function weak-type estimate," the same Hardy/Littlewood attribution, and the same year.
Its planned dossier maps the same apparent theorem family. This is strong duplicate evidence, but
target-set identity is an integration-lane decision. Its artifacts are not source authority or
shared proof evidence for this ID.

## Pinned Lean boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the intake probe imports
`Mathlib.MeasureTheory.Covering.Besicovitch` and
`Mathlib.MeasureTheory.Measure.Lebesgue.EqHaar`. It checks APIs for balls, Lebesgue/Haar measure,
lower integrals, Besicovitch covering, and Vitali-family measure bounds. A bounded source-tree name
search found no declaration defining the Hardy-Littlewood maximal operator or stating its weak
`(1,1)` estimate. Nearby covering and differentiation results are ingredients, not closure. These
observations are intake discovery only, not the later immutable anchor audit and not a global
absence claim.

## External Lean candidate

Immutable raw-source inspection of `fpvandoorn/carleson` commit
`fdcce451b494680b1fd5534236a71d9b258860b2` located
`Carleson/ToMathlib/HardyLittlewood.lean` (Git blob
`6933e211fcdd5d38cf08691af54b73348367c978`; observed raw SHA-256
`a6658eefb1c1a29509dadb21b8568c1504ac95da83d9d24f6c99646a7df28d22`). Lines 29-37 define
an uncentered maximal function as a supremum of ball averages. Lines 211-233 prove:

```text
hasWeakType_maximalFunction_one [BorelSpace X] [SeparableSpace X] :
  HasWeakType (maximalFunction μ B c r 1) 1 1 μ μ (A ^ 2)
```

under the surrounding pseudometric, measurable-space, normed-codomain, and doubling-measure
context. The immutable commit's GitHub Actions run `27613659124` reports successful `Build project`
and `Lint style` jobs. Its toolchain is `leanprover/lean4:v4.30.0-rc2`, its manifest pins mathlib
`1a4917a18b30ea1333c195e597067fe044ac9176`, and the repository license is Apache-2.0.

This is a credible immutable formal lead, but it does not yet support root `M1` or `M0`. It is not in
this repository's pinned dependency closure, targets a newer toolchain and mathlib, was not rebuilt
here, and has not been mapped to an inspected or frozen exact Hardy-Littlewood human statement. The
family-of-balls and doubling-space generality, constant `A ^ 2`, and `HasWeakType` packaging may be
broader than the eventual canonical claim. Exact-type transport, independent upstream build and
terminal dependency evidence, axiom provenance, placeholder/unsafe closure, license/SBOM
integration, and repo-local feasibility belong to the statement and anchor-audit phases. The
unfrozen root therefore remains `M4` at intake.

Before `H0`, accountable reviewers must preserve and inspect an immutable source edition, map every
incorporated definition, premise, proof node, conclusion, and correction with pinpoint locators,
resolve duplicate identity, and independently approve the mapping. Before the statement gate, the
operator convention, domain, dimension, function model, threshold, constant, binders, and boundary
cases must be frozen and elaborated without broadening or substitution.
