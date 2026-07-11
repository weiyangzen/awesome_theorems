import Mathlib.Algebra.Azumaya.Basic
import Mathlib.Algebra.Azumaya.Matrix
import Mathlib.Algebra.BrauerGroup.Defs
import Mathlib.RingTheory.Artinian.Module
import Mathlib.RingTheory.Morita.Matrix
import Mathlib.RingTheory.SimpleModule.WedderburnArtin

/-!
# THM-M-0424 anchor probes

These declarations check the useful candidates found by the bounded anchor
audit. None constructs `BrauerGroupLawData` or closes `BrauerGroupStatement`.
-/

noncomputable section

namespace Stage1Instances.THM_M_0424.AnchorAudit

universe u v

variable {K : Type u} [Field K]

/-- Local spelling of the frozen target's quotient class. -/
abbrev AuditedBrauerClass (A : CSA.{u, v} K) : BrauerGroup K :=
  Quotient.mk (Brauer.CSA_Setoid K) A

/-- The quotient API classifies representatives by its defining setoid. -/
theorem quotient_eq_iff (A B : CSA.{u, v} K) :
    AuditedBrauerClass A = AuditedBrauerClass B <-> IsBrauerEquivalent A B :=
  Quotient.eq

/-- Wedderburn-Artin gives a supporting normal form, not the Brauer group law. -/
theorem wedderburnArtin (A : CSA.{u, v} K) :
    exists (n : Nat) (_ : NeZero n) (D : Type v) (_ : DivisionRing D) (_ : Algebra K D)
      (_ : Module.Finite K D), Nonempty (A ≃ₐ[K] Matrix (Fin n) (Fin n) D) := by
  letI : IsArtinianRing A := IsArtinianRing.of_finite K A
  exact IsSimpleRing.exists_algEquiv_matrix_divisionRing_finite K A

/-- Stable matrix equivalence supplies the easy direction of the Morita bridge. -/
theorem brauerEquivalent_to_morita {A B : CSA.{u, v} K}
    (h : IsBrauerEquivalent A B) : IsMoritaEquivalent K A B := by
  obtain ⟨n, m, hn, hm, ⟨e⟩⟩ := h
  haveI : Nonempty (Fin n) := Fin.pos_iff_nonempty.mp (Nat.pos_of_ne_zero hn)
  haveI : Nonempty (Fin m) := Fin.pos_iff_nonempty.mp (Nat.pos_of_ne_zero hm)
  exact IsMoritaEquivalent.trans K
    (IsMoritaEquivalent.trans K (IsMoritaEquivalent.matrix K (R := A))
      (IsMoritaEquivalent.of_algEquiv (R := K) e))
    (IsMoritaEquivalent.matrix K (R := B)).symm

/-- The neighboring Azumaya API contains only supporting base and matrix cases. -/
theorem azumaya_support (R : Type u) [CommRing R] :
    IsAzumaya R R /\
      (forall (n : Type v) [Fintype n] [DecidableEq n] [Nonempty n],
        IsAzumaya R (Matrix n n R)) := by
  exact ⟨IsAzumaya.id R, fun n => IsAzumaya.matrix R n⟩

end Stage1Instances.THM_M_0424.AnchorAudit

#check Stage1Instances.THM_M_0424.AnchorAudit.quotient_eq_iff
#check Stage1Instances.THM_M_0424.AnchorAudit.wedderburnArtin
#check Stage1Instances.THM_M_0424.AnchorAudit.brauerEquivalent_to_morita
#check Stage1Instances.THM_M_0424.AnchorAudit.azumaya_support
