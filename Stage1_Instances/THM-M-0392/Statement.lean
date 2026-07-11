import Init

/-!
# THM-M-0392: canonical Mordell-equation statement

This module freezes and elaborates the integer finiteness statement only. It does not prove it.
-/

namespace Stage1Instances.THMM0392

/-- A dependency-minimal finiteness predicate: the type injects into some finite type. -/
def IsFinite (α : Type) : Prop :=
  ∃ n : Nat, ∃ encode : α → Fin n, Function.Injective encode

/-- The affine Mordell equation with integer parameter and coordinates. -/
def MordellEquation (k x y : Int) : Prop :=
  y ^ 2 = x ^ 3 + k

/-- Integer points on the affine Mordell equation for a fixed parameter. -/
def IntegralSolutions (k : Int) :=
  {p : Int × Int // MordellEquation k p.1 p.2}

/-- The exact rev-5.6 target: each nonzero integer parameter has finitely many integer solutions. -/
def MordellFinitenessStatement : Prop :=
  ∀ k : Int, k ≠ 0 → IsFinite (IntegralSolutions k)

/-- An inline presentation of the same target, retained as a checked alternate encoding. -/
def InlineEquationStatement : Prop :=
  ∀ k : Int, k ≠ 0 →
    IsFinite {p : Int × Int // p.2 ^ 2 = p.1 ^ 3 + k}

/-- Statement-level transport only; this theorem supplies no finiteness proof. -/
theorem mordellFinitenessStatement_iff_inlineEquationStatement :
    MordellFinitenessStatement ↔ InlineEquationStatement :=
  Iff.rfl

-- Separately elaborated mutations. None receives equivalence or proof credit.
def MutationRemovedNonzero : Prop :=
  ∀ k : Int, IsFinite (IntegralSolutions k)

def MutationChangedCoordinateDomain : Prop :=
  ∀ k : Int, k ≠ 0 →
    IsFinite {p : Nat × Nat // (p.2 : Int) ^ 2 = (p.1 : Int) ^ 3 + k}

def MutationChangedBinderScope : Prop :=
  ∃ k : Int, k ≠ 0 ∧ IsFinite (IntegralSolutions k)

def MutationZeroBoundary : Prop :=
  IsFinite (IntegralSolutions 0)

end Stage1Instances.THMM0392

set_option pp.explicit true in
#print Stage1Instances.THMM0392.MordellFinitenessStatement
