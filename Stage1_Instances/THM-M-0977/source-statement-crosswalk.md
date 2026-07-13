# Source-statement crosswalk

## Repository record and provenance

`Docs/researches/math_theorems.md:7134-7139` supplies exactly the title `Chernoff界`, Herman
Chernoff, 1952, the gloss `独立随机变量和的尾概率`, importance `高`, and status `已验证`.
All six uncited lines originate at repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no formula, bibliography,
edition, theorem/page, definitions, binders, assumptions, conclusion, proof boundary, correction,
erratum, reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:26632-26657` assigns `THM-M-0977` while explicitly leaving definitions,
premises, proof, dependencies, equivalent forms, axioms, machine status, and artifact links open.
The generated `已验证` scheduling bucket is not source or kernel evidence.

## Duplicate catalog record

`Docs/researches/math_theorems.md:7259-7264` repeats the same author, year, gloss, importance, and
status under the translated title `切尔诺夫界` in a probability category; generation assigns it
`THM-M-0993`. Exact-field deduplication does not merge the two titles, so both survive as rev-5.6
targets. Category placement and translation alone do not prove that their statements differ.

The existing provisional `THM-M-0993` worker intake selected a fixed-tilt product-MGF upper-tail
statement, and later worker artifacts contain a self-tested kernel-checking composition for that
separately selected target. Their master acceptance, status, and all credit remain independently
owned and open. That selection is not grounded by a pinpoint catalog-source mapping and is not
imported here; the master must resolve identity/allocation before any cross-target statement choice.

## Human source lead

A plausible historical lead is Herman Chernoff, *A Measure of Asymptotic Efficiency for Tests of a
Hypothesis Based on the Sum of Observations*, *Annals of Mathematical Statistics* 23(4) (1952),
493-507, DOI `10.1214/aoms/1177729330`. Crossref metadata was observed, but the Project Euclid
article and PDF endpoints returned access-control HTML rather than the article in this worker
environment. The paper text, pinpoint result, incorporated definitions, premises, conclusion,
proof passage, correction and errata status, and relationship to modern results called "Chernoff
bounds" were therefore not inspected or preserved. This is a bibliographic lead only and cannot
support H0 or select a root.

| Catalog component | Source mapping | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| "Chernoff bound" | 1952 bibliographic lead; exact theorem locator uninspected | one exact `Prop` after source selection | Family identified; root open |
| Independent variables | Catalog gloss only; independence strength and indexing absent | `iIndepFun`, finite family, or another source-faithful encoding | Candidate only |
| Sum | No finite/asymptotic index or codomain supplied | `Finset.sum`, `Fintype` sum, sequence partial sum | Open |
| Tail probability | No upper/lower/two-sided or event convention supplied | `Measure.real` or another probability representation | Open |
| Bound formula | No MGF, CGF, optimized, additive, multiplicative, or rate formula supplied | mathlib candidate family below | Open |
| Assumptions | No measurability, integrability, boundedness, Bernoulli, or parameter conditions | explicit hypotheses and typeclasses | Open |
| Boundaries | No empty-family, zero-tilt, endpoint, or infinite-moment policy | checked cases and mutations | Open |

No material premise, transition, or conclusion currently reaches an immutable primary source
locator. The human classification is provisional `H1`, not H0: a standard published family and
bibliographic lead are known, but exact source fidelity and independent review are absent.

## Formal candidate crosswalk

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.Probability.Moments.Basic` exposes:

| Candidate declaration | Exact-topic role | Credit boundary |
|---|---|---|
| `ProbabilityTheory.measure_ge_le_exp_mul_mgf` | upper tail at nonnegative tilt | single random variable / sum after composition; not a selected root |
| `ProbabilityTheory.measure_le_le_exp_mul_mgf` | lower tail at nonpositive tilt | distinct direction; not interchangeable |
| `ProbabilityTheory.measure_ge_le_exp_cgf` | upper-tail CGF form | weaker/equivalent relationship to MGF form not accepted here |
| `ProbabilityTheory.measure_le_le_exp_cgf` | lower-tail CGF form | distinct direction; not a selected root |
| `ProbabilityTheory.iIndepFun.integrable_exp_mul_sum` | exponential integrability of a finite independent sum | bridge candidate only |
| `ProbabilityTheory.iIndepFun.mgf_sum` | finite independent-sum MGF factorization | bridge candidate only |
| `ProbabilityTheory.iIndepFun.cgf_sum` | finite independent-sum CGF additivity | bridge candidate only |

`IntakeProbe.lean` elaborates these interfaces and reports candidate axioms `propext`,
`Classical.choice`, and `Quot.sound`. It does not state or prove this target. Repo-local
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_273.lean` and
`Stage1_Instances/THM-M-0993` are historical/cross-target discovery surfaces, not owned evidence.

## Next source gate

An independent probability reviewer and the integration lane must obtain and immutably identify an
authoritative source, pinpoint one exact result, map every incorporated definition and premise,
audit corrections/errata and modern naming, and resolve the `THM-M-0977`/`THM-M-0993` allocation.
Only then may the statement phase choose a mathematical proposition and encode, elaborate,
fingerprint, transport, and mutation-test its exact Lean target.
