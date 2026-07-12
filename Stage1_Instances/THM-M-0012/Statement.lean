import Mathlib.Analysis.Complex.Polynomial.Basic

/-!
# THM-M-0012 canonical Lean statement

This module freezes the pointwise root-existence formulation of the fundamental theorem of
algebra selected at intake. It contains checked statement transports and mutation fixtures, but no
proof of the canonical target.
-/

namespace Stage1Instances.THM_M_0012

open Polynomial

/-- A complex polynomial is nonconstant when it is not in the image of `Polynomial.C`. -/
def Nonconstant (f : Polynomial Complex) : Prop :=
  Not (exists c : Complex, f = C c)

/-- Every nonconstant univariate complex polynomial has a complex root. -/
def FundamentalTheoremOfAlgebraTarget : Prop :=
  forall f : Polynomial Complex, Nonconstant f ->
    exists z : Complex, IsRoot f z

/-- The positive-degree shape used by the pinned `Complex.exists_root` declaration. -/
def PositiveDegreeRootTarget : Prop :=
  forall f : Polynomial Complex, 0 < degree f ->
    exists z : Complex, IsRoot f z

/-- Direct evaluation-at-zero form of the catalog claim. -/
def EvaluationRootTarget : Prop :=
  forall f : Polynomial Complex, Nonconstant f ->
    exists z : Complex, eval z f = 0

/-- Exclusion of all constant polynomials is equivalent to positive `WithBot Nat` degree. -/
theorem nonconstant_iff_degree_pos (f : Polynomial Complex) :
    Nonconstant f <-> 0 < degree f := by
  constructor
  · intro hf
    rw [<- not_le]
    intro hdegree
    exact hf ⟨coeff f 0, eq_C_of_degree_le_zero hdegree⟩
  · intro hdegree
    rintro ⟨c, rfl⟩
    exact (not_lt_of_ge (degree_C_le (a := c))) hdegree

/-- Checked transport to the exact positive-degree proposition adjacent to the pinned theorem. -/
theorem fundamentalTheoremOfAlgebraTarget_iff_positiveDegreeRootTarget :
    FundamentalTheoremOfAlgebraTarget <-> PositiveDegreeRootTarget := by
  constructor
  · intro h f hf
    exact h f ((nonconstant_iff_degree_pos f).2 hf)
  · intro h f hf
    exact h f ((nonconstant_iff_degree_pos f).1 hf)

/-- Checked transport between `Polynomial.IsRoot` and evaluation at zero. -/
theorem fundamentalTheoremOfAlgebraTarget_iff_evaluationRootTarget :
    FundamentalTheoremOfAlgebraTarget <-> EvaluationRootTarget := by
  simp only [FundamentalTheoremOfAlgebraTarget, EvaluationRootTarget, IsRoot.def]

/-! Structural mutations elaborate as propositions but receive no statement-identity credit. -/

def mutationRemovedNonconstantHypothesis : Prop :=
  forall f : Polynomial Complex,
    exists z : Complex, IsRoot f z

def mutationChangedDomainToReal : Prop :=
  forall f : Polynomial Real,
    Not (exists r : Real, f = C r) -> exists x : Real, IsRoot f x

def mutationChangedBinderScope : Prop :=
  exists z : Complex, forall f : Polynomial Complex,
    Nonconstant f -> IsRoot f z

def mutationExcludedLinearBoundary : Prop :=
  forall f : Polynomial Complex, 1 < degree f ->
    exists z : Complex, IsRoot f z

variable
  (hRemoved : mutationRemovedNonconstantHypothesis)
  (hDomain : mutationChangedDomainToReal)
  (hScope : mutationChangedBinderScope)
  (hBoundary : mutationExcludedLinearBoundary)

#check_failure (show FundamentalTheoremOfAlgebraTarget from hRemoved)
#check_failure (show FundamentalTheoremOfAlgebraTarget from hDomain)
#check_failure (show FundamentalTheoremOfAlgebraTarget from hScope)
#check_failure (show FundamentalTheoremOfAlgebraTarget from hBoundary)

/-! Boundary witnesses test the canonical antecedent without proving the root-existence target. -/

/-- The zero polynomial is excluded by the canonical nonconstancy antecedent. -/
theorem zero_not_nonconstant : Not (Nonconstant (0 : Polynomial Complex)) := by
  exact fun h => h ⟨0, C_0.symm⟩

/-- Every nonzero or zero constant polynomial is excluded by the canonical antecedent. -/
theorem C_not_nonconstant (c : Complex) : Not (Nonconstant (C c)) := by
  exact fun h => h ⟨c, rfl⟩

/-- Linear polynomials are included by the canonical antecedent. -/
theorem X_nonconstant : Nonconstant (X : Polynomial Complex) := by
  exact (nonconstant_iff_degree_pos X).2 <| by simp

#check fundamentalTheoremOfAlgebraTarget_iff_positiveDegreeRootTarget
#check fundamentalTheoremOfAlgebraTarget_iff_evaluationRootTarget
#print axioms nonconstant_iff_degree_pos
#print axioms fundamentalTheoremOfAlgebraTarget_iff_positiveDegreeRootTarget
#print axioms fundamentalTheoremOfAlgebraTarget_iff_evaluationRootTarget

set_option pp.universes true in
set_option pp.explicit true in
#print FundamentalTheoremOfAlgebraTarget

end Stage1Instances.THM_M_0012
