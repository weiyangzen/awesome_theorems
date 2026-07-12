# THM-M-1003 obligation tree

This version freezes 16 canonical obligations before proof status is counted. The exact root
remains open. The proof graph separates the already-audited partial mathlib anchors from the
substantive same-exponent conditional-expectation route.

## M1003-ROOT

The exact target in `Statement.lean`; it requires the checked terminal composition.

## M1003-S-DEFINITIONS

The finite-measure, Nat-indexed, real-valued martingale data, strict exponent, and common-limit
predicate. This is statement infrastructure, not convergence evidence.

## M1003-S-BOUNDARY

The strict endpoint exclusions are kernel-checked. Zero measure and arbitrary measurable spaces
remain admitted, while p=1, p=infinity, continuous time, and Banach-valued variants remain outside.

## M1003-S-FOUNDATION

The transitive axiom, import, TCB, and no-oracle audit is a release obligation and remains open.

## M1003-N-L1-BOUND

Derive the uniform L1 bound required by the pinned a.e.-limit theorem from the original uniform
Lp bound, strict exponent, and finite measure. A theorem name alone cannot close this reduction.

## M1003-B-ENDPOINTS

Make the strict exponent and degenerate branches exhaustive; no endpoint theorem may be smuggled
into the root.

## M1003-C-LIMIT

Select `Filtration.limitProcess` as the candidate and discharge its representation and
measurability conventions.

## M1003-L-AE-LIMIT

Use `Submartingale.ae_tendsto_limitProcess` only after the exact L1 premise has been constructed.

## M1003-L-LIMIT-MEMLP

Use `Submartingale.memLp_limitProcess` at the original exponent and uniform bound.

## M1003-L-COND-REP

Establish that each process value is the conditional expectation of the selected terminal limit.
This central bridge has no audited terminal declaration in the pinned environment.

## M1003-L-COND-APPROX

Prove that conditional expectations along the increasing filtration converge in Lp to the
terminal MemLp variable for 1<p<infinity. This is the central same-exponent approximation engine.

## M1003-T-CANDIDATE

Combine a.e. convergence and limit `MemLp` for one selected candidate.

## M1003-T-SAME-EXPONENT

Compose conditional representation and approximation into convergence of the eLpNorm difference
at the input exponent.

## M1003-T-ASSEMBLE

`root_of_limit_packages` is a kernel-checked composition certificate. It consumes both terminal
packages and yields the full exact root; it is conditional and supplies no proof of either input.

## M1003-X-SOURCE

Primary-source edition, theorem/page, assumptions, convention, and errata mapping remains required.

## M1003-X-PROVENANCE

Terminal proof-body, wrapper, import, axiom, TCB, and replay provenance is informational for proof
coverage but mandatory at release.

## Closure boundary

The remaining root cut set is `M1003-T-CANDIDATE` plus `M1003-T-SAME-EXPONENT`. The registry freeze
does not claim proof closure, H0 source fidelity, R0 reconstruction, validation, or theorem completion.
