# THM-M-1470 source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:10728-10733` supplies exactly the title `后验误差估计`, the
attribution Ivo Babuška, the year 1971, the gloss `数值解的误差估计`, importance "high," and status
`已验证`. All six uncited lines entered the repository in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no bibliography, definition,
formula, binder, hypothesis, estimator, conclusion, proof, correction history, or formal artifact.

`Docs/Stage0_Blueprint.md:39973-39998` repeats the gloss while explicitly leaving the formal system,
foundation, background, exact definitions and premises, proof route, dependencies, equivalent
forms, axioms, machine status, and artifact links open. Its generic statements that a closed result
is believed to exist are not target-specific source or machine evidence. The rev-5.6 manifest keeps
`已验证` only as `source_status_untrusted` and resets the target to `L0 / rework_required`.

The phrase "error estimation for a numerical solution" is not truth-valued: it names neither the
error nor an asserted relationship between that error and an estimator.

## Bibliographic source lead

Crossref and Springer publisher metadata identify Ivo Babuška, *Error-bounds for finite element
method*, *Numerische Mathematik* 16(4), 322-333 (1971), DOI `10.1007/BF02165003`. The match of
author, year, title, and subject makes this a strong source lead, but not `H0`. The catalog contains
no DOI or result locator; the inspected publisher surface exposes bibliography metadata but not the
article body; and no theorem passage, incorporated definitions, assumption map, proof boundary,
erratum audit, immutable admitted copy, source-to-target selection, or independent review exists.

The paper title also does not choose which proposition on pages 322-333 should be the root. A later
source audit must inspect the primary text and must not reconstruct its claims from modern textbook
terminology.

## Clause crosswalk

| Repository element | Mathematical component to select | Prospective Lean component | Intake result |
|---|---|---|---|
| `后验` / a posteriori | information available from the computed approximation, residual, mesh, or successive iterates | explicit estimator inputs and their computability boundary | no inputs fixed |
| `误差` / error | difference from an exact solution, eigenpair, functional, or fixed point in a named norm | exact and approximate objects plus norm or goal functional | quantity and norm absent |
| `估计` / estimate | upper, lower, two-sided, asymptotic, local, or global inequality | ordered inequality, constants, oscillation, and quantifiers | direction and conclusion absent |
| numerical solution | one source-defined discretization or iterative scheme | discrete spaces, mesh or iteration data, and output relation | method and model absent |
| Babuška / 1971 | likely bibliographic pointer to the 1971 finite-element paper | immutable edition and exact theorem/page crosswalk | strong metadata lead only |
| `已验证` | untrusted inventory label | accepted source and kernel receipts | no H or M credit |

## Neighbor and variant boundary

Finite-element discretization (`THM-M-1461`), Galerkin (`THM-M-1462`), adaptive finite elements
(`THM-M-1469`), and a priori error estimation (`THM-M-1471`) are separately cataloged. Reliability,
efficiency, estimator reduction, best approximation, and convergence have different hypotheses and
conclusions. No adjacent target may select or close this root.

## Lean discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, `IntakeProbe.lean`
checks coercive-form lower bounds and solvability, Hilbert projection minimality, and the
fixed-point-specific a posteriori iterate estimate. The first group is only adjacent variational
substrate. The last declaration is explicitly a non-candidate. A bounded repo-local and
pinned-mathlib search found no source-identical finite-element a posteriori estimator theorem.
This is intake discovery, not the later exhaustive anchor audit or a global absence claim.

## Source gate

Before leaving `H5`, accountable reviewers must choose a proposition from an immutable primary or
authoritative source; map every definition, domain, binder, hypothesis, constant, estimator term,
conclusion, and boundary case; inspect proof boundaries and corrections; justify identity with the
catalog and distinction from neighbors; and independently approve the crosswalk. Human-proof status
must then be classified afresh rather than inherited from `已验证`.

The canonical module, expression, expression hash, environment fingerprint, checked transports,
and statement mutations remain null. No H0, M0, R0, audit completion, or theorem completion is
claimed.
