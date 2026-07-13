# THM-M-1456 source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:10630-10635` supplies exactly the title `预处理技术`, the
attribution `众多数学家`, the period `20世纪`, the gloss `加速迭代收敛的技术`, importance
"high," and status `已验证`. All six uncited lines entered the repository in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no bibliography, definition,
formula, ordered binder, hypothesis, conclusion, proof, correction record, or formal artifact.

`Docs/Stage0_Blueprint.md:39595-39621` repeats the same gloss while explicitly leaving the
background, exact definitions and premises, proof route, dependencies, equivalent formulations,
axioms, machine status, and artifact links open. The rev-5.6 manifest preserves `已验证` only as
`source_status_untrusted` and resets the target to `L0 / rework_required`.

## Authoritative specification lead

The Netlib electronic edition of Richard Barrett, Michael Berry, Tony F. Chan, James Demmel, June
Donato, Jack Dongarra, Victor Eijkhout, Roldan Pozo, Charles Romine, and Henk van der Vorst,
*Templates for the Solution of Linear Systems: Building Blocks for Iterative Methods*, second
edition, SIAM, 1994, DOI `10.1137/1.9781611971538`, was inspected at
`https://www.netlib.org/templates/templates.html` on 2026-07-13. The observed 573,161-byte HTML had
SHA-256 `006eb59144d9292245c3b0f9a65d7b60b4f08f196220ebbeecb35f66036b83a3`; its HTTP
`Last-Modified` value was 2006-08-24.

Chapter 3, Section 3.1 ("The why and how," printed page 35) says that iterative convergence depends
on spectral properties and defines a preconditioner as a matrix effecting a same-solution
transformation intended to produce more favorable spectral properties. It illustrates left
preconditioning by `M^-1 A x = M^-1 b`. Sections 3.1.1 and 3.1.2 discuss setup/application cost and
left, right, and symmetric preconditioning. This is a strong definition and scope lead, not `H0`:
the catalog does not cite it, the electronic artifact has not been independently admitted as an
immutable edition, and its chapter does not select a universal theorem that every preconditioner
accelerates every iterative method.

## Clause crosswalk

| Repository element | Possible mathematical component | Required Lean component | Intake result |
|---|---|---|---|
| `预处理技术` | an invertible transformation or auxiliary approximate solve | exact matrix/operator and left, right, split, or symmetric action | family only |
| "iterative" | a stationary, Krylov, nonlinear, eigenvalue, or optimization recurrence | one source-selected iteration and state type | absent |
| "accelerating convergence" | improvement in residual/error rate, spectral radius, condition number, iteration count, or cost | exact metric, comparator, quantifier order, and bound | absent; not universally true |
| "equivalent problem" in the inspected lead | e.g. `A x = b` iff `M^-1 A x = M^-1 b` for invertible `M` | inverse cancellation and matrix-vector identities | useful substrate, not acceleration |
| many mathematicians / twentieth century | broad historical provenance | immutable pinpoint source and correction audit | unverified metadata |
| `已验证` | catalog status | accepted human proof and kernel receipts would be required | no H or M credit |

## Non-substitution boundary

An elementary solution-equivalence lemma does not prove faster convergence. A condition-number
bound for SPD preconditioned CG would silently select CG and an SPD setting. A spectral-radius
theorem would silently select a stationary method and one iteration matrix. A Jacobi, SSOR,
incomplete-factorization, or multigrid theorem would select a particular construction. No such
choice may be made from the broad catalog wording alone.

## Source gate

Before the target can leave `H5`, accountable reviewers must redirect it to one corrected,
truth-valued proposition; preserve an immutable primary or authoritative source; freeze every
domain, binder, hypothesis, conclusion, comparison, cost convention, and boundary case; inspect the
proof boundary and errata; and justify why the proposition represents `THM-M-1456`. A second
qualified reviewer must approve the mapping. Human-proof status must then be classified afresh
rather than inherited from `已验证`.

## Lean discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, `IntakeProbe.lean`
checks adjacent interfaces for matrix inverse cancellation, matrix-vector maps, positive-definite
matrices and inverse preservation, norm bounds, and generic fixed-point limits. A bounded search
found no exact `preconditioner`, numerical `condition number`, preconditioned iteration, or
preconditioned-CG/GMRES declaration. Generic English uses of "precondition" were unrelated. This is
intake discovery only, not the downstream immutable anchor audit or a claim about all Lean projects.

The canonical module, expression, expression hash, environment fingerprint, checked transports,
and statement mutations remain null. No H0, M0, R0, audit completion, or theorem completion is
claimed.
