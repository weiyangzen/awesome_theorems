# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records the functional-analysis entry `谱定理`, attributes it to
David Hilbert and John von Neumann, dates it to 1932, and gives only `正规算子的谱分解`
("spectral decomposition of normal operators"). Stage0 repeats this metadata. The rev-5.6 manifest
preserves `已验证` only as `source_status_untrusted`. No definition, theorem hypotheses, proof
source, edition, theorem/page locator, or formal artifact is supplied.

The same research inventory also contains a different matrix spectral-theorem record, saying normal
matrices are unitarily diagonalizable, and a neighboring compact-operator spectral theorem. Those
records show why the functional-analysis wording must not silently collapse to a finite-dimensional
or compact specialization.

## Candidate source work

An authoritative functional-analysis or operator-theory edition must be selected during the source
audit. The audit must pinpoint the theorem and pages, record whether it treats bounded or unbounded
normal operators, transcribe all Hilbert-space and measure hypotheses, identify the exact
representation and uniqueness statement, check errata, and obtain independent review. No such
source is accepted in this intake, so the current human status is `H3`, not `H0`.

## Crosswalk

| Repository phrase | Possible mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "operator" | bounded operator on a complex Hilbert space | a continuous linear map and its adjoint | pinned API probed; exact domain open |
| "normal" | `T*T = TT*` | `IsStarNormal` on the operator algebra | pinned predicate probed; encoding open |
| "spectral decomposition" | projection-valued measure and operator integral | PVM, support, integration, operator equality | not source-selected; API audit open |
| "spectral decomposition" | multiplication-operator representation | measure space, `L2`, unitary equivalence | not source-selected; API audit open |
| "spectral decomposition" | continuous functional calculus | `ContinuousFunctionalCalculus`, `cfcHom` | candidate API probed; not equivalent by fiat |
| `已验证` | untrusted inventory label | no Lean proposition or proof credit | explicitly rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded intake
probe imports adjoint and continuous-functional-calculus modules and checks six relevant interfaces.
This establishes encoding ingredients only. Mathlib also contains finite-dimensional Hermitian
matrix and symmetric-linear-map spectral theorems, but they do not close this normal-operator target
without a checked source relationship. Formal candidate discovery and provenance remain the later
anchor-audit phase.
