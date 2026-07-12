import ObligationTree

/-!
# THM-M-0452 proof bodies

This module discharges the quotient-descent branch of the frozen obligation
tree.  Given the already-frozen polarization package, bilinearity makes the
pairing vanish whenever either argument is torsion.  Two applications of
`QuotientAddGroup.lift` therefore produce the pairing on the torsion quotient;
the diagonal-kernel field proves positive definiteness there.

The canonical-height and polarization constructions remain separate open
inputs.  In particular, this file does not claim the exact root theorem.
-/

noncomputable section

open scoped WeierstrassCurve.Affine

namespace Stage1Instances.THM_M_0452

universe u

variable {K : Type u} [Field K] [DecidableEq K] [NumberField K]
variable {E : WeierstrassCurve K} [E.IsElliptic]
variable {h : CanonicalHeightCore K E}

private lemma pairing_zero_left (p : PolarizationCore K E h.canonicalHeight)
    (Q : E⟮K⟯) : p.pairing 0 Q = 0 := by
  have := p.add_left 0 0 Q
  have := congrArg (fun x : ℝ => x - p.pairing 0 Q) this
  have hz : (0 : ℝ) = p.pairing 0 Q := by
    simpa only [zero_add, add_sub_cancel_left, sub_self] using this
  exact hz.symm

private lemma pairing_zero_right (p : PolarizationCore K E h.canonicalHeight)
    (P : E⟮K⟯) : p.pairing P 0 = 0 := by
  have := p.add_right P 0 0
  have := congrArg (fun x : ℝ => x - p.pairing P 0) this
  have hz : (0 : ℝ) = p.pairing P 0 := by
    simpa only [zero_add, add_sub_cancel_left, sub_self] using this
  exact hz.symm

private def pairingLeftHom (p : PolarizationCore K E h.canonicalHeight) (Q : E⟮K⟯) :
    E⟮K⟯ →+ ℝ where
  toFun P := p.pairing P Q
  map_zero' := pairing_zero_left p Q
  map_add' P R := p.add_left P R Q

private def pairingRightHom (p : PolarizationCore K E h.canonicalHeight) (P : E⟮K⟯) :
    E⟮K⟯ →+ ℝ where
  toFun Q := p.pairing P Q
  map_zero' := pairing_zero_right p P
  map_add' Q R := p.add_right P Q R

private lemma torsion_pairing_left_zero (p : PolarizationCore K E h.canonicalHeight)
    {T : E⟮K⟯} (hT : T ∈ AddCommGroup.torsion E⟮K⟯) (Q : E⟮K⟯) :
    p.pairing T Q = 0 := by
  obtain ⟨n, hn, hnT⟩ := hT.exists_nsmul_eq_zero
  have hp := p.zsmul_left (n : ℤ) T Q
  norm_num [hnT, pairing_zero_left p Q] at hp
  exact hp.resolve_left hn.ne'

private lemma torsion_pairing_right_zero (p : PolarizationCore K E h.canonicalHeight)
    (P : E⟮K⟯) {T : E⟮K⟯} (hT : T ∈ AddCommGroup.torsion E⟮K⟯) :
    p.pairing P T = 0 := by
  obtain ⟨n, hn, hnT⟩ := hT.exists_nsmul_eq_zero
  have hp := p.zsmul_right (n : ℤ) P T
  norm_num [hnT, pairing_zero_right p P] at hp
  exact hp.resolve_left hn.ne'

private def pairingLeftQuotient (p : PolarizationCore K E h.canonicalHeight) (Q : E⟮K⟯) :
    (E⟮K⟯ ⧸ (AddCommGroup.torsion E⟮K⟯)) →+ ℝ :=
  QuotientAddGroup.lift (AddCommGroup.torsion E⟮K⟯) (pairingLeftHom p Q) <| by
    intro T hT
    exact torsion_pairing_left_zero p hT Q

private def pairingQuotientRightHom (p : PolarizationCore K E h.canonicalHeight)
    (X : E⟮K⟯ ⧸ (AddCommGroup.torsion E⟮K⟯)) : E⟮K⟯ →+ ℝ where
  toFun Q := pairingLeftQuotient p Q X
  map_zero' := by
    refine QuotientAddGroup.induction_on X ?_
    intro P
    exact pairing_zero_right p P
  map_add' Q R := by
    refine QuotientAddGroup.induction_on X ?_
    intro P
    exact p.add_right P Q R

private def pairingOnTorsionQuotient (p : PolarizationCore K E h.canonicalHeight)
    (X : E⟮K⟯ ⧸ (AddCommGroup.torsion E⟮K⟯)) :
    (E⟮K⟯ ⧸ (AddCommGroup.torsion E⟮K⟯)) →+ ℝ :=
  QuotientAddGroup.lift (AddCommGroup.torsion E⟮K⟯) (pairingQuotientRightHom p X) <| by
    intro T hT
    refine QuotientAddGroup.induction_on X ?_
    intro P
    exact torsion_pairing_right_zero p P hT

/-- `M0452-D-WELLDEFINED` and `M0452-D-POSITIVE`: the bilinear pairing with
torsion diagonal kernel descends to a positive-definite form on the quotient. -/
def quotientPairingCoreOfPolarization
    (p : PolarizationCore K E h.canonicalHeight) : QuotientPairingCore K E p.pairing where
  quotientPairing X Y := pairingOnTorsionQuotient p X Y
  quotient_lift P Q := rfl
  quotient_positive_definite := by
    intro X
    refine QuotientAddGroup.induction_on X ?_
    intro P
    constructor
    · exact p.diagonal_nonnegative P
    · constructor
      · intro hp
        exact QuotientAddGroup.eq_iff_sub_mem.mpr (by
          simpa using (p.diagonal_kernel P).mp hp)
      · intro hP
        have hT : IsOfFinAddOrder P := by
          have : P - 0 ∈ AddCommGroup.torsion E⟮K⟯ :=
            QuotientAddGroup.eq_iff_sub_mem.mp hP
          simpa using this
        exact (p.diagonal_kernel P).mpr hT

/-- The quotient branch now has an unconditional local proof body once the
height and polarization packages have been supplied. -/
theorem quotientPairingCoreTarget_of_polarization : QuotientPairingCoreTarget.{u} := by
  intro K _ _ _ E _ h p
  exact ⟨quotientPairingCoreOfPolarization p⟩

#print axioms quotientPairingCoreOfPolarization
#print axioms quotientPairingCoreTarget_of_polarization

end Stage1Instances.THM_M_0452
