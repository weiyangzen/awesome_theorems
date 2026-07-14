import «Stage1_Instances».«THM-M-0526».ObligationTree
import Mathlib.Topology.Subpath

/-!
# THM-M-0526: proof-phase implementation

This module closes `SVK-MAP-FUNCTORIALITY` and its parent `SVK-SQUARE` by
reducing both inclusion composites to the same map on path representatives.
It also implements the compactness body of `SVK-LEBESGUE-NUMBER`: every path
has a finite monotone subdivision subordinate to either member of the open
cover. The later word, homotopy-grid, and generation branches remain open;
consequently this file does not declare a proof of `SeifertVanKampenTarget`.
-/

namespace Stage1Instances.THM_M_0526

open Set
open scoped unitInterval

universe u

noncomputable section

variable {X : Type u} [TopologicalSpace X]

/-- The inclusion square commutes. After exposing a fundamental-group element
as a homotopy class, both composites map its representative to the same path
in the ambient space. -/
theorem square_commutativity_proof (U V : Set X) (x0 : X)
    (hxU : x0 ∈ U) (hxV : x0 ∈ V) :
    SquareCommutativity U V x0 hxU hxV := by
  change (FundamentalGroup.map (ambientInclusion U) _).comp
      (FundamentalGroup.map (subspaceInclusion inter_subset_left) _) =
    (FundamentalGroup.map (ambientInclusion V) _).comp
      (FundamentalGroup.map (subspaceInclusion inter_subset_right) _)
  ext p
  rcases p with ⟨p⟩
  rfl

/-- Cover-parametric package consumed by `compose_root`. None of the cover or
connectedness hypotheses is needed for functoriality of the inclusion maps. -/
theorem square_package :
    ∀ (X : Type u) [TopologicalSpace X]
      (U V : Set X) (x0 : X), IsOpen U → IsOpen V → U ∪ V = univ →
      (hxU : x0 ∈ U) → (hxV : x0 ∈ V) →
      IsPathConnected U → IsPathConnected V → IsPathConnected (U ∩ V) →
      SquareCommutativity U V x0 hxU hxV := by
  intro X _ U V x0 _ _ _ hxU hxV _ _ _
  exact square_commutativity_proof U V x0 hxU hxV

/-- A path admits a finite monotone subdivision subordinate to a two-set open
cover. The Boolean witness records whether a segment lies in `U` or `V`.

This is the compactness body frozen as `SVK-LEBESGUE-NUMBER`; the range form
is ready for the later loop-word construction. -/
theorem path_subdivision_of_two_open_cover {x y : X} (U V : Set X)
    (hU : IsOpen U) (hV : IsOpen V) (hcover : U ∪ V = univ)
    (p : Path x y) :
    ∃ t : ℕ → unitInterval, t 0 = 0 ∧ Monotone t ∧
      (∃ m, ∀ n ≥ m, t n = 1) ∧
      ∀ n, ∃ useU : Bool,
        range (p.subpath (t n) (t (n + 1))) ⊆ if useU then U else V := by
  let c : Bool → Set unitInterval := fun useU => p ⁻¹' if useU then U else V
  have hcOpen : ∀ useU, IsOpen (c useU) := by
    intro useU
    cases useU
    · exact hV.preimage p.continuous
    · exact hU.preimage p.continuous
  have hcCover : univ ⊆ ⋃ useU, c useU := by
    intro s _
    have hs : p s ∈ U ∪ V := by
      rw [hcover]
      exact mem_univ _
    rcases hs with hsU | hsV
    · exact mem_iUnion.mpr ⟨true, by simpa [c] using hsU⟩
    · exact mem_iUnion.mpr ⟨false, by simpa [c] using hsV⟩
  obtain ⟨t, ht0, htMono, htOne, htSub⟩ :=
    exists_monotone_Icc_subset_open_cover_unitInterval hcOpen hcCover
  refine ⟨t, ht0, htMono, htOne, fun n => ?_⟩
  obtain ⟨useU, hSub⟩ := htSub n
  refine ⟨useU, ?_⟩
  rw [Path.range_subpath_of_le p _ _ (htMono n.le_succ)]
  rintro _ ⟨s, hs, rfl⟩
  exact hSub hs

end

end Stage1Instances.THM_M_0526

#check Stage1Instances.THM_M_0526.square_commutativity_proof
#check Stage1Instances.THM_M_0526.square_package
#check Stage1Instances.THM_M_0526.path_subdivision_of_two_open_cover
#print axioms Stage1Instances.THM_M_0526.square_commutativity_proof
#print axioms Stage1Instances.THM_M_0526.square_package
#print axioms Stage1Instances.THM_M_0526.path_subdivision_of_two_open_cover
