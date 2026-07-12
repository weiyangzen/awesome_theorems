# Scope map

## Preserved theorem family

The intake preserves the local Hopf-bifurcation family named by the catalog: periodic solutions
emerge near a stationary solution as a parameter varies. A later statement phase may select an exact
root only from an immutable, independently reviewed source passage. Candidate components, none yet
credited as the theorem, include:

- a one-parameter family of autonomous vector fields and a nearby branch of equilibria;
- a finite-dimensional real phase space, a Banach space, or another source-selected state space;
- a linearization with one critical conjugate pair crossing the imaginary axis;
- source-specific simplicity, spectral-gap, nonresonance, transversality, and nonlinear
  nondegeneracy conditions;
- existence of a local branch of nonconstant periodic solutions with period converging to the
  critical linear period;
- local uniqueness modulo time translation and a precise parameter/amplitude parametrization; and
- supercritical or subcritical side, orbital stability, equilibrium stability change, or normal
  form when the selected source proves those stronger conclusions.

## Decisions required at statement freeze

1. Preserve one lawful complete source edition, select a numbered theorem or precisely delimited
   result, map its incorporated definitions and proof boundary, review corrections or errata, and
   obtain independent source approval.
2. Decide whether the root is Hopf's analytic existence/isolation theorem, a modern smooth
   finite-dimensional normal-form theorem, a Banach/PDE/delay theorem, a degenerate theorem, or an
   explicit source-defined conjunction. A theorem-family title cannot silently combine them.
3. Fix the system form, scalar field, phase space, dimension or Banach structure, parameter domain,
   vector field, equilibrium branch, solution notion, and local or global flow requirements.
4. Fix the exact regularity and analyticity assumptions in the state and parameter variables,
   including the derivatives required to define any Lyapunov coefficient.
5. State the critical spectral hypothesis: the conjugate pair, nonzero frequency, algebraic and
   geometric simplicity, multiplicity, remaining spectrum, spectral gap, Fredholm or resolvent
   assumptions, and harmonic nonresonance.
6. State the crossing condition and its orientation, and decide whether a nonzero first Lyapunov
   coefficient or another nonlinear coefficient is required.
7. Define periodicity, nonconstancy, positive or minimal period, phase equivalence, amplitude,
   parameterization, and convergence of solutions and periods to the equilibrium branch.
8. Fix the conclusion strength: existence only; one-sided occurrence; local isolation or uniqueness
   modulo phase; normal-form equivalence; stability; or supercritical/subcritical classification.
9. Freeze all ordered binders, quantifier dependencies, neighborhoods, exceptional cases, logical
   principles, and the relation of any alternate encoding to the canonical proposition.

## Degenerate and boundary cases

Source review must explicitly dispose of a zero-dimensional phase space; zero critical frequency;
multiple or nonsemisimple imaginary eigenvalues; additional center spectrum; a pair that merely
touches rather than crosses the imaginary axis; vanishing first Lyapunov coefficient; resonant
higher harmonics; a stationary or constant solution counted as periodic; zero, nonminimal, or
unbounded period; both parameter sides or neither side containing cycles; multiple nearby cycle
branches; loss of local uniqueness under time translation; a nonisolated equilibrium branch;
insufficient vector-field regularity; and local solutions that leave the selected neighborhood.

Degenerate Hopf theorems can yield no nearby periodic solutions or a different branch pattern. They
cannot be imported into a generic theorem without a checked case split and source mapping.

## Neighbor and substitution exclusions

- `THM-M-1358` bifurcation theory is a broader subject entry and supplies no exact Hopf theorem.
- `THM-M-1359`, `THM-M-1361`, and `THM-M-1362` own saddle-node, transcritical, and pitchfork
  bifurcations. Their scalar normal forms and evidence cannot replace a complex-eigenvalue crossing.
- The Neimark-Sacker bifurcation for an iterated map is a discrete-time analogue, not the
  continuous-time ODE theorem named by this catalog category unless a source explicitly selects it.
- A particular Lienard, van der Pol, or complex scalar normal-form example establishes only that
  example, not the source-selected general theorem.
- A structure storing a periodic branch, spectral crossing, normal form, or stability conclusion as
  a field is not a proof of its existence.
- Numerical continuation, plotted phase portraits, sampled eigenvalues, floating-point Lyapunov
  coefficients, and simulations provide no theorem credit without a verified certificate covering
  the exact target.
- Generic ODE, flow, periodicity, differentiability, eigenvalue, and spectrum APIs are substrate,
  not a Hopf theorem.
- The repository's `verified` label and this intake probe supply no source-fidelity or machine-proof
  evidence.

## Formal boundary

Pinned mathlib exposes integral-curve and flow interfaces, smoothness and Frechet derivatives,
function periodicity, and finite-dimensional eigenvalue and general spectrum predicates. The probe
authenticates only these adjacent interfaces. It does not define the source-selected equilibrium
branch, periodic-orbit quotient, spectral crossing, Lyapunov coefficient, center-manifold reduction,
normal form, or bifurcation conclusion. No canonical Lean target, expression fingerprint, checked
transport, mutation suite, or proof body is claimed at intake.
