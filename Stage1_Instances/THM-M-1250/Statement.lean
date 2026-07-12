import Mathlib.Analysis.Distribution.SchwartzSpace.Basic

/-!
# THM-M-1250: exact Schwartz-space statement

This module freezes the statement boundary only. It does not prove the
characterization.
-/

noncomputable section

open scoped SchwartzMap

namespace Stage1Instances.THM_M_1250

abbrev EuclideanDomain (n : Nat) := Fin n → ℝ

/-- The classical smoothness and rapid-decay conditions for a complex-valued
function on `R^n`, expressed using Fréchet derivatives. -/
def IsSchwartzFunction {n : Nat} (f : EuclideanDomain n → ℂ) : Prop :=
  ContDiff ℝ ⊤ f ∧
    ∀ k r : Nat, ∃ C : ℝ, ∀ x,
      ‖x‖ ^ k * ‖iteratedFDeriv ℝ r f x‖ ≤ C

/-- A function on `R^n` belongs to the Schwartz space exactly when it is
smooth and every derivative decays faster than every inverse polynomial.

Dimension zero is deliberately included. Equality is pointwise function
equality, so the left side states membership without assuming a bundled map.
-/
def SchwartzSpaceCharacterization : Prop :=
  ∀ (n : Nat) (f : EuclideanDomain n → ℂ),
    (∃ φ : SchwartzMap (EuclideanDomain n) ℂ, (φ : EuclideanDomain n → ℂ) = f) ↔
      IsSchwartzFunction f

/-- Subtype encoding used to check the transport from existential membership. -/
def SchwartzRepresentative {n : Nat} (f : EuclideanDomain n → ℂ) :=
  { φ : SchwartzMap (EuclideanDomain n) ℂ // (φ : EuclideanDomain n → ℂ) = f }

theorem exists_representative_iff_nonempty
    {n : Nat} (f : EuclideanDomain n → ℂ) :
    (∃ φ : SchwartzMap (EuclideanDomain n) ℂ, (φ : EuclideanDomain n → ℂ) = f) ↔
      Nonempty (SchwartzRepresentative f) := by
  constructor
  · rintro ⟨φ, hφ⟩
    exact ⟨⟨φ, hφ⟩⟩
  · rintro ⟨⟨φ, hφ⟩⟩
    exact ⟨φ, hφ⟩

-- Separately elaborated structural mutations used by `check_statement.py`.
def mutationRealCodomain : Prop :=
  ∀ (n : Nat) (f : EuclideanDomain n → ℝ),
    ∃ φ : SchwartzMap (EuclideanDomain n) ℝ, (φ : EuclideanDomain n → ℝ) = f

def mutationOmitsSmoothness : Prop :=
  ∀ (n : Nat) (f : EuclideanDomain n → ℂ),
    (∃ φ : SchwartzMap (EuclideanDomain n) ℂ, (φ : EuclideanDomain n → ℂ) = f) ↔
      ∀ k r : Nat, ∃ C : ℝ, ∀ x,
        ‖x‖ ^ k * ‖iteratedFDeriv ℝ r f x‖ ≤ C

def mutationOnlyFunctionDecay : Prop :=
  ∀ (n : Nat) (f : EuclideanDomain n → ℂ),
    (∃ φ : SchwartzMap (EuclideanDomain n) ℂ, (φ : EuclideanDomain n → ℂ) = f) ↔
      ContDiff ℝ ⊤ f ∧
        ∀ k : Nat, ∃ C : ℝ, ∀ x, ‖x‖ ^ k * ‖f x‖ ≤ C

def mutationPositiveDimension : Prop :=
  ∀ (n : Nat), 0 < n → ∀ f : EuclideanDomain n → ℂ,
    (∃ φ : SchwartzMap (EuclideanDomain n) ℂ, (φ : EuclideanDomain n → ℂ) = f) ↔
      IsSchwartzFunction f

end Stage1Instances.THM_M_1250

set_option pp.explicit true in
#print Stage1Instances.THM_M_1250.SchwartzSpaceCharacterization
