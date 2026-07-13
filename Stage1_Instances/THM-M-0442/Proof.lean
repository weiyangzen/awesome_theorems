import ObligationTree

/-!
# THM-M-0442 partial proof execution

This module checks the finite-cardinality consequence needed to compare the
exact classification with the weaker external FLT assumption. It does not
prove the classification or inhabit any field of `ObligationTree.MazurEngine`.
-/

noncomputable section

open scoped WeierstrassCurve.Affine

namespace Stage1Instances.THMM0442.Proof

open Stage1Instances.THMM0442

/-- The weak cardinality proposition exposed by the audited FLT source. -/
def TorsionBoundAtMostSixteen : Prop :=
  ∀ (E : WeierstrassCurve Rat) [E.IsElliptic],
    (AddCommGroup.torsion E⟮Rat⟯ : Set E⟮Rat⟯).ncard ≤ 16

/-- Every cyclic order in the exact target is at most sixteen. -/
theorem cyclic_order_le_sixteen {n : Nat} (h : IsMazurCyclicOrder n) : n ≤ 16 := by
  rcases h with ⟨_, h10⟩ | rfl
  · omega
  · omega

/-- Every bicyclic index in the exact target gives total order at most sixteen. -/
theorem bicyclic_index_four_mul_le_sixteen {m : Nat}
    (h : IsMazurBicyclicIndex m) : 2 * (2 * m) ≤ 16 := by
  rcases h with ⟨_, h4⟩
  omega

/-- A cyclic equivalence determines the cardinality of the torsion subtype. -/
theorem torsion_ncard_eq_of_hasCyclicTorsionOrder
    {E : WeierstrassCurve Rat} [E.IsElliptic] {n : Nat}
    (h : HasCyclicTorsionOrder E n) :
    (AddCommGroup.torsion E⟮Rat⟯ : Set E⟮Rat⟯).ncard = n := by
  rcases h with ⟨e⟩
  rw [← Nat.card_coe_set_eq]
  exact (Nat.card_congr e.toEquiv).trans (Nat.card_zmod n)

/-- A bicyclic equivalence determines the cardinality of the torsion subtype. -/
theorem torsion_ncard_eq_of_hasBicyclicTorsionIndex
    {E : WeierstrassCurve Rat} [E.IsElliptic] {m : Nat}
    (h : HasBicyclicTorsionIndex E m) :
    (AddCommGroup.torsion E⟮Rat⟯ : Set E⟮Rat⟯).ncard = 2 * (2 * m) := by
  rcases h with ⟨e⟩
  rw [← Nat.card_coe_set_eq]
  calc
    Nat.card (RationalTorsionGroup E) = Nat.card (ZMod 2 × ZMod (2 * m)) :=
      Nat.card_congr e.toEquiv
    _ = 2 * (2 * m) := by rw [Nat.card_prod, Nat.card_zmod, Nat.card_zmod]

/-- The exact classification implies the weaker audited cardinality bound. -/
theorem mazurRationalTorsionTarget_implies_torsionBoundAtMostSixteen
    (h : MazurRationalTorsionTarget) : TorsionBoundAtMostSixteen := by
  intro E hE
  rcases h E with ⟨n, hn, hcyc⟩ | ⟨m, hm, hbic⟩
  · rw [torsion_ncard_eq_of_hasCyclicTorsionOrder hcyc]
    exact cyclic_order_le_sixteen hn
  · rw [torsion_ncard_eq_of_hasBicyclicTorsionIndex hbic]
    exact bicyclic_index_four_mul_le_sixteen hm

#print axioms cyclic_order_le_sixteen
#print axioms bicyclic_index_four_mul_le_sixteen
#print axioms torsion_ncard_eq_of_hasCyclicTorsionOrder
#print axioms torsion_ncard_eq_of_hasBicyclicTorsionIndex
#print axioms mazurRationalTorsionTarget_implies_torsionBoundAtMostSixteen
#print axioms Stage1Instances.THMM0442.ObligationTree.engine_compose

end Stage1Instances.THMM0442.Proof
