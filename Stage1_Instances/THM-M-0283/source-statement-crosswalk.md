# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md:2034-2039` records only:

- title: `马尔可夫不等式`;
- attribution: Andrey Markov;
- year: 1889;
- gloss: `非负随机变量的概率上界`;
- importance: high;
- untrusted formalization label: `已验证`.

The identical record occurs at lines 7252-7257 in the probability section. Repository generation
deduplicates it and retains the earlier real-analysis record, so the manifest category remains
`分析学 / 实分析`. All twelve catalogue lines originate in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. No bibliography, URL, formula, theorem locator, or proof
locator is supplied. `Docs/Stage0_Blueprint.md:7819-7844` repeats the metadata while leaving exact
definitions, premises, equivalent forms, axioms, machine status, and artifact links open. These
records establish catalogue identity only.

## Human-source status

The repository records no primary source for the claimed 1889 attribution and no independently
reviewed modern authoritative statement. This intake does not invent one. The catalogue identifies
the result as a proved standard theorem family, so intake conservatively records provisional `H1`
source-reconstruction debt rather than H0 proof credit. An H0 crosswalk requires an immutable
edition, exact theorem/page, full assumptions and proof boundary, correction and errata audit,
source-to-node mapping, and independent review.

## Clause crosswalk

| Repository phrase or candidate clause | Human-source status | Pinned Lean candidate | Intake decision |
|---|---|---|---|
| "random variable" | sample space, sigma-algebra, measure, and codomain absent | arbitrary measurable type, `Measure alpha`, `f : alpha -> ENNReal` or `Real` | open; do not substitute |
| "nonnegative" | pointwise versus almost-everywhere absent | encoded by `ENNReal`, or explicit `0 <= f` almost everywhere for `Real` | candidate choices only |
| "probability" | probability measure versus general measure absent | general `Measure alpha`; no probability typeclass in the basic candidates | source mapping open |
| upper-tail event | threshold and strictness absent | `{x | epsilon <= f x}` | candidate only |
| expectation/integral | codomain, integrability, and finiteness absent | `lintegral` in `ENNReal`, or Bochner integral in `Real` | candidate choices only |
| upper bound | product versus division absent | product declarations plus a division declaration with nonzero/finite threshold | canonical form open |
| `已验证` | untrusted inventory metadata | no proposition or proof object | no H or M completion credit |

## Formal candidate crosswalk

The intake probe elaborates the following at the pinned revision:

| Declaration | Candidate role | Unclosed gate |
|---|---|---|
| `MeasureTheory.mul_meas_ge_le_lintegral₀` | extended-nonnegative product form under almost-everywhere measurability | source identity, canonical target serialization, transport, provenance, and trust audit |
| `MeasureTheory.mul_meas_ge_le_lintegral` | measurable extended-nonnegative product form | decision whether stronger measurability matches the source |
| `MeasureTheory.meas_ge_le_lintegral_div` | familiar extended-nonnegative division form | source threshold assumptions and boundary semantics |
| `MeasureTheory.mul_meas_ge_le_integral_of_nonneg` | real-valued integrable product form with almost-everywhere nonnegativity | source codomain, integrability, `mu.real`, threshold, and transport decisions |

The pinned mathlib module header states the familiar probability formula, but that documentation is
a formal-candidate description, not the missing repository source. Before H0, an accountable source
reviewer must admit and crosswalk an immutable source. Before statement acceptance, Lean work must
freeze minimal imports and an elaborated expression and pass removed-hypothesis, changed-domain,
binder-scope, and boundary mutations.
