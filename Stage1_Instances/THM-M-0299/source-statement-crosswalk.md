# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:2146-2151` supplies the title `奇异积分有界性定理`
("singular-integral boundedness theorem"), attributes it to Alberto Calderon and Antoni Zygmund,
gives the year 1952, and states only `奇异积分的L^p有界性` ("`L^p` boundedness of singular
integrals"). Git blame places all six uncited lines in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record has no definition, domain, ordered
binders, hypotheses, conclusion strength, proof boundary, errata, or formal artifact.

`Docs/Stage0_Blueprint.md:8251-8276` repeats the gloss while expressly leaving exact definitions and
premises, proof route, dependencies, equivalent formulations, axioms, machine status, and artifact
links open. The rev-5.6 manifest retains `已验证` only as untrusted metadata and resets the target to
`L0 / rework_required`.

## Inspected bibliographic source lead

DOI/Crossref metadata identifies A. P. Calderon and A. Zygmund, "On the existence of certain
singular integrals," *Acta Mathematica* **88** (1952), 85-139,
DOI `10.1007/BF02392130`. The metadata matches the repository attribution, date, and subject, and
links to a Project Euclid record. It is a credible primary-paper lead.

The article PDF endpoint was blocked by the publisher/archive access layer in this worker
environment. Consequently no article text, exact theorem/page passage, definitions, premises,
proof nodes, or corrections were inspected. The live Crossref response is mutable bibliographic
metadata, not an immutable paper snapshot. No paper-content hash, comprehensive errata result, or
independent review is claimed. This is `H1` discovery evidence, not `H0`.

## Component crosswalk

| Catalog/source component | Mathematical detail required | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| "singular integral" | exact operator class, initial domain, off-diagonal kernel representation, truncation, and limit convention | a concrete kernel/operator definition and construction | entirely open |
| ambient variables | Euclidean or other space, dimension, scalars, measure, and a.e. conventions | measurable/normed spaces and measure parameters | generic APIs exist; choices open |
| kernel conditions | size, homogeneity, smoothness or Hormander condition, cancellation, and constants | structured predicates with quantified estimates | no target-specific API selected |
| operator premise | whether an initial `L^2` bound or another testing/cancellation premise is assumed | exact typed hypothesis or derived lemma | source choice open |
| `L^p` | exact `1 < p < infinity` range, endpoint exclusions, domain/codomain, and norm encoding | `MeasureTheory.MemLp` or `MeasureTheory.Lp` at a selected exponent | generic carrier API probed only |
| boundedness | extension existence/uniqueness, norm inequality, constant quantifiers, and dependence | `ContinuousLinearMap` or exact universally quantified inequality | conclusion shape open |
| principal value | truncated operators, convergence mode, and relation to the extension | filters/integration plus checked equivalence bridges | absent from the gloss |
| Calderon/Zygmund, 1952 | historical/source identity | node-specific source evidence, never a Lean premise | likely paper located; pinpoint mapping open |
| `已验证` | untrusted inventory status | no proposition and no proof credit | rejected as evidence |

## Neighbor crosswalk

`THM-M-0298` separately schedules the decomposition technique; `THM-M-0350` the Hilbert transform;
`THM-M-0352` Calderon-Zygmund theory broadly; `THM-M-0364` the `T(1)` `L^2` criterion;
`THM-M-0366` Cauchy-integral boundedness; and `THM-M-1171` the PDE second-derivative estimate. These
may become typed dependencies or applications only after exact statement comparison. None owns or
supplies a substitute canonical root for this ID.

## Formal boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the intake probe checks
generic measure, Bochner integral, `MemLp`, `Lp`, and continuous-linear-map interfaces. A bounded
name search found no Calderon-Zygmund, singular-integral, weak-type, Hilbert-transform,
Riesz-transform, or maximal-truncation declaration. These facts authenticate adjacent encoding
ingredients only; they are not the later immutable anchor audit or a claim of global absence.

Before `H0`, reviewers must preserve and hash the selected primary source, pinpoint the theorem and
every incorporated definition/premise/proof transition/conclusion, resolve corrections, and approve
the mapping independently. Before the statement gate, the exact operator, kernel, domain, exponent,
bound, binders, boundary cases, and alternate transports must be frozen and kernel-elaborated.
