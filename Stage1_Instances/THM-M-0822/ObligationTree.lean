import Statement
import Mathlib.Combinatorics.SetFamily.KruskalKatona

/-!
# THM-M-0822 conditional obligation composition

This module checks the exact child-to-parent interfaces frozen by registry
version 1. The target-owned star branch and the pinned mathlib upper-bound
terminal are kept as explicit packages. Their concrete implementations are
checked below, but this phase does not install or accept them as proof state.
-/

namespace Stage1Instances.THM_M_0822.ObligationTree

open Finset

/-- The attaining-family conjunct of the frozen maximum-value target. -/
def AttainmentPackage : Prop :=
  forall (n r : Nat), 1 <= r -> r <= n / 2 ->
    exists A : Finset (Finset (Fin n)),
      (A : Set (Finset (Fin n))).Intersecting /\
      (A : Set (Finset (Fin n))).Sized r /\
      A.card = (n - 1).choose (r - 1)

/-- The universal upper-bound conjunct of the frozen maximum-value target. -/
def UpperBoundPackage : Prop :=
  forall (n r : Nat), 1 <= r -> r <= n / 2 ->
    forall A : Finset (Finset (Fin n)),
      (A : Set (Finset (Fin n))).Intersecting ->
      (A : Set (Finset (Fin n))).Sized r ->
      A.card <= (n - 1).choose (r - 1)

/-- The exact proposition supplied by the pinned mathlib terminal. -/
def MathlibUpperBoundTerminal : Prop :=
  forall (n r : Nat),
    forall A : Finset (Finset (Fin n)),
      (A : Set (Finset (Fin n))).Intersecting ->
      (A : Set (Finset (Fin n))).Sized r ->
      r <= n / 2 ->
      A.card <= (n - 1).choose (r - 1)

/-- Selection of a ground element throughout the admissible range. -/
def GroundElementPackage : Prop :=
  forall (n r : Nat), 1 <= r -> r <= n / 2 -> Nonempty (Fin n)

/-- Construction of the canonical star from admissible parameters. -/
def StarConstructionPackage : Prop :=
  forall (n r : Nat), 1 <= r -> r <= n / 2 ->
    exists x : Fin n, exists A : Finset (Finset (Fin n)),
      A = Stage1Instances.THM_M_0822.erdosKoRadoStar n r x

/-- Intersection property of every canonical star. -/
def StarIntersectingPackage : Prop :=
  forall (n r : Nat) (x : Fin n),
    (Stage1Instances.THM_M_0822.erdosKoRadoStar n r x :
      Set (Finset (Fin n))).Intersecting

/-- Uniformity property of every canonical star. -/
def StarSizedPackage : Prop :=
  forall (n r : Nat) (x : Fin n),
    (Stage1Instances.THM_M_0822.erdosKoRadoStar n r x :
      Set (Finset (Fin n))).Sized r

/-- Image representation used to calculate a star's cardinality. -/
def StarImagePackage : Prop :=
  forall (n r : Nat) (x : Fin n), 1 <= r ->
    Stage1Instances.THM_M_0822.erdosKoRadoStar n r x =
      (powersetCard (r - 1) (Finset.univ.erase x)).image (insert x)

/-- Cardinality interface of every positive-rank canonical star. -/
def StarCardPackage : Prop :=
  forall (n r : Nat) (x : Fin n), 1 <= r ->
    (Stage1Instances.THM_M_0822.erdosKoRadoStar n r x).card =
      (n - 1).choose (r - 1)

/-- Checked construction composition from the ground-element child. -/
theorem starConstruction_of_groundElement
    (ground : GroundElementPackage) : StarConstructionPackage := by
  intro n r hr hhalf
  let x := Classical.choice (ground n r hr hhalf)
  exact ⟨x, Stage1Instances.THM_M_0822.erdosKoRadoStar n r x, rfl⟩

/-- Checked cardinality composition from the image child. -/
theorem starCard_of_image (image : StarImagePackage) : StarCardPackage := by
  intro n r x hr
  rw [image n r x hr, card_image_of_injOn]
  · rw [card_powersetCard, card_erase_of_mem (mem_univ x), card_univ,
      Fintype.card_fin]
  · intro a ha b hb hab
    have hxa : x ∉ a :=
      fun hx => (mem_erase.1 ((mem_powersetCard.1 ha).1 hx)).1 rfl
    have hxb : x ∉ b :=
      fun hx => (mem_erase.1 ((mem_powersetCard.1 hb).1 hx)).1 rfl
    simpa [hxa, hxb] using congrArg (erase · x) hab

