# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:9866-9871` supplies exactly the title `Floquet定理`, Gaston
Floquet, 1883, the gloss `周期系统的基本解矩阵`, importance "high," and status `已验证`. Git
provenance places all six uncited lines in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record has no equation, bibliography,
definition, binder, hypothesis, conclusion, proof boundary, correction history, or formal artifact.

`Docs/Stage0_Blueprint.md:36804-36829` repeats those fields and explicitly leaves the formal system,
foundation, precise definitions and premises, proof route, dependencies, equivalent forms, axioms,
machine state, and artifact links open. Its generic planning statement that a closed result is
known is not evidence. The rev-5.6 manifest preserves `已验证` only as
`source_status_untrusted` and resets the target to `L0 / rework_required`.

## Literal crosswalk

| Repository element | Possible mathematical component | Required Lean component | Intake result |
|---|---|---|---|
| `Floquet定理` | one result in the classical periodic-linear-system family | one source-selected proposition, not the whole theory | recognizable family; root open |
| `周期系统` | scalar or first-order linear ODE with a positive-period coefficient | coefficient function, period, regularity, solution convention, scalar field | all choices open |
| `基本解矩阵` | normalized or arbitrary invertible solution matrix | exact matrix ODE and pointwise-unit predicate | definition and normalization absent |
| Floquet / 1883 | historical provenance | immutable edition, theorem/page, definitions, proof and errata mapping | paper identified; mapping open |
| `已验证` | untrusted inventory label | reviewed human source and kernel evidence would be required | no H or M credit |

## Inspected source leads

G. Floquet, *Sur les equations differentielles lineaires a coefficients periodiques*, *Annales
scientifiques de l'Ecole Normale Superieure*, series 2, volume 12 (1883), pages 47-88, DOI
`10.24033/asens.220`, is the identifiable historical primary paper. Numdam landing-page metadata
and Crossref metadata confirm the author, title, journal, year, volume, pages, and DOI. The catalog
does not cite it. A complete stable PDF was not acquired during intake, so no theorem/page text,
incorporated definitions, proof boundary, translation, or errata is credited as inspected primary
proof evidence.

The Encyclopedia of Mathematics entry *Floquet theory*, stable revision `46944`, was inspected as
a secondary source-family discriminator. It gives a real periodic system `x'=A(t)x` with positive
period and locally summable coefficient, then separates: (1) a representation of every fundamental
matrix as `X(t)=F(t) exp(tK)`; (2) reduction by `x=F(t)y` to a constant matrix equation; and (3)
spectral splitting and exponential dichotomy consequences. It explicitly says the factors are
generally complex and that a real factor may need period `2T` rather than `T`.

This entry is useful ambiguity evidence, not H0. It is secondary, the catalog does not select one
numbered component, its incorporated definition of fundamental matrix was not audited, and no
complete assumption-to-target mapping or independent review is accepted. Its exact raw-revision
retrieval URL and response hash are recorded in the provisional receipt; the bytes remain an
unarchived network discovery input and cannot support offline or release-grade evidence.

## Candidate source-to-Lean components

| Candidate component | Prospective pinned Lean surface | Intake assessment |
|---|---|---|
| positive period and periodic coefficient | `Function.Periodic A T` plus `0 < T` | regularity and coefficient type open |
| matrix solution of `X'=AX` | `IsIntegralCurve` or a source-specific derivative predicate | multiplication orientation and matrix norm instance open |
| fundamental matrix | a solution matrix with pointwise `IsUnit` or values in `GL` | normalization and equivalence open |
| monodromy | the value or transition matrix after one period | base time and identity orientation open |
| Floquet factor | periodic `P` and constant `B` with a matrix-exponential equality | field, period, and existence strength open |
| exponential invertibility | `Matrix.isUnit_exp` | substrate only; no logarithm or factorization theorem |

The API probe authenticates names and types only. No row is a canonical statement, checked
transport, proof body, or M0 result.

## Source and statement gate

Before leaving `H1`, accountable reviewers must select an immutable proposition and edition,
transcribe every incorporated definition, ordered binder, hypothesis, conclusion, and field/period
convention, inspect translation and errata, reconcile the `THM-M-1352`/`1354`/`1355` boundaries,
and independently approve the mapping. The statement phase must then freeze minimal imports, the
elaborated expression and environment fingerprint, checked transports, and removed-hypothesis,
changed-domain, binder-scope, and boundary mutations. None of those downstream gates is claimed by
this intake.
