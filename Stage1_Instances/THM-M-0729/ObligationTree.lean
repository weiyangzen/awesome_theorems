import Statement

/-!
# THM-M-0729 conditional obligation composition

This module checks only the logical assembly selected by the frozen obligation
architecture.  Both PCP inclusions remain explicit premises; no PCP proof is
claimed here.
-/

namespace Stage1Instances.THM_M_0729

/-- The two directional conclusions required by the canonical equality. -/
def DirectionalPackage : Prop :=
  (forall language : Language, InNP language -> InPCPLogConst language) /\
  (forall language : Language, InPCPLogConst language -> InNP language)

theorem expandedTarget_of_directionalPackage (h : DirectionalPackage) :
    ExpandedTarget := by
  intro language
  exact ⟨h.1 language, h.2 language⟩

/-- Checked child-to-root assembly.  Its premise is deliberately open. -/
theorem root_of_directionalPackage (h : DirectionalPackage) : PCPTheorem := by
  exact pcpTheorem_iff_expandedTarget.mpr
    (expandedTarget_of_directionalPackage h)

#print axioms expandedTarget_of_directionalPackage
#print axioms root_of_directionalPackage

end Stage1Instances.THM_M_0729
