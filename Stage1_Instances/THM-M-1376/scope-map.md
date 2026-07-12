# Scope map

## Preserved theorem family

The intake preserves the Poincare recurrence family named by the catalog without replacing the
word `bounded` by a stronger mathematical contract from memory. Candidate components that a later
source-selected statement may use, but that are not credited as the theorem at intake, include:

- a measurable space, a finite measure, and a self-map preserving that measure;
- almost-everywhere infinite return to each measurable or null-measurable set;
- a second-countable topology with measurable open sets and almost-everywhere return to every
  neighborhood;
- a measure-preserving continuous flow on an invariant finite-measure carrier, specialized to a
  selected nonzero time map; and
- an ODE or Hamiltonian phase space with a finite invariant region or energy shell and a proved
  invariant measure.

## Decisions required at statement freeze

The statement phase must freeze all of the following from an approved source and duplicate-target
decision rather than from the existing `THM-M-1521` implementation:

1. The exact source edition, theorem/page, incorporated definitions, proof boundary, corrections,
   and independent review.
2. Whether the dynamics is a discrete self-map, a continuous flow, an ODE solution operator, or a
   Hamiltonian flow, including the time domain and any chosen time step.
3. The carrier, sigma-algebra, topology, measure, and whether finite total measure or only finite
   measure of an invariant subset is assumed.
4. Whether measure preservation, conservativity, boundedness, compactness, volume preservation,
   invariance of an energy shell, and completeness of the dynamics are assumptions or derived
   bridges.
5. Whether recurrence means return to the same measurable set, return to every neighborhood,
   accumulation at the initial point, or equality/approximation of a phase-space state.
6. The precise exceptional set and quantifier order: almost every point of each set, almost every
   globally recurrent point, or another source-selected formulation.
7. Whether returns are once, arbitrarily late, or infinitely often; whether iteration zero counts;
   and which filter or unbounded-time convention is used.
8. The exact ordered binders, universe and typeclass context, hypotheses, conclusion, and accepted
   logical and computational profile.

## Degenerate and boundary cases

Source review must explicitly dispose of zero and infinite measures; null and empty sets; finite
spaces and identity or periodic maps; nonmeasurable sets; a map that is only nonsingular or only
conservative; noninvertible maps; a continuous flow at time zero; incomplete trajectories; escape
from the selected region; boundary points; equilibria; and topological boundedness without a finite
invariant measure. A null-set implication may be vacuous but remains part of common formulations.

## Duplicate and substitution exclusions

- `THM-M-1521`, the mathematical-physics duplicate, remains a distinct rev-5.6 target. Its legacy
  slot, dossier, statement, proof chain, and receipts confer no scope or status here. Master review
  must decide aliasing, deduplication, or distinct specialization before evidence can be shared.
- `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_180.lean` belongs to `THM-M-1521`; its normalized
  discrete statement and finite-invariant-model wrapper are discovery inputs only.
- The stronger physics wording about almost all orbits of a bounded conservative system is not an
  exact ODE theorem until phase space, invariant measure, finiteness, flow, and time-map bridges are
  fixed and checked.
- Topological boundedness alone is not finite measure, conservativity, or recurrence.
- Generic conservativity, recurrence, measure-preservation, or iteration APIs alone provide no
  theorem credit for an unidentified root.
- A structure field or hypothesis that directly assumes the desired recurrence is not a proof.
- A finite simulation, numerical trajectory, or return observed for selected initial conditions is
  not the almost-everywhere theorem.
- The catalog's untrusted `verified` label supplies no human-source or kernel evidence.

No canonical Lean target, expression fingerprint, checked alternate encoding, discovery protocol,
obligation registry, or proof state is frozen at intake.
