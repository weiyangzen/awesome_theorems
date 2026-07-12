import ObligationTree

/-!
# THM-M-0525 proof-phase bodies

The frozen forward-concatenation group is constructed from mathlib's quotient-level path laws.
Unlike the existing `FundamentalGroup` instance, multiplication here is `p.trans q`, exactly as
required by `Statement.lean`.
-/

universe u

namespace THM_M_0525

noncomputable section

/-- Associativity for forward concatenation of endpoint-fixed path-homotopy classes. -/
theorem forward_trans_assoc (X : Type u) [TopologicalSpace X] (x : X) :
    forall a b c : LoopClass X x,
      Path.Homotopic.Quotient.trans (Path.Homotopic.Quotient.trans a b) c =
        Path.Homotopic.Quotient.trans a (Path.Homotopic.Quotient.trans b c) :=
  Path.Homotopic.Quotient.trans_assoc

/-- The constant loop is a left identity for forward concatenation. -/
theorem forward_refl_trans (X : Type u) [TopologicalSpace X] (x : X) :
    forall a : LoopClass X x,
      Path.Homotopic.Quotient.trans (Path.Homotopic.Quotient.refl x) a = a :=
  Path.Homotopic.Quotient.refl_trans

/-- Reversal is a left inverse for forward concatenation. -/
theorem forward_symm_trans (X : Type u) [TopologicalSpace X] (x : X) :
    forall a : LoopClass X x,
      Path.Homotopic.Quotient.trans (Path.Homotopic.Quotient.symm a) a =
        Path.Homotopic.Quotient.refl x :=
  Path.Homotopic.Quotient.symm_trans

/-- Unconditional proof of the exact frozen THM-M-0525 statement. -/
theorem statement_proof (X : Type u) [TopologicalSpace X] (x : X) : Statement X x :=
  statement_of_left_laws X x
    (forward_trans_assoc X x)
    (forward_refl_trans X x)
    (forward_symm_trans X x)

#print axioms forward_trans_assoc
#print axioms forward_refl_trans
#print axioms forward_symm_trans
#print axioms statement_proof

end
end THM_M_0525
