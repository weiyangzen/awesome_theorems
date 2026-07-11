import Statement

/-!
# THM-M-0113 proof-phase result

The frozen target is not provable: `HodgeData.isKahler` is an unconstrained
proposition, so it does not connect the geometric hypothesis to the supplied
cohomology spaces or Hodge pieces.  The countermodel below uses the
zero-dimensional compact complex manifold and gives every Hodge piece the
bottom submodule of a nontrivial cohomology space.
-/

noncomputable section

open scoped Manifold Topology

namespace Stage1Instances.THMM0113

private abbrev ZeroModel := Fin 0 -> Complex

private instance : Unique ZeroModel := inferInstance

private def counterexampleData :
    HodgeData ZeroModel ZeroModel (modelWithCornersSelf Complex ZeroModel) ZeroModel where
  isComplexManifold := inferInstance
  isKahler := True
  cohomology := fun _ => Complex
  hodgePiece := fun _ _ _ => ⊥
  conjugate := fun _ => star
  conjugate_add := by
    intro n x y
    simp
  conjugate_smul := by
    intro n z x
    simp
  conjugate_involutive := by
    intro n x
    simp

/-- The exact frozen target implies that the bottom submodule of `Complex`
is top in degree zero, which contradicts `one_ne_zero`. -/
theorem not_hodgeDecompositionTarget :
    ¬ HodgeDecompositionTarget.{0, 0, 0, 0} := by
  intro target
  have conclusion := target ZeroModel ZeroModel
    (modelWithCornersSelf Complex ZeroModel) ZeroModel counterexampleData trivial
  have spans := (conclusion 0).1.2
  have bottom_eq_top : (⊥ : Submodule Complex Complex) = ⊤ := by
    rw [iSup_eq_bot.mpr] at spans
    · exact spans
    · intro pq
      rfl
  have one_mem_bottom : (1 : Complex) ∈ (⊥ : Submodule Complex Complex) := by
    rw [bottom_eq_top]
    trivial
  have : (1 : Complex) = 0 := by
    exact (show (1 : Complex) ∈ (⊥ : Submodule Complex Complex) from one_mem_bottom)
  exact one_ne_zero this

#print not_hodgeDecompositionTarget
#print axioms not_hodgeDecompositionTarget

end Stage1Instances.THMM0113
