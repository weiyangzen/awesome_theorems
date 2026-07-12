import Statement

/-!
# THM-M-0324 obligation composition interfaces

This file checks only the two logical composition boundaries selected by the
frozen obligation architecture. It neither constructs Enflo's space nor
asserts an approximation-property theorem.
-/

namespace Stage1Instances.THM_M_0324

universe u

/-- If every Schauder basis would imply a property which the space does not
have, then the space has no Schauder basis. The future proof phase must supply
the exact approximation-property predicate and both premises. -/
theorem noBasis_of_basis_implies_property (X : RealBanachSpace.{u}) (P : Prop)
    (property_fails : ¬ P)
    (basis_implies_property : Nonempty (SchauderBasis Real X.carrier) → P) :
    ¬ Nonempty (SchauderBasis Real X.carrier) := by
  intro basis
  exact property_fails (basis_implies_property basis)

/-- Checked final constructor for the canonical existential target. All four
substantive witness fields remain separately registered proof obligations. -/
theorem root_of_witness (X : RealBanachSpace.{u})
    (infiniteDimensional : ¬ FiniteDimensional Real X.carrier)
    (separable : TopologicalSpace.SeparableSpace X.carrier)
    (noSchauderBasis : ¬ Nonempty (SchauderBasis Real X.carrier)) :
    EnfloNoSchauderBasisTarget.{u} := by
  exact ⟨X, infiniteDimensional, separable, noSchauderBasis⟩

#print axioms noBasis_of_basis_implies_property
#print axioms root_of_witness

end Stage1Instances.THM_M_0324
