import Statement
import Mathlib.Algebra.Group.MinimalAxioms

/-!
Conditional composition harness for the frozen THM-M-0525 obligation tree.
The quotient laws are explicit hypotheses here; this file does not discharge them.
-/

universe u

namespace THM_M_0525

noncomputable section

abbrev LoopClass (X : Type u) [TopologicalSpace X] (x : X) :=
  Path.Homotopic.Quotient x x

/-- Build the forward-concatenation group from the three minimal group laws. -/
abbrev groupOfLeftLaws (X : Type u) [TopologicalSpace X] (x : X)
    (assoc : forall a b c : LoopClass X x,
      Path.Homotopic.Quotient.trans (Path.Homotopic.Quotient.trans a b) c =
        Path.Homotopic.Quotient.trans a (Path.Homotopic.Quotient.trans b c))
    (one_mul : forall a : LoopClass X x,
      Path.Homotopic.Quotient.trans (Path.Homotopic.Quotient.refl x) a = a)
    (inv_mul : forall a : LoopClass X x,
      Path.Homotopic.Quotient.trans (Path.Homotopic.Quotient.symm a) a =
        Path.Homotopic.Quotient.refl x) : Group (LoopClass X x) := by
  letI : Mul (LoopClass X x) := ⟨Path.Homotopic.Quotient.trans⟩
  letI : One (LoopClass X x) := ⟨Path.Homotopic.Quotient.refl x⟩
  letI : Inv (LoopClass X x) := ⟨Path.Homotopic.Quotient.symm⟩
  exact Group.ofLeftAxioms assoc one_mul inv_mul

/-- Checked child-to-root composition. All mathematical laws remain named premises. -/
theorem statement_of_left_laws (X : Type u) [TopologicalSpace X] (x : X)
    (assoc : forall a b c : LoopClass X x,
      Path.Homotopic.Quotient.trans (Path.Homotopic.Quotient.trans a b) c =
        Path.Homotopic.Quotient.trans a (Path.Homotopic.Quotient.trans b c))
    (one_mul : forall a : LoopClass X x,
      Path.Homotopic.Quotient.trans (Path.Homotopic.Quotient.refl x) a = a)
    (inv_mul : forall a : LoopClass X x,
      Path.Homotopic.Quotient.trans (Path.Homotopic.Quotient.symm a) a =
        Path.Homotopic.Quotient.refl x) : Statement X x := by
  let g := groupOfLeftLaws X x assoc one_mul inv_mul
  refine ⟨⟨g, ?_, ?_, ?_⟩⟩
  · intro p q
    change @Mul.mul _ g.toMul p q = _
    rfl
  · change @One.one _ g.toOne = _
    rfl
  · intro p
    change @Inv.inv _ g.toInv p = _
    rfl

#print axioms groupOfLeftLaws
#print axioms statement_of_left_laws

end
end THM_M_0525
