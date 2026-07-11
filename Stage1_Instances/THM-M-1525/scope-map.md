# Scope map

## Included claim

- A complex Hilbert space and a concretely represented Hamiltonian with an explicit dense domain.
- Hypotheses sufficient for the selected evolution theorem, expected to include self-adjointness.
- An initial state satisfying the required domain/regularity conditions.
- A real-time wavefunction satisfying the time-dependent equation `i dpsi/dt = H psi` and the
  initial condition, with constants/units fixed explicitly (the displayed form uses `hbar = 1`).
- Uniqueness, unitarity, norm conservation, or energy conservation only when supplied by the exact
  selected source theorem and its hypotheses.

## Statement-phase decisions

The next phase must choose between the original equation as a law and a rigorous well-posedness or
Stone-theorem consequence that is actually theorem-shaped. It must freeze bounded versus unbounded
operators, the Hamiltonian domain and its invariance, strong versus weak differentiability, the
solution regularity, time-dependent versus autonomous Hamiltonians, units, binder order, and all
universe/typeclass assumptions. Boundary cases such as the zero space and initial data outside the
operator domain must be handled explicitly rather than silently excluded.

## Explicit exclusions

- Experimental confirmation or the physical postulate by itself as a Lean theorem.
- Only the time-independent eigenvalue equation, a particular potential, or a finite-dimensional
  matrix model as a substitute for the selected general claim.
- A structure that contains the desired evolution or conservation facts as unconstrained fields.
- Treating a bounded continuous linear operator as an unnoticed substitute for the usual
  unbounded Hamiltonian.
- Crediting adjacent Laplacian, ODE, spectrum, or unitary APIs as terminal closure.

The statement phase may narrow to a source-faithful rigorous theorem, but may not broaden, weaken,
or replace the claim merely to obtain an easy Lean proof.
