import Stage1_Instances.«THM-M-1227».Statement

/-!
# THM-M-1227 differential validation probes

These declarations reconstruct the zero-data branch directly from the frozen statement surface.
They deliberately import neither `Proof` nor another validation module. They do not assert the
general Leray-Hopf existence target.
-/

open Filter MeasureTheory Set
open scoped Topology

namespace Stage1.THM_M_1227.Validation

open Stage1.THM_M_1227

/-- A direct reconstruction of all six frozen solution conditions for zero velocity and gradient. -/
theorem zero_isLerayHopfSolution_direct (nu : Real) :
    IsLerayHopfSolution nu (fun _ => 0) (fun _ _ => 0) (fun _ _ => 0) := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩
  · simp [IsWeakGradient]
  · change ∀ᵐ _t ∂(volume.restrict (Ici (0 : Real))),
      Integrable (fun _x : Space => ∑ i, (0 : Velocity) i * (0 : Velocity) i) ∧
      Integrable (fun _x : Space => ∑ i, ∑ j, (0 : Gradient) i j * (0 : Gradient) i j)
    simp
  · simp
  · intro phi _
    simp
    change 0 = ∫ x : Space, ∑ i, (0 : Velocity) i * phi 0 x i
    simp
  · change Tendsto
      (fun _t : Real => ∫ _x : Space,
        ∑ i, (((0 : Velocity) - 0) i) * (((0 : Velocity) - 0) i))
      (nhdsWithin 0 (Ioi 0)) (nhds 0)
    simp
  · intro t _
    change
      (∫ _x : Space, ∑ i, (0 : Velocity) i * (0 : Velocity) i) +
          2 * nu * ∫ _s in Set.Icc (0 : Real) t,
            ∫ _x : Space, ∑ i, ∑ j, (0 : Gradient) i j * (0 : Gradient) i j ≤
        ∫ _x : Space, ∑ i, (0 : Velocity) i * (0 : Velocity) i
    simp

/-- Direct existential packaging of the independently reconstructed zero-data solution. -/
theorem lerayHopfExistence_of_eq_zero_direct (nu : Real) (u0 : Space -> Velocity)
    (hu0 : u0 = fun _ => 0) :
    ∃ (u : Real -> Space -> Velocity) (g : Real -> Space -> Gradient),
      IsLerayHopfSolution nu u0 u g := by
  subst u0
  exact ⟨fun _ _ => 0, fun _ _ => 0, zero_isLerayHopfSolution_direct nu⟩

#print sorries zero_isLerayHopfSolution_direct
#print axioms zero_isLerayHopfSolution_direct
#print sorries lerayHopfExistence_of_eq_zero_direct
#print axioms lerayHopfExistence_of_eq_zero_direct

end Stage1.THM_M_1227.Validation
