import Statement

set_option autoImplicit false

/-!
# THM-M-0528 independent local validation probe

This module reconstructs the frozen root without importing `Proof`. It uses the
checked pointwise/composite transport and invokes the pinned mathlib terminal
declaration directly. This is implementation-diverse same-worker evidence, not
the distinct-runner attestation required for release.
-/

namespace Stage1Instances.THM_M_0528.Validation

universe u v w

/-- Proof-independent reconstruction of the exact frozen target. -/
theorem independentlyReconstructedCoveringLiftUniqueness :
    CoveringLiftUniquenessTarget.{u, v, w} :=
  coveringLiftUniquenessTarget_iff_pointwiseProjectionEncoding.mpr (by
    intro E X A _ _ _ _ p hp g₁ g₂ hg₁ hg₂ hproj a ha
    exact hp.eq_of_comp_eq hg₁ hg₂ (funext hproj) a ha)

#print axioms independentlyReconstructedCoveringLiftUniqueness
#print axioms IsCoveringMap.eq_of_comp_eq

end Stage1Instances.THM_M_0528.Validation
