import ObligationTree

/-!
# THM-M-0419 partial proof execution

This module implements the intended frozen cyclotomic-identification
transport. It turns positive containment in any abstract singleton
cyclotomic extension into the exact `PositiveContainmentTarget` used by the
root architecture. It does not construct the local Kronecker-Weber packages
or the global conductor and inertia embedding.
-/

namespace Stage1.THM_M_0419.Proof

universe uK uL

/-- The output of the conductor and inertia packages before identifying their
abstract singleton cyclotomic extension with `CyclotomicField`. -/
def AbstractPositiveContainmentTarget : Prop :=
  ∀ (K : Type uK) [Field K] [Algebra ℚ K] [NumberField K]
      [IsAbelianGalois ℚ K],
    ∃ n : ℕ, 1 ≤ n ∧
      ∃ (L : Type uL) (_ : Field L) (_ : Algebra ℚ L)
        (_ : IsCyclotomicExtension {n} ℚ L),
        Nonempty (K →ₐ[ℚ] L)

/-- `M0419-C-CYCLOTOMIC-IDENTIFY`: identify the abstract singleton
cyclotomic extension with the canonical cyclotomic field and compose its
existing `ℚ`-algebra embedding. -/
theorem cyclotomicIdentify :
    AbstractPositiveContainmentTarget.{uK, uL} →
      ObligationTree.PositiveContainmentTarget.{uK} := by
  intro abstract K _ _ _ _
  obtain ⟨n, hn, L, fieldL, algebraL, cyclotomicL, ⟨f⟩⟩ := abstract K
  letI : Field L := fieldL
  letI : Algebra ℚ L := algebraL
  letI : IsCyclotomicExtension {n} ℚ L := cyclotomicL
  letI : NeZero n := ⟨Nat.ne_of_gt hn⟩
  letI : Algebra ℚ (CyclotomicField n ℚ) :=
    CyclotomicField.algebraBase n ℚ ℚ
  letI : IsCyclotomicExtension {n} ℚ (CyclotomicField n ℚ) :=
    CyclotomicField.isCyclotomicExtension n ℚ
  refine ⟨n, hn, ?_⟩
  exact ⟨(IsCyclotomicExtension.algEquiv {n} ℚ L
    (CyclotomicField n ℚ)).toAlgHom.comp f⟩

#check cyclotomicIdentify
#print axioms cyclotomicIdentify
#print axioms IsCyclotomicExtension.algEquiv

end Stage1.THM_M_0419.Proof