/-- Checked attainment composition. Every direct mathematical child is consumed. -/
theorem attainment_of_starPackages
    (construction : StarConstructionPackage)
    (intersecting : StarIntersectingPackage)
    (sized : StarSizedPackage)
    (card : StarCardPackage) : AttainmentPackage := by
  intro n r hr hhalf
  rcases construction n r hr hhalf with ⟨x, A, hA⟩
  subst A
  exact ⟨Stage1Instances.THM_M_0822.erdosKoRadoStar n r x,
    intersecting n r x, sized n r x, card n r x hr⟩

/-- Checked target-owned attainment interface. -/
theorem attainment_of_localStar : AttainmentPackage := by
  apply attainment_of_starPackages
  · apply starConstruction_of_groundElement
    intro n r hr hhalf
    have hn2 : 0 < n / 2 := lt_of_lt_of_le Nat.zero_lt_one (hr.trans hhalf)
    exact ⟨⟨0, Nat.pos_of_div_pos hn2⟩⟩
  · exact Stage1Instances.THM_M_0822.erdosKoRadoStar_intersecting
  · exact Stage1Instances.THM_M_0822.erdosKoRadoStar_sized
  · apply starCard_of_image
    exact Stage1Instances.THM_M_0822.erdosKoRadoStar_eq_image

/-- Checked adapter from the pinned terminal type to the target's upper-bound package. -/
theorem upperBound_of_mathlibTerminal
    (terminal : MathlibUpperBoundTerminal) : UpperBoundPackage := by
  intro n r _hr hhalf A hIntersecting hSized
  exact terminal n r A hIntersecting hSized hhalf

/-- The actual pinned upper-bound candidate. Its terminal proof body remains
owned by `Finset.erdos_ko_rado`, not by this wrapper. -/
theorem pinnedMathlibUpperBound : MathlibUpperBoundTerminal := by
  intro n r A hIntersecting hSized hhalf
  exact Finset.erdos_ko_rado hIntersecting hSized hhalf

/-- The exact result type produced by the terminal assembly node. -/
abbrev ExactAssembly : Prop :=
  Stage1Instances.THM_M_0822.ErdosKoRadoMaximumTarget

/-- Exact child-to-assembly composition. Both mathematical children are consumed. -/
theorem composeRoot
    (attainment : AttainmentPackage)
    (upperBound : UpperBoundPackage) : ExactAssembly := by
  intro n r hr hhalf
  exact And.intro (attainment n r hr hhalf)
    (upperBound n r hr hhalf)

/-- Checked identity from terminal assembly to the canonical root. -/
theorem rootOfExactAssembly
    (assembly : ExactAssembly) :
    Stage1Instances.THM_M_0822.ErdosKoRadoMaximumTarget :=
  assembly

#check Stage1Instances.THM_M_0822.erdosKoRadoStar
#check Stage1Instances.THM_M_0822.erdosKoRadoStar_eq_image
#check Stage1Instances.THM_M_0822.erdosKoRadoStar_intersecting
#check Stage1Instances.THM_M_0822.erdosKoRadoStar_sized
#check Stage1Instances.THM_M_0822.card_erdosKoRadoStar
#check Stage1Instances.THM_M_0822.erdosKoRadoStar_attains
#check Finset.erdos_ko_rado
#check Finset.kruskal_katona_lovasz_form
#check Finset.iterated_kk
#check Finset.kruskal_katona

#print axioms attainment_of_localStar
#print axioms starConstruction_of_groundElement
#print axioms starCard_of_image
#print axioms attainment_of_starPackages
#print axioms upperBound_of_mathlibTerminal
#print axioms pinnedMathlibUpperBound
#print axioms composeRoot
#print axioms rootOfExactAssembly

set_option pp.universes true in
set_option pp.explicit true in
#print Stage1Instances.THM_M_0822.ErdosKoRadoMaximumTarget

end Stage1Instances.THM_M_0822.ObligationTree
