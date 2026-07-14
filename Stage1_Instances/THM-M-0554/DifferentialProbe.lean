import Mathlib.Algebra.Homology.SpectralSequence.Basic

namespace Stage1.THM_M_0554

/-- Diagnostic for the literal bidegree field; not a frozen-node composition. -/
theorem differentialBidegreeProbe (r p q : ℤ) (_hr : 2 ≤ r) :
    (ComplexShape.up' (⟨r, 1 - r⟩ : ℤ × ℤ)).Rel
      (p, q) (p + r, q + (1 - r)) := by
  rfl

#print axioms differentialBidegreeProbe

end Stage1.THM_M_0554
