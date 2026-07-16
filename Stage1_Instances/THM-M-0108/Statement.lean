import Mathlib.Analysis.Complex.Basic
import Mathlib.Analysis.Analytic.Basic
import Mathlib.LinearAlgebra.Projectivization.Basic
import Mathlib.RingTheory.MvPolynomial.Homogeneous

/-!
# THM-M-0108: Chow's theorem, reduced carrier formulation

The analytic input is defined by local analytic equations on the punctured
homogeneous-coordinate cone. This supplies mathematical data missing from the
bare `Projectivization` API without postulating a projective topology or using
an abstract placeholder predicate. The algebraic conclusion is equality of
the reduced carrier with a simultaneous zero locus of homogeneous complex
polynomials.
-/

noncomputable section
set_option autoImplicit false

namespace Stage1Instances.THMM0108

/-- Homogeneous coordinates for finite-dimensional complex projective space. -/
abbrev HomogeneousCoordinates (n : Nat) : Type :=
  Fin (n + 1) -> Complex

/-- The set-theoretic complex projective carrier in dimension `n`. -/
abbrev ComplexProjectiveSpace (n : Nat) : Type :=
  Projectivization Complex (HomogeneousCoordinates n)

/-- Nonzero homogeneous-coordinate vectors. -/
abbrev PuncturedCoordinates (n : Nat) : Type :=
  { v : HomogeneousCoordinates n // v ≠ 0 }

/-- The quotient map from nonzero coordinates to their projective class. -/
def projectivizationMap (n : Nat) :
    PuncturedCoordinates n -> ComplexProjectiveSpace n :=
  fun v => Projectivization.mk' Complex v

/-- Closedness in projective space, expressed through the quotient preimage. -/
def IsProjectivelyClosed {n : Nat} (Z : Set (ComplexProjectiveSpace n)) : Prop :=
  IsClosed (projectivizationMap n ⁻¹' Z)

/-- A reduced complex-analytic projective subset. Around each nonzero
homogeneous coordinate vector, its quotient preimage is the common zero locus
of finitely many analytic functions. -/
def IsComplexAnalyticProjectiveSubset {n : Nat}
    (Z : Set (ComplexProjectiveSpace n)) : Prop :=
  ∀ v : PuncturedCoordinates n,
    projectivizationMap n v ∈ Z ->
      ∃ (U : Set (HomogeneousCoordinates n))
        (m : Nat) (f : Fin m -> HomogeneousCoordinates n -> Complex),
        IsOpen U /\
        (v : HomogeneousCoordinates n) ∈ U /\
        (∀ i, AnalyticOnNhd Complex (f i) U) /\
        ∀ w : PuncturedCoordinates n,
          (w : HomogeneousCoordinates n) ∈ U ->
            (projectivizationMap n w ∈ Z <-> ∀ i, f i w = 0)

/-- The complete reduced analytic input boundary for Chow's theorem. -/
def IsClosedComplexAnalyticProjectiveSubset {n : Nat}
    (Z : Set (ComplexProjectiveSpace n)) : Prop :=
  IsProjectivelyClosed Z /\ IsComplexAnalyticProjectiveSubset Z

/-- A fixed family of homogeneous equations cuts out exactly `Z`. -/
def HomogeneousEquationsCutOut {n : Nat}
    (equations : Set (MvPolynomial (Fin (n + 1)) Complex))
    (Z : Set (ComplexProjectiveSpace n)) : Prop :=
  (∀ p, p ∈ equations -> ∃ degree : Nat, p.IsHomogeneous degree) /\
  ∀ v : PuncturedCoordinates n,
    (projectivizationMap n v ∈ Z <->
      ∀ p, p ∈ equations ->
        MvPolynomial.eval (v : HomogeneousCoordinates n) p = 0)

/-- `Z` is the simultaneous projective zero locus of homogeneous complex
polynomials. -/
def IsHomogeneousPolynomialCutOut {n : Nat}
    (Z : Set (ComplexProjectiveSpace n)) : Prop :=
  ∃ equations : Set (MvPolynomial (Fin (n + 1)) Complex),
    HomogeneousEquationsCutOut equations Z

/-- Chow's theorem in its reduced, set-theoretic carrier formulation: every
closed complex-analytic subset of finite-dimensional complex projective space
is algebraic. Dimension zero and the empty and full subsets are included. -/
def ChowTheoremTarget : Prop :=
  ∀ (n : Nat) (Z : Set (ComplexProjectiveSpace n)),
    IsClosedComplexAnalyticProjectiveSubset Z ->
      IsHomogeneousPolynomialCutOut Z

/-! The following four declarations are deliberately non-equivalent statement
mutations. They are elaborated but never credited as theorem targets. -/

/-- Mutation: closedness has been removed from the analytic hypothesis. -/
def mutationRemovedClosedness : Prop :=
  ∀ (n : Nat) (Z : Set (ComplexProjectiveSpace n)),
    IsComplexAnalyticProjectiveSubset Z -> IsHomogeneousPolynomialCutOut Z

/-- An affine analytic subset, used only to express the changed-domain
mutation without weakening the native mathematical content of analyticity. -/
def IsComplexAnalyticAffineSubset {n : Nat}
    (Z : Set (HomogeneousCoordinates n)) : Prop :=
  ∀ v, v ∈ Z ->
    ∃ (U : Set (HomogeneousCoordinates n))
      (m : Nat) (f : Fin m -> HomogeneousCoordinates n -> Complex),
      IsOpen U /\ v ∈ U /\
      (∀ i, AnalyticOnNhd Complex (f i) U) /\
      ∀ w, w ∈ U -> (w ∈ Z <-> ∀ i, f i w = 0)

/-- Mutation: the ambient domain has been changed from projective to affine
space, and arbitrary rather than homogeneous equations are used. -/
def mutationChangedDomain : Prop :=
  ∀ (n : Nat) (Z : Set (HomogeneousCoordinates n)),
    IsClosed Z -> IsComplexAnalyticAffineSubset Z ->
      ∃ equations : Set (MvPolynomial (Fin (n + 1)) Complex),
        ∀ v, v ∈ Z <->
          ∀ p, p ∈ equations -> MvPolynomial.eval v p = 0

/-- Mutation: one equation family is moved outside the binder for `Z`. -/
def mutationChangedBinderScope : Prop :=
  ∀ n : Nat,
    ∃ equations : Set (MvPolynomial (Fin (n + 1)) Complex),
      ∀ Z : Set (ComplexProjectiveSpace n),
        IsClosedComplexAnalyticProjectiveSubset Z ->
          HomogeneousEquationsCutOut equations Z

/-- Mutation: the dimension-zero boundary case has been excluded. -/
def mutationExcludedDimensionZero : Prop :=
  ∀ (n : Nat), 0 < n -> ∀ Z : Set (ComplexProjectiveSpace n),
    IsClosedComplexAnalyticProjectiveSubset Z ->
      IsHomogeneousPolynomialCutOut Z

#check_failure
  (rfl : ChowTheoremTarget = mutationRemovedClosedness)
#check_failure
  (rfl : ChowTheoremTarget = mutationChangedDomain)
#check_failure
  (rfl : ChowTheoremTarget = mutationChangedBinderScope)
#check_failure
  (rfl : ChowTheoremTarget = mutationExcludedDimensionZero)

set_option pp.universes true in
set_option pp.all true in
#print Stage1Instances.THMM0108.ChowTheoremTarget

set_option pp.universes true in
set_option pp.all true in
#print Stage1Instances.THMM0108.mutationRemovedClosedness

set_option pp.universes true in
set_option pp.all true in
#print Stage1Instances.THMM0108.mutationChangedDomain

set_option pp.universes true in
set_option pp.all true in
#print Stage1Instances.THMM0108.mutationChangedBinderScope

set_option pp.universes true in
set_option pp.all true in
#print Stage1Instances.THMM0108.mutationExcludedDimensionZero

#print axioms Stage1Instances.THMM0108.ChowTheoremTarget
#print axioms Stage1Instances.THMM0108.IsComplexAnalyticProjectiveSubset
#print axioms Stage1Instances.THMM0108.IsHomogeneousPolynomialCutOut

end Stage1Instances.THMM0108
