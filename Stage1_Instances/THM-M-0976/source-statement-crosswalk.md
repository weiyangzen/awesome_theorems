# Source-statement crosswalk

## Repository source

The source corpus contains three identical uncited records:

- `Docs/researches/math_theorems.md:7127-7132` in combinatorics;
- `Docs/researches/math_theorems.md:7294-7299` in probability; and
- `Docs/researches/math_theorems.md:7919-7924` in stochastic processes.

Each gives title `McDiarmid不等式`, attribution Colin McDiarmid, year 1989, gloss
`有界差函数的集中`, high importance, and status `已验证`. All originate in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The records contain no bibliography, formula,
definition, theorem locator, premise, constant, proof boundary, correction record, reviewer, or
formal artifact. Repository generation deduplicates identical records and the manifest retains the
combinatorics category.

`Docs/Stage0_Blueprint.md:26605-26630` repeats the metadata while explicitly leaving exact
definitions and premises, proof route, equivalent forms, axiom policy, machine status, and artifact
links open. The rev-5.6 manifest resets the target to `L0 / rework_required` and marks the historical
verified label untrusted.

## Bibliographic source lead

Crossref and Cambridge Core metadata observed on 2026-07-13 identify Colin McDiarmid, "On the
method of bounded differences," in *Surveys in Combinatorics, 1989*, Cambridge University Press,
pages 148-188, Crossref `published-print` date 1989-08-03, DOI
`10.1017/CBO9781107359949.008`, and ISBNs `9780521378239` and `9781107359949`.

This metadata is a credible lead consistent with every catalog field, but the repository does not
cite it. No lawful immutable full chapter was added, and no exact theorem number/page, statement,
definitions, proof passage, correction or errata history, or independent review was accepted. The
locator therefore remains `E5` discovery evidence and cannot establish `H0`.

## Clause crosswalk

| Repository phrase or candidate clause | Human-source status | Required Lean component | Intake decision |
|---|---|---|---|
| bounded-difference function | exact domain, codomain, regularity, and difference convention absent | function on a finite dependent product plus a coordinate-replacement predicate | family identified; encoding open |
| independent inputs | omitted by the gloss | probability space/product laws and `iIndepFun` or checked equivalent | expected candidate premise only |
| changing coordinate `i` | pointwise, essential, or support-restricted scope absent | `Function.update` or an exact tuple-agreement relation | open |
| constants `c_i` | sign, strictness, variability, and width convention absent | finite nonnegative family and squared finite sum | open |
| concentration | centering, event direction, and threshold absent | expectation/integrability, measurable event, probability coercion | open |
| exponential rate | no coefficient or denominator supplied | `Real.exp` expression such as `-2*t^2 / sum c_i^2` | familiar candidate, not selected |
| lower/two-sided forms | not mentioned | checked negation/union transports and any factor `2` | descendants or alternatives, open |
| `已验证` | untrusted inventory metadata | accepted source and kernel receipts | no H or M credit |

## Pinned Lean boundary

At the pinned mathlib revision, the intake probe elaborates adjacent declarations including
`ProbabilityTheory.iIndepFun`, `MeasureTheory.Measure.real`, `MeasureTheory.integral`,
`Function.update`, `Finset.sum`, and `Real.exp`. Module
`Mathlib.Probability.Moments.SubGaussian` provides Hoeffding and Azuma-Hoeffding machinery, but a
bounded exact-topic search found no `McDiarmid` or function-level bounded-difference concentration
declaration. Repo-local `S1_M_274.lean` explicitly says its centered-sum Hoeffding wrapper is not an
Azuma/McDiarmid process theorem and lists McDiarmid among absent search terms.

The probe and search do not establish a global absence result, exact statement, or proof. They
support `M4` at intake: no usable exact artifact has been located for the unfrozen root.

## Source gate and retry condition

Before `H0`, an accountable source reviewer must admit an immutable full edition, select one exact
result, map every incorporated definition, ordered binder, independence premise, coordinate-change
condition, constant, event, conclusion, proof node, and boundary case, audit corrections and errata,
and sign the crosswalk. Before statement acceptance, the exact source-mapped Lean expression must
elaborate under minimal pinned imports and pass removed-hypothesis, changed-domain, binder-scope,
and boundary mutations. Until then, the canonical mathematical and Lean targets remain null.
