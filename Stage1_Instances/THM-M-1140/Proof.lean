import ObligationTree

/-!
# THM-M-1140 proof execution

This module closes the connected-topological propagation package from the
frozen obligation tree. The analytic local-rigidity package is not asserted:
the pinned dependency closure has no arbitrary-dimensional mean-value or
strong-maximum theorem from which to construct it.
-/

open Set
open InnerProductSpace

namespace Stage1Instances.THM_M_1140

/-- A nonempty locally constant level set is all of a connected domain. -/
theorem connectedLevelPropagation : ConnectedLevelPropagation := by
  intro n Omega u c hne hopen hconn hcont hexists hlocal
  let level : Set Omega := {x | u x = c}
  have hlevelClosed : IsClosed level := by
    change IsClosed {x : Omega | (Omega.restrict u) x = (fun _ => c) x}
    exact isClosed_eq hcont.restrict continuous_const
  have hlevelOpen : IsOpen level := by
    rw [isOpen_iff_mem_nhds]
    intro y hy
    obtain ⟨V, hVopen, hyV, hVOmega, hVeq⟩ :=
      hlocal y y.property hy
    filter_upwards [hVopen.preimage_val.mem_nhds hyV] with z hz
    exact hVeq z hz
  letI : PreconnectedSpace Omega := Subtype.preconnectedSpace hconn.isPreconnected
  have hlevelNonempty : level.Nonempty := by
    obtain ⟨y, hy, hyc⟩ := hexists
    exact ⟨⟨y, hy⟩, hyc⟩
  have hlevel : level = univ := IsClopen.eq_univ ⟨hlevelClosed, hlevelOpen⟩ hlevelNonempty
  intro x hx
  have hxlevel : (⟨x, hx⟩ : Omega) ∈ level := hlevel.symm.subset (mem_univ _)
  exact hxlevel

#print axioms connectedLevelPropagation

end Stage1Instances.THM_M_1140
