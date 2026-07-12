import Mathlib.Data.Fin.Tuple.Reflection
import Mathlib.Data.Set.Card
import Mathlib.Data.Set.Finite.Basic
import Mathlib.NumberTheory.Height.Basic
import Mathlib.RingTheory.MvPolynomial.Basic
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Topology.Connected.Basic
import Mathlib.Topology.Instances.Real.Lemmas

/-!
The exact first-version Pila-Wilkie target from Theorem 1.8.  This file only freezes and
elaborates the proposition; it does not assert the proposition as a theorem.
-/

namespace AwesomeTheorems.THM_M_0464

open Finset Set

/-- A Boolean formula in polynomial equalities and strict inequalities. -/
inductive SemialgebraicFormula (n : ℕ) where
  | equal (p : MvPolynomial (Fin n) ℝ)
  | positive (p : MvPolynomial (Fin n) ℝ)
  | not (p : SemialgebraicFormula n)
  | and (p q : SemialgebraicFormula n)

def SemialgebraicFormula.Realize {n : ℕ} :
    SemialgebraicFormula n → (Fin n → ℝ) → Prop
  | .equal p, x => MvPolynomial.eval x p = 0
  | .positive p, x => 0 < MvPolynomial.eval x p
  | .not p, x => ¬p.Realize x
  | .and p q, x => p.Realize x ∧ q.Realize x

/-- A semialgebraic subset of `ℝⁿ`, in the Boolean-combination definition. -/
def IsSemialgebraic {n : ℕ} (s : Set (Fin n → ℝ)) : Prop :=
  ∃ p : SemialgebraicFormula n, s = {x | p.Realize x}

/-- Cartesian product, with the first block of coordinates followed by the second. -/
def setProduct {n m : ℕ} (s : Set (Fin n → ℝ)) (t : Set (Fin m → ℝ)) :
    Set (Fin (n + m) → ℝ) :=
  {z | (fun i => z (Fin.castAdd m i)) ∈ s ∧ (fun j => z (Fin.natAdd n j)) ∈ t}

/-- Projection of the final `m` coordinates. -/
def project {n m : ℕ} (s : Set (Fin (n + m) → ℝ)) : Set (Fin n → ℝ) :=
  {x | ∃ y : Fin m → ℝ, Fin.addCases x y ∈ s}

/-- The paper's sequence of Boolean algebras of definable real sets. -/
structure OMinimalStructure where
  definable : (n : ℕ) → Set (Fin n → ℝ) → Prop
  empty_definable : ∀ n, 1 ≤ n → definable n ∅
  compl_definable : ∀ {n s}, 1 ≤ n → definable n s → definable n sᶜ
  union_definable : ∀ {n s t}, 1 ≤ n → definable n s → definable n t → definable n (s ∪ t)
  semialgebraic_definable : ∀ {n s}, 1 ≤ n → IsSemialgebraic s → definable n s
  product_definable : ∀ {n m s t},
    1 ≤ n → 1 ≤ m → definable n s → definable m t → definable (n + m) (setProduct s t)
  projection_definable : ∀ {n m s}, 1 ≤ n → definable (n + m) s → definable n (project s)
  one_frontier_finite : ∀ {s : Set (Fin 1 → ℝ)}, definable 1 s → (frontier s).Finite

/-- The union of connected, positive-dimensional semialgebraic subsets of `x`.  For a connected
semialgebraic set, positive dimension is equivalent to having more than one point. -/
def algebraicPart {n : ℕ} (x : Set (Fin n → ℝ)) : Set (Fin n → ℝ) :=
  ⋃₀ {s : Set (Fin n → ℝ) |
    s ⊆ x ∧ IsSemialgebraic s ∧ IsConnected s ∧ ¬s.Subsingleton}

/-- The paper's affine height `max (|a|, b)` for a reduced rational `a / b`. -/
def rationalHeight (q : ℚ) : ℕ := max q.num.natAbs q.den

/-- The coordinatewise maximum height on `ℚⁿ`. -/
def pointHeight {n : ℕ} (q : Fin n → ℚ) : ℕ :=
  univ.sup (fun i => rationalHeight (q i))

/-- Rational points in `x` of height at most `T`. -/
def rationalPoints {n : ℕ} (x : Set (Fin n → ℝ)) (T : ℕ) : Set (Fin n → ℚ) :=
  {q | (fun i => (q i : ℝ)) ∈ x ∧ pointHeight q ≤ T}

/-- Pila-Wilkie, Theorem 1.8 (first version): for a definable `X ⊆ ℝⁿ` and every positive
`epsilon`, the number of rational points of height at most `T` in `X \ Xᵃˡᵍ` is
`O(T ^ epsilon)`.  The source convention is `T ≥ 1` and `n ≥ 1`.

This is deliberately a `Prop` definition rather than a theorem declaration: the statement phase
elaborates the exact target but supplies no proof or proof credit.
-/
def PilaWilkieStatement : Prop :=
  ∀ (S : OMinimalStructure) (n : ℕ) (_hn : 1 ≤ n)
    (X : Set (Fin n → ℝ)) (_hX : S.definable n X)
    (epsilon : ℝ),
    0 < epsilon →
      ∃ c : ℝ, ∀ T : ℕ, 1 ≤ T →
        (rationalPoints (X \ algebraicPart X) T).Finite ∧
          ((rationalPoints (X \ algebraicPart X) T).ncard : ℝ) ≤ c * (T : ℝ) ^ epsilon

#check PilaWilkieStatement

set_option pp.universes true in
set_option pp.explicit true in
#print PilaWilkieStatement

end AwesomeTheorems.THM_M_0464
