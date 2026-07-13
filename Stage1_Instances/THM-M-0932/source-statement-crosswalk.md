# Source-statement crosswalk

## Repository record and provenance

`Docs/researches/math_theorems.md:6812-6817` supplies exactly the title `零和序列`, attribution
`众多数学家`, period `20世纪`, gloss `零和问题的理论`, importance `高`, and status `已验证`. All six
uncited lines entered the repository in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no bibliography, stable source
identifier, definition, formula, theorem number, proof boundary, correction history, or formal
artifact.

`Docs/Stage0_Blueprint.md:25417-25442` mechanically expands the same record. It explicitly leaves the
target formal system, precise definitions and premises, proof route, dependent lemmas, equivalent
forms, axioms, machine state, and artifact links as `待补充`. The rev-5.6 manifest retains `已验证`
only as `source_status_untrusted`, assigns rank 1471 and the uniform `L0 / rework_required`
baseline, and records `theorem_complete=false`.

## Literal crosswalk

| Repository element | Possible mathematical component | Required Lean component | Intake result |
|---|---|---|---|
| `零和序列` | the subject of zero-sum sequences, usually over additive groups | one exact proposition over a fixed carrier and sequence encoding | subject identified; proposition open |
| `零和问题的理论` | definitions, threshold invariants, existence, structure, inverse, or factorization results | exact ordered binders, hypotheses, conclusion, and relationships among encodings | no result is selected |
| `众多数学家`, `20世纪` | broad historical attribution | immutable edition and theorem/section/page with source-to-node mapping | no source credit |
| `已验证` | untrusted inventory metadata | reviewed human proof and kernel evidence would be required | no H or M credit |

## Subject-reference lead

Crossref and Elsevier core metadata identify Weidong Gao and Alfred Geroldinger, *Zero-sum
problems in finite abelian groups: A survey*, *Expositiones Mathematicae* 24(4) (2006), 337-369,
DOI `10.1016/j.exmath.2006.07.002`. The Crossref metadata snapshot observed on 2026-07-13 has
SHA-256 `f383dfee0285612b49507db975e8c7ced1ba35493b2a24e14519c8ee8633b14a`; the Elsevier
core-data response has SHA-256
`b108aecb28d9255bcd1a67542749733f8fb6c9742f6881fb9f2a80ca9f5ae3e1`.

The title is strong evidence that the catalog wording names a broad subject rather than one
theorem. It does not select a root: the repository does not cite this survey, no complete text or
pinpoint proposition was admitted, and no source definitions, proof boundary, correction map, or
independent review was accepted. Bibliographic metadata supplies no H0 evidence.

## Missing source-to-statement map

An accepted crosswalk would have to select one immutable source proposition and map every
incorporated definition, premise, binder, conclusion, proof boundary, correction, and boundary
case. The repository currently does not decide:

- the carrier class, such as a finite abelian group, cyclic group, arbitrary additive commutative
  group, or monoid;
- whether a sequence is a list, multiset, free abelian monoid element, or indexed finite family;
- whether the empty sequence is zero-sum and whether a requested subsequence must be nonempty or
  proper;
- whether repetitions are allowed and what the subsequence relation preserves;
- whether the root concerns arbitrary zero-sum subsequences, prescribed lengths, minimality,
  zero-sum-freeness, an optimal invariant, inverse structure, or factorization; or
- the exact quantifier order, threshold, equality/inequality orientation, optimality clause, and
  trivial-group or small-parameter conventions.

The provisional human-source classification is therefore `H5`: the received topic wording is not
yet a stable truth-valued proposition. This classifies the repository target, not the truth or
human-proof status of standard zero-sum theorems.

## Pinned Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.Combinatorics.Additive.ErdosGinzburgZiv` proves
`Int.erdos_ginzburg_ziv`, `ZMod.erdos_ginzburg_ziv`, and multiset versions. Those declarations
state the specific EGZ theorem cataloged separately as `THM-M-0931`. They do not select or prove a
generic "theory of zero-sum problems" root. A bounded exact-topic query found no declaration named
for zero-sum sequences, a Davenport constant, or an Olson constant in repo-local Lean or pinned
mathlib. That observation is intake discovery, not an exhaustive external anchor audit or a global
absence claim.

`IntakeProbe.lean` authenticates multiset cardinality/sum interfaces and the adjacent EGZ
declarations without defining a target or receiving proof credit. Before the statement phase can
begin, accountable reviewers must select and preserve an exact proposition, reconcile neighboring
ownership, audit source fidelity and corrections, and independently approve this crosswalk.
