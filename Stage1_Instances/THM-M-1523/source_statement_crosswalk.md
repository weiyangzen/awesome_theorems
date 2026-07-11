# Source-statement crosswalk

| Claim component | Available source anchor | Lean target | Intake assessment |
|---|---|---|---|
| Catalogue item | `Docs/Stage1_Blueprint.md`, `THM-M-1523`: `量子力学的数学基础` | none frozen | A subject heading, not an exact theorem |
| Supplied content | Same entry: `希尔伯特空间形式` | complex Hilbert-space APIs are a future discovery surface | Names a formalism but supplies no binders, hypotheses, conclusion, or boundary cases |
| Suggested object model | Same entry mentions analysis, linear operators, Hilbert spaces, measure theory, and PDE/geometry interfaces | modules/declarations not yet audited | Repository-generated discovery guidance, not a primary mathematical source and not machine evidence |
| Suggested architecture | axiomatic model -> spaces/operators -> spectral or variational structure -> estimate -> wrapper | no canonical root | Architecture seed only; it cannot determine which theorem is meant |

## Source boundary

The title closely resembles John von Neumann's *Mathematical Foundations of Quantum Mechanics*, but
title resemblance is not enough to select a particular edition, theorem, page, assumptions, or
errata record. Consequently it is recorded only as a discovery lead, not an accepted source anchor.
No primary-source proposition can presently be crosswalked to a Lean expression without inventing
missing mathematics.

The next phase may proceed only after recording an exact primary-source theorem (edition,
theorem/page, assumptions, and errata) or an explicitly approved axiom-to-consequence claim. It must
then freeze the complex/real scalar choice, Hilbert-space universes, operator boundedness and domain,
self-adjointness or normality hypotheses, quantifier order, degenerate cases, and conclusion. A
spectral theorem, uncertainty inequality, or variational lemma must not be adopted merely because
mathlib can express it.

No `H0` or exact-statement claim is made. The legacy `已验证` label is untrusted metadata and gives no
source or proof credit.
