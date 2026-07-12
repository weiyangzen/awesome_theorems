import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Data.Set.Card
import Mathlib.ModelTheory.Algebra.Field.Basic
import Mathlib.ModelTheory.Definability
import Mathlib.Topology.Closure
import Mathlib.Topology.Separation.Connected

/-!
# THM-M-0665: exact Pila-Wilkie first-version statement

This module freezes Theorem 1.8 of Pila and Wilkie's 2006 paper. It states the
target only; it contains no proof of the counting theorem.
-/

open FirstOrder
open Set

namespace Stage1Instances.THM_M_0665

local instance : FirstOrder.Ring.CompatibleRing Real :=
  FirstOrder.Ring.compatibleRingOfRing Real

/-- Rational points in affine `n`-space. -/
abbrev RationalPoint (n : Nat) := Fin n -> Rat

/-- The affine height from Pila-Wilkie Definition 1.3. -/
def rationalHeight (q : Rat) : Nat :=
  max q.num.natAbs q.den

/-- Coordinatewise maximum of the affine rational height. -/
def pointHeight {n : Nat} (q : RationalPoint n) : Nat :=
  Finset.univ.sup fun i => rationalHeight (q i)

/-- Coordinatewise inclusion of a rational point in real affine space. -/
def rationalPointToReal {n : Nat} (q : RationalPoint n) : Fin n -> Real :=
  fun i => q i

/-- Semialgebraic means definable, with real parameters, in the ring language.
Over the real closed field this also captures inequalities. -/
def IsSemialgebraic {n : Nat} (X : Set (Fin n -> Real)) : Prop :=
  (Set.univ : Set Real).Definable Language.ring X

/-- A first-order expansion of the real field is o-minimal when it contains the
semialgebraic sets and every definable unary set has finite boundary. -/
def IsOMinimalExpansion
    (L : Language.{0, 0}) [L.Structure Real] : Prop :=
  (forall (n : Nat) (X : Set (Fin n -> Real)),
      IsSemialgebraic X -> (Set.univ : Set Real).Definable L X) /\
    (forall X : Set (Fin 1 -> Real),
      (Set.univ : Set Real).Definable L X -> (frontier X).Finite)

/-- The algebraic part from Pila-Wilkie Definition 1.5: the union of all
connected positive-dimensional semialgebraic subsets of `X`. For a connected
semialgebraic set, positive dimension is equivalent to having two points. -/
def algebraicPart {n : Nat} (X : Set (Fin n -> Real)) : Set (Fin n -> Real) :=
  {x | exists A : Set (Fin n -> Real),
    A <= X /\ IsSemialgebraic A /\ IsPreconnected A /\ A.Nontrivial /\ x ∈ A}

/-- Rational points of affine height at most `T` in the transcendental part. -/
def transcendentalRationalPoints {n : Nat}
    (X : Set (Fin n -> Real)) (T : Nat) : Set (RationalPoint n) :=
  {q | rationalPointToReal q ∈ X \ algebraicPart X /\ pointHeight q <= T}

/--
Pila-Wilkie, Theorem 1.8 (first version): for a set definable in an o-minimal
expansion of the real field and every positive real exponent, the number of
rational points of height at most `T` outside the algebraic part is bounded by
`c * T ^ epsilon`, uniformly for `T >= 1`.
-/
def PilaWilkie : Prop :=
  forall (L : Language.{0, 0}) [L.Structure Real],
    IsOMinimalExpansion L ->
    forall (n : Nat) (X : Set (Fin n -> Real)),
      (Set.univ : Set Real).Definable L X ->
      forall epsilon : Real, 0 < epsilon ->
        exists c : Real, 0 < c /\ forall T : Nat, 1 <= T ->
          (transcendentalRationalPoints X T).Finite /\
          ((transcendentalRationalPoints X T).ncard : Real) <=
            c * (T : Real) ^ epsilon

/-- Checked expansion fixing binder order, scope, height, algebraic part, and
the quantitative conclusion. -/
theorem pilaWilkie_iff : PilaWilkie <->
    forall (L : Language.{0, 0}) [L.Structure Real],
      IsOMinimalExpansion L ->
      forall (n : Nat) (X : Set (Fin n -> Real)),
        (Set.univ : Set Real).Definable L X ->
        forall epsilon : Real, 0 < epsilon ->
          exists c : Real, 0 < c /\ forall T : Nat, 1 <= T ->
            (transcendentalRationalPoints X T).Finite /\
            ((transcendentalRationalPoints X T).ncard : Real) <=
              c * (T : Real) ^ epsilon :=
  Iff.rfl

-- Structural mutations are separately elaborated and fingerprinted.
def mutationRemovedOMinimality : Prop :=
  forall (L : Language.{0, 0}) [L.Structure Real]
    (n : Nat) (X : Set (Fin n -> Real)),
      (Set.univ : Set Real).Definable L X ->
      forall epsilon : Real, 0 < epsilon -> exists c : Real, 0 < c

def mutationChangedDomain : Prop :=
  forall (n : Nat) (X : Set (Fin n -> Real)),
    IsSemialgebraic X -> forall epsilon : Real, 0 < epsilon -> exists c : Real, 0 < c

def mutationChangedBinderScope : Prop :=
  exists c : Real, 0 < c /\ forall (L : Language.{0, 0}) [L.Structure Real],
    IsOMinimalExpansion L -> forall (n : Nat), exists X : Set (Fin n -> Real), X = X

/-- The height threshold `T = 0` is deliberately outside the source theorem. -/
theorem threshold_boundary : not (1 <= (0 : Nat)) := by decide

/-- The zero-dimensional affine height uses the empty maximum convention. -/
theorem zero_dimensional_height (q : RationalPoint 0) : pointHeight q = 0 := by
  simp [pointHeight]

end Stage1Instances.THM_M_0665

set_option pp.explicit true in
#print Stage1Instances.THM_M_0665.PilaWilkie
