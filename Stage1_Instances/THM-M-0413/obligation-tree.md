# Frozen obligation architecture

## Root and route

`THM-M-0413-ROOT` is the exact statement fingerprint frozen in `statement.json`: for every
`K : Type u` with `[Field K] [NumberField K]`, `NumberField.RingOfIntegers K` is a Dedekind domain.
The route passes through the exact number-field instance interface and the generic integral-closure
theorem. These are separate obligations because the wrapper does not relocate or duplicate the
terminal upstream proof body. The checked transport to `integralClosure Z K` is an alias surface,
not another denominator entry.

## Component packages

The generic bridge is decomposed according to the actual pinned mathlib body into domain,
Noetherian, dimension-at-most-one, and integral-closed components. `ObligationTree.lean` treats
these as hypotheses and checks that all four are consumed to construct the bridge, then checks the
two wrapper-to-root steps. This proves conditional composition only. It asserts none of the
component premises.

Noetherianity retains the trace-dual finite-span route as a high-risk package. Dimension retains
prime contraction and maximality under integral closure. Integral closedness retains transitivity
and the integral-closure universal property. A short upstream invocation does not turn any of these
major results into an unmodeled primitive.

## Prerequisites and trust

`P-BASE-Z` owns the base Dedekind facts for the integers. `P-FINITE-SEPARABLE` owns the context
obtained from `NumberField K`, including finite dimensionality, separability, and the integral
closure identification. Their exact subordinate declaration closure remains proof-phase work.

`X-TRUST` is connected by a trust edge, never a proof edge. The narrow Lean check does not establish
the full transitive declaration, compiled-artifact, tool, license, computation, or release TCB
closure.

## Freeze boundary

Registry version 1 has ten required root-relevant obligations and zero exclusions. The denominator
was chosen from the exact statement and pinned source architecture, with closure status excluded
from freeze decisions. Each unit has a substantive ledger of at most three current steps, but major
packages are explicitly recursive bridges rather than certified terminal leaves. All debt remains
`[H1, M3, R3]`; audit completion, theorem completion, and master acceptance are false.
