# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:9880-9885` supplies exactly the title `线性系统的稳定性`, the
attribution "many mathematicians," the twentieth century, the gloss `线性系统的稳定性判据`,
importance "high," and status `已验证`. Git history places all six uncited lines in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no source, equation,
definitions, binders, hypotheses, conclusion, proof boundary, correction history, or formal
artifact.

`Docs/Stage0_Blueprint.md:36858-36883` repeats those fields while explicitly leaving the formal
system, foundation, exact definitions and premises, proof route, dependencies, equivalent forms,
axioms, machine status, and artifact links open. The rev-5.6 target manifest retains `已验证` only
as untrusted source metadata and resets this target to `L0 / rework_required`.

No primary source is cited or selected. The broad attribution and date are discovery metadata, not
a pinpoint source crosswalk. Consequently this intake makes no `H0` or historical-genealogy claim.

## Inspected source-family lead

Gerald Teschl, *Ordinary Differential Equations and Dynamical Systems*, Graduate Studies in
Mathematics 140, American Mathematical Society, 2012, is an authoritative modern source lead. The
author-hosted preliminary edition and official errata were inspected. For finite-dimensional
continuous-time autonomous systems `x' = A x`, it separates several candidate results:

- Theorem 3.4, printed page 71, classifies which initial conditions yield convergence to zero or
  bounded forward trajectories in terms of generalized eigenspaces.
- Corollary 3.5, printed page 71, characterizes bounded stability by nonpositive real parts plus
  equality of algebraic and geometric multiplicity for zero-real-part eigenvalues.
- Corollary 3.6, printed pages 71-72, characterizes asymptotic stability by strictly negative real
  parts and gives an exponential matrix-norm estimate below the spectral decay threshold.
- Theorem 9.1, printed page 254, restates bounded global stability and global asymptotic stability
  as separate clauses. Theorem 9.2 then treats stable and unstable invariant subspaces.

This source makes the ambiguity concrete: the Jordan boundary condition belongs to bounded
stability, while strict negativity belongs to asymptotic/exponential stability. It does not resolve
whether the catalog intended either result, a discrete-time analogue, a Lyapunov-matrix criterion,
or a control/semigroup theorem. The catalog does not cite Teschl, and no complete assumption/proof/
errata mapping or independent review is accepted, so this source lead remains `H1` discovery rather
than `H0` evidence.

## Component crosswalk

| Catalog component | Material alternatives | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| `线性系统` / linear system | continuous or discrete, autonomous or time-varying, homogeneous or controlled, matrix or semigroup | matrix action, `IsIntegralCurve`, iterates, fundamental matrix, or a future semigroup encoding | dynamics and carrier open |
| `稳定性` / stability | bounded/Lyapunov, asymptotic, exponential, uniform, BIBO, input-to-state | quantified norm, neighborhood, limit, or input-output predicate | exact predicate and quantifier order open |
| `判据` / criterion | eigenvalue/Jordan, spectral radius, matrix exponential, Lyapunov equation, coefficient or frequency test | `Module.End.HasEigenvalue`, `spectrum`, `NormedSpace.exp`, positive-definite matrices, future control APIs | criterion and implication direction open |
| boundary spectrum | imaginary axis, zero real part, unit circle, continuous spectrum | generalized eigenspaces, semisimplicity, complexification, spectrum | proposition-changing boundary absent |
| `已验证` | untrusted inventory label | no proposition or proof object | no H or M credit |

## Lean and target boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the discovery-only
probe checks matrix exponential, diagonal and conjugation identities, invertibility of the
exponential, finite-dimensional eigenvalue/spectrum equivalence, and generic integral-curve APIs.
A bounded case-insensitive search over pinned mathlib and repository-local Lean found no declaration
named as a linear-system stability, Hurwitz-stability, asymptotic-stability, or exponential-
stability theorem. The matrix-exponential file itself does not supply long-time decay or a spectral
stability classification. These observations are not the later immutable external anchor audit and
do not establish global absence.

Neighbor dossiers correctly treat this target only as a distinct boundary: `THM-M-1342` is general
Lyapunov stability theory, and `THM-M-1344` is nonlinear transfer from a linearization. The nearby
Routh-Hurwitz, Nyquist, and Floquet catalog entries are separate targets and supply no statement or
proof credit here.

Before statement work, accountable reviewers must preserve an immutable source, select one exact
truth-valued root, transcribe its incorporated definitions, ordered binders, hypotheses, conclusion,
proof boundary, and corrections, reconcile neighbor ownership, and independently approve the
crosswalk. Only then may the statement phase freeze minimal imports, the elaborated expression and
environment fingerprints, checked transports, and removed-hypothesis, changed-domain, changed-
binder-scope, and boundary mutations.
