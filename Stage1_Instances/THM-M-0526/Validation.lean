import «Stage1_Instances».«THM-M-0526».Statement
import Mathlib.Topology.Subpath
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0526 same-worker differential validation

This module imports neither `Proof` nor `ObligationTree`. It separately
reconstructs the two proof bodies currently claimed by the proof receipt: the
inclusion-square calculation and the subordinate path subdivision. It does not
construct either universal-property package or prove the canonical root.
-/

namespace Stage1Instances.THM_M_0526.Validation

open Set
open scoped unitInterval

universe u

noncomputable section

variable {X : Type u} [TopologicalSpace X]

/-- Differential reconstruction of the inclusion-square calculation, stated
directly rather than through the obligation-tree alias. -/
theorem independentlyReconstructedSquare (U V : Set X) (x0 : X)
    (hxU : x0 ∈ U) (hxV : x0 ∈ V) :
    let hxW : x0 ∈ U ∩ V := ⟨hxU, hxV⟩
    let iWU := fundamentalGroupSubspaceMap (X := X) inter_subset_left x0 hxW
    let iWV := fundamentalGroupSubspaceMap (X := X) inter_subset_right x0 hxW
    let iUX := fundamentalGroupAmbientMap U x0 hxU
    let iVX := fundamentalGroupAmbientMap V x0 hxV
    iUX.comp iWU = iVX.comp iWV := by
  change (FundamentalGroup.map (ambientInclusion U) _).comp
      (FundamentalGroup.map (subspaceInclusion inter_subset_left) _) =
    (FundamentalGroup.map (ambientInclusion V) _).comp
      (FundamentalGroup.map (subspaceInclusion inter_subset_right) _)
  ext p
  rcases p with ⟨p⟩
  rfl

/-- Differential reconstruction of the compactness/subdivision body. -/
theorem independentlyReconstructedSubdivision {x y : X} (U V : Set X)
    (hU : IsOpen U) (hV : IsOpen V) (hcover : U ∪ V = univ)
    (p : Path x y) :
    ∃ t : ℕ → unitInterval, t 0 = 0 ∧ Monotone t ∧
      (∃ m, ∀ n ≥ m, t n = 1) ∧
      ∀ n, ∃ useU : Bool,
        range (p.subpath (t n) (t (n + 1))) ⊆ if useU then U else V := by
  let cover : Bool → Set unitInterval := fun useU => p ⁻¹' if useU then U else V
  have coverOpen : ∀ useU, IsOpen (cover useU) := by
    intro useU
    cases useU
    · exact hV.preimage p.continuous
    · exact hU.preimage p.continuous
  have coverAll : univ ⊆ ⋃ useU, cover useU := by
    intro s _
    have hs : p s ∈ U ∪ V := by
      rw [hcover]
      exact mem_univ _
    rcases hs with hsU | hsV
    · exact mem_iUnion.mpr ⟨true, by simpa [cover] using hsU⟩
    · exact mem_iUnion.mpr ⟨false, by simpa [cover] using hsV⟩
  obtain ⟨t, ht0, htMono, htOne, htSub⟩ :=
    exists_monotone_Icc_subset_open_cover_unitInterval coverOpen coverAll
  refine ⟨t, ht0, htMono, htOne, fun n => ?_⟩
  obtain ⟨useU, hSub⟩ := htSub n
  refine ⟨useU, ?_⟩
  rw [Path.range_subpath_of_le p _ _ (htMono n.le_succ)]
  rintro _ ⟨s, hs, rfl⟩
  exact hSub hs

end

assert_no_sorry independentlyReconstructedSquare
assert_no_sorry independentlyReconstructedSubdivision
#print sorries independentlyReconstructedSquare
#print sorries independentlyReconstructedSubdivision
#print axioms independentlyReconstructedSquare
#print axioms independentlyReconstructedSubdivision

end Stage1Instances.THM_M_0526.Validation
