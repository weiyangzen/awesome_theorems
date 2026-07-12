# Frozen obligation tree

Item: `S56-M-1088-OBLIGATION_TREE`  
Registry: `THM-M-1088-OBLIGATIONS-v1`

The tree freezes a finite-exhaustion route to the exact countable-index target in `Statement.lean`.
It is an architecture and execution denominator, not a proof of Borell--TIS. Every listed semantic
node is root-relevant. Source, provenance, and trust overlays are separated from proof edges and do
not earn machine-proof credit.

## M1088-ROOT

Exact `BorellTISTarget`. It depends on the checked terminal assembly, whose analytic engine remains
open. Boundary: root debt remains `[H2, M3, R4]`; no theorem closure is claimed.

## M1088-S-CONTEXT

Freeze the exact binder order, measurable space, countable nonempty index type, process, supplied
supremum representative, and positive variance proxy. Budget: 35 steps.

## M1088-S-SUPREMUM

Relate `S` pointwise to the bounded real range supremum and retain coordinate measurability plus
integrability of `S`. Budget: 55 steps.

## M1088-S-BOUNDARY

Preserve the strict event and `u >= 0`; split `u = 0` from `u > 0`. The frozen theorem excludes
`sigma2 = 0`, so a zero-variance extension is not part of this node. Budget: 45 steps.

## M1088-S-FOUNDATION

Audit classical measure theory, imports, axioms, and noncomputable integration. This release-gate
dependency cannot substitute for a mathematical premise. Budget: 40 steps.

## M1088-N-ENUMERATION

Produce a nonempty finite exhaustion of the countable index type and prove that it preserves the
canonical supremum in the limit. Budget: 90 steps.

## M1088-C-FINITE-MAX

Construct finite maxima, prove measurability and monotonicity, identify their pointwise limit with
`S`, and track finite variance suprema. Budget: 100 steps.

## M1088-L-FINITE-CONCENTRATION

Prove sharp one-sided concentration for every finite maximum. The audited LSLT theorem is only a
related design candidate and supplies no proof credit here. Budget: 100 steps.

## M1088-L-COVARIANCE

Factor the finite Gaussian vector through its covariance and control the Lipschitz constant of the
maximum by the finite variance supremum. Budget: 100 steps.

## M1088-B-POSITIVE-TAIL

For `u > 0`, transport finite concentration through the exact strict event and `ENNReal` probability
bound. Budget: 70 steps.

## M1088-B-ZERO-TAIL

Prove the `u = 0` bound directly, without dividing by zero or silently strengthening the event.
Budget: 45 steps.

## M1088-B-MERGE

Check exhaustiveness of the two tail branches and compose them into the quantified `u >= 0`
conclusion. Budget: 35 steps.

## M1088-L-MEAN-LIMIT

Show convergence of the finite-maxima expectations to the integral of `S` from the frozen
integrability hypotheses. Budget: 100 steps.

## M1088-L-PROBABILITY-LIMIT

Pass the finite strict-event inequalities to the countable supremum while preserving the sharp
variance constant. Budget: 100 steps.

## M1088-T-ENGINE

Compose enumeration, finite maxima, finite concentration, both limit arguments, and the boundary
merge into `ObligationTree.UpperTailEngine`. This is the current root cut set and remains unproved.
Budget: 100 steps.

## M1088-T-ASSEMBLE

`ObligationTree.target_of_upperTailEngine` is a checked conditional composition certificate. It
consumes an exact `UpperTailEngine` and returns the exact `BorellTISTarget`; it does not implement the
engine. Budget: 25 steps.

## M1088-X-SOURCE

Pinpoint primary theorem statements and proof transitions, including separability, variance,
strictness, and boundary conventions. Human-source overlay only. Budget: 80 steps.

## M1088-X-PROVENANCE

Resolve every terminal proof body and transitive declaration origin, deduplicating wrappers and
transports. Governance overlay only. Budget: 50 steps.

## M1088-X-TRUST

Record toolchain, kernel, automation, compiled artifacts, replay, and computation boundaries.
Release overlay only. Budget: 50 steps.
