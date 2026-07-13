# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:433-438` supplies exactly:

- title: `冯·诺依曼迹不等式`;
- attribution: John von Neumann;
- year: 1937;
- gloss: `矩阵迹的最大值不等式`;
- importance: medium;
- untrusted formalization label: `已验证`.

All six uncited lines entered the repository in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. `Docs/Stage0_Blueprint.md:1699-1724`
repeats them while explicitly leaving exact definitions and premises, proof route, dependencies,
alternate statements, axioms, machine status, and artifact links open. That projection is not an
independent mathematical source.

## Historical source lead

An unverified discovery lead encountered in later literature is a 1937 John von Neumann paper
commonly cited under the title *Some matrix-inequalities and metrization of matrix-space*. The
catalogue itself gives no paper, edition, journal, theorem number, page, quotation, or errata locator.
During this intake the worker could not authenticate the lead's full bibliographic metadata or
retrieve an immutable primary passage. Web bibliographic/search attempts were incomplete or
access-limited, so no exact formula, proof, correction status, or H0 credit is derived from the lead.

A later immutable source may restate the familiar singular-value inequality precisely, but it must
be recorded as primary or secondary, inspected at a fixed revision, and independently reviewed. A
modern restatement cannot by itself establish what the catalogue intended or which formulation the
1937 source proved.

## Clause crosswalk

| Repository/source component | Mathematical data still required | Prospective pinned Lean surface | Intake status |
|---|---|---|---|
| von Neumann trace inequality | exact primary or authoritative theorem passage and relation to the catalogue | exact target after source admission | theorem family identified only |
| matrices | scalar field, row/column types, dimensions, square/rectangular convention | `Matrix m n R` or finite-dimensional linear maps | open |
| trace pairing | multiplication order, transpose/adjoint convention, result scalar | `Matrix.trace`, `LinearMap.trace` | adjacent APIs elaborate |
| maximum-value inequality | left-hand real-valued operation, direction, right-hand bound, equality/max statement | real order, norm/re, finite sums | entirely open |
| singular values | definition, ordering, multiplicity, zero padding, finite range | `LinearMap.singularValues` | adjacent definition elaborates; target mapping open |
| 1937 / John von Neumann | immutable source identity, theorem/page, definitions, proof boundary, corrections/errata | not applicable | plausible historical lead, not admitted H0 evidence |
| `已验证` | exact immutable formal project, module, declaration, body, toolchain and receipt | none supplied | untrusted; no proof credit |

## Formal discovery boundary

The discovery-only probe imports pinned matrix trace, inner-product trace, and singular-value modules.
It checks concrete APIs needed by a possible future encoding. A bounded case-insensitive search over
pinned mathlib found no occurrence combining trace with `singularValues` and no relevant von Neumann
trace declaration. The repo-local legacy file `S1_M_058.lean` belongs to `THM-M-0430`, so its checked
Langlands metadata is not a candidate and gives this target no status.

This bounded result does not assert that no Lean 4 formalization exists in mathlib under different
terminology or in external projects. The later anchor audit must precommit search terms and cutoffs,
inspect exact types and proof-body provenance, and pin/import/check any credible candidate.

## Required source admission

Before the statement node can close, an accountable source review must preserve an immutable source,
pinpoint the exact theorem and definitions, map every binder, premise, convention, conclusion,
boundary case, proof boundary, correction, and erratum, and reconcile the source with the catalogue
gloss. The Lean statement phase must then elaborate exactly that claim with minimal pinned imports,
serialize the expression and environment fingerprints, compile checked transports for credited
variants, and run all required statement mutations. Until then the canonical statement remains null
and the root remains below H0.
