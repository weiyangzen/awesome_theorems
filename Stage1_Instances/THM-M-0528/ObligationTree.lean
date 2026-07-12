import Statement

set_option autoImplicit false

namespace Stage1Instances.THM_M_0528

universe u v w

/-!
# THM-M-0528 conditional obligation composition

The imported terminal theorem is deliberately an explicit premise here. This
checks the child-to-root composition without installing the proof-phase wrapper
or claiming that the premise has been accepted.
-/

/-- Exact pointwise form expected from the audited mathlib terminal body. -/
abbrev ExactPointwiseAnchor : Prop :=
  PointwiseProjectionEncoding.{u, v, w}

/-- Checked composition of the exact pointwise anchor into the canonical root. -/
theorem root_of_exactPointwiseAnchor
    (anchor : ExactPointwiseAnchor.{u, v, w}) :
    CoveringLiftUniquenessTarget.{u, v, w} :=
  coveringLiftUniquenessTarget_iff_pointwiseProjectionEncoding.mpr anchor

#print axioms root_of_exactPointwiseAnchor

end Stage1Instances.THM_M_0528
