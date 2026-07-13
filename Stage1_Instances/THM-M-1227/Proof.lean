import Stage1_Instances.«THM-M-1227».Statement

/-!
# THM-M-1227 proof execution

This module closes only the frozen `M1227-B-ZERO` obligation. It deliberately does not assert the
general Leray-Hopf existence theorem: the five-node root cut set recorded by the frozen obligation
registry has no repo-local or pinned terminal proof body.
-/

open Filter MeasureTheory Set
open scoped Topology

namespace Stage1.THM_M_1227

/-- The identically zero velocity and gradient satisfy all six frozen solution conditions. -/
theorem zero_isLerayHopfSolution (nu : Real) :
    IsLerayHopfSolution nu (fun _ => 0) (fun _ _ => 0) (fun _ _ => 0) := by
  apply isLerayHopfSolution_compose
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

/-- The zero-datum branch produces the witnesses required by the canonical target. -/
theorem lerayHopfExistence_of_eq_zero (nu : Real) (u0 : Space -> Velocity)
    (hu0 : u0 = fun _ => 0) :
    ∃ (u : Real -> Space -> Velocity) (g : Real -> Space -> Gradient),
      IsLerayHopfSolution nu u0 u g := by
  subst u0
  exact ⟨fun _ _ => 0, fun _ _ => 0, zero_isLerayHopfSolution nu⟩

#print axioms zero_isLerayHopfSolution
#print axioms lerayHopfExistence_of_eq_zero
#print sorries zero_isLerayHopfSolution
#print sorries lerayHopfExistence_of_eq_zero

end Stage1.THM_M_1227
