import Mathlib.Order.Height
import Mathlib.Order.Partition.Finpartition

/-!
# THM-M-0820 discovery-only intake probe

These checks authenticate pinned order, chain-height, antichain, and finite-partition interfaces.
They do not freeze a Mirsky target, audit terminal proof bodies, or create proof credit.
-/

#check @IsAntichain
#check @Set.chainHeight
#check @Set.exists_eq_chainHeight_of_finite
#check @Set.encard_le_chainHeight_of_isChain
#check @subsingleton_of_isChain_of_isAntichain
#check @Finpartition
#check @Finpartition.card_mono
#check @IsChain

example : IsAntichain (fun x y : Fin 1 => x <= y) Set.univ := by
  intro x _ y _ hxy hle
  exact hxy (Subsingleton.elim x y)

example : (Set.univ : Set (Fin 1)).chainHeight (fun x y => x <= y) = 1 := by
  apply le_antisymm
  · simpa using Set.chainHeight_le_encard (Set.univ : Set (Fin 1)) (fun x y => x <= y)
  · exact (Set.one_le_chainHeight_iff _ _).mpr Set.univ_nonempty

example : (Set.univ : Set (Fin 0)).chainHeight (fun x y => x <= y) = 0 := by
  exact Set.chainHeight_of_isEmpty (s := (Set.univ : Set (Fin 0))) (fun x y => x <= y)
