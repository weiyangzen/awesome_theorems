import Mathlib.Analysis.Calculus.DifferentialForm.Basic

/-!
# THM-M-1527: exact Maxwell statement boundary

This module freezes the conditional coordinate-equivalence theorem selected by
the rev-5.6 intake.  It states no empirical claim and contains no proof of the
coordinate-decomposition hypotheses.
-/

noncomputable section

namespace Stage1Instances.THM_M_1527

universe u

abbrev Euclidean3 := Fin 3 -> Real
abbrev ScalarField := Euclidean3 -> Real
abbrev VectorField := Euclidean3 -> Euclidean3
abbrev TimeScalarField := Real -> ScalarField
abbrev TimeVectorField := Real -> VectorField

/-- The vector-calculus operations used by the SI component equations. -/
structure ClassicalOperators where
  div : VectorField -> ScalarField
  curl : VectorField -> VectorField
  timeDerivScalar : TimeScalarField -> TimeScalarField
  timeDerivVector : TimeVectorField -> TimeVectorField

/-- SI constants. Positivity is kept in the canonical target as a hypothesis. -/
structure SIConstants where
  epsilon0 : Real
  mu0 : Real

/-- Electric and magnetic fields, charge density, and current density. -/
structure ClassicalFields where
  electric : TimeVectorField
  magnetic : TimeVectorField
  charge : TimeScalarField
  current : TimeVectorField

def GaussElectric (ops : ClassicalOperators) (c : SIConstants)
    (f : ClassicalFields) : Prop :=
  forall t x, ops.div (f.electric t) x = f.charge t x / c.epsilon0

def GaussMagnetic (ops : ClassicalOperators) (f : ClassicalFields) : Prop :=
  forall t x, ops.div (f.magnetic t) x = 0

def Faraday (ops : ClassicalOperators) (f : ClassicalFields) : Prop :=
  forall t x, ops.curl (f.electric t) x = -ops.timeDerivVector f.magnetic t x

def AmpereMaxwell (ops : ClassicalOperators) (c : SIConstants)
    (f : ClassicalFields) : Prop :=
  forall t x, ops.curl (f.magnetic t) x =
    c.mu0 • f.current t x +
      (c.mu0 * c.epsilon0) • ops.timeDerivVector f.electric t x

def ClassicalMaxwellSystem (ops : ClassicalOperators) (c : SIConstants)
    (f : ClassicalFields) : Prop :=
  GaussElectric ops c f /\ GaussMagnetic ops f /\
    Faraday ops f /\ AmpereMaxwell ops c f

/-- Unbundled real differential forms on a normed spacetime model. -/
abbrev DifferentialForm (Spacetime : Type u) [NormedAddCommGroup Spacetime]
    [NormedSpace Real Spacetime] (degree : Nat) :=
  Spacetime -> Spacetime [⋀^Fin degree]→L[Real] Real

inductive SignatureConvention where
  | lorentzianMostlyPlus
deriving DecidableEq

inductive OrientationConvention where
  | spacetimeOrientedAndTimeOriented
deriving DecidableEq

/-- Covariant field/current data. The Lorentzian Hodge star is explicit model data. -/
structure CovariantFields (Spacetime : Type u) [NormedAddCommGroup Spacetime]
    [NormedSpace Real Spacetime] where
  dimension : Nat
  fieldStrength : DifferentialForm Spacetime 2
  current : DifferentialForm Spacetime 3
  hodgeStarOnTwoForms : DifferentialForm Spacetime 2 -> DifferentialForm Spacetime 2
  signature : SignatureConvention
  orientation : OrientationConvention

def Homogeneous {Spacetime : Type u} [NormedAddCommGroup Spacetime]
    [NormedSpace Real Spacetime] (f : CovariantFields Spacetime) : Prop :=
  forall x, extDeriv f.fieldStrength x = 0

def Inhomogeneous {Spacetime : Type u} [NormedAddCommGroup Spacetime]
    [NormedSpace Real Spacetime] (f : CovariantFields Spacetime) : Prop :=
  forall x, extDeriv (f.hodgeStarOnTwoForms f.fieldStrength) x = f.current x

def CovariantMaxwellSystem {Spacetime : Type u} [NormedAddCommGroup Spacetime]
    [NormedSpace Real Spacetime] (f : CovariantFields Spacetime) : Prop :=
  Homogeneous f /\ Inhomogeneous f

/-- The two substantive component-decomposition obligations, separated from
the propositional recombination performed by the eventual root proof. -/
structure CoordinateDecomposition {Spacetime : Type u}
    [NormedAddCommGroup Spacetime] [NormedSpace Real Spacetime]
    (ops : ClassicalOperators) (c : SIConstants) (classical : ClassicalFields)
    (covariant : CovariantFields Spacetime) : Prop where
  homogeneous_iff : Homogeneous covariant <->
    GaussMagnetic ops classical /\ Faraday ops classical
  inhomogeneous_iff : Inhomogeneous covariant <->
    GaussElectric ops c classical /\ AmpereMaxwell ops c classical

/-- Exact target: with positive SI constants and a checked 3+1 coordinate
decomposition, the four classical equations are equivalent to `dF = 0` and
`d(star F) = J`. -/
def MaxwellCoordinateEquivalence : Prop :=
  forall (Spacetime : Type u) [NormedAddCommGroup Spacetime]
    [NormedSpace Real Spacetime]
    (ops : ClassicalOperators) (c : SIConstants) (classical : ClassicalFields)
    (covariant : CovariantFields Spacetime),
      covariant.dimension = 4 ->
      covariant.signature = .lorentzianMostlyPlus ->
      covariant.orientation = .spacetimeOrientedAndTimeOriented ->
      0 < c.epsilon0 -> 0 < c.mu0 ->
      CoordinateDecomposition ops c classical covariant ->
      (ClassicalMaxwellSystem ops c classical <-> CovariantMaxwellSystem covariant)

-- Structural mutations. These elaborate but must fingerprint differently.
def mutationRemovedPositiveConstants : Prop :=
  forall (Spacetime : Type u) [NormedAddCommGroup Spacetime]
    [NormedSpace Real Spacetime]
    (ops : ClassicalOperators) (c : SIConstants) (classical : ClassicalFields)
    (covariant : CovariantFields Spacetime),
      covariant.dimension = 4 ->
      covariant.signature = .lorentzianMostlyPlus ->
      covariant.orientation = .spacetimeOrientedAndTimeOriented ->
      CoordinateDecomposition ops c classical covariant ->
      (ClassicalMaxwellSystem ops c classical <-> CovariantMaxwellSystem covariant)

def mutationChangedSpacetimeDomain : Prop :=
  forall (ops : ClassicalOperators) (c : SIConstants) (classical : ClassicalFields)
    (covariant : CovariantFields Euclidean3),
      covariant.dimension = 4 ->
      covariant.signature = .lorentzianMostlyPlus ->
      covariant.orientation = .spacetimeOrientedAndTimeOriented ->
      0 < c.epsilon0 -> 0 < c.mu0 ->
      CoordinateDecomposition ops c classical covariant ->
      (ClassicalMaxwellSystem ops c classical <-> CovariantMaxwellSystem covariant)

def mutationChangedBinderScope : Prop :=
  forall (Spacetime : Type u) [NormedAddCommGroup Spacetime]
    [NormedSpace Real Spacetime]
    (ops : ClassicalOperators) (c : SIConstants),
      0 < c.epsilon0 -> 0 < c.mu0 ->
      forall (classical : ClassicalFields) (covariant : CovariantFields Spacetime),
        covariant.dimension = 4 ->
        covariant.signature = .lorentzianMostlyPlus ->
        covariant.orientation = .spacetimeOrientedAndTimeOriented ->
        CoordinateDecomposition ops c classical covariant ->
        (ClassicalMaxwellSystem ops c classical <-> CovariantMaxwellSystem covariant)

def mutationOneWayConclusion : Prop :=
  forall (Spacetime : Type u) [NormedAddCommGroup Spacetime]
    [NormedSpace Real Spacetime]
    (ops : ClassicalOperators) (c : SIConstants) (classical : ClassicalFields)
    (covariant : CovariantFields Spacetime),
      covariant.dimension = 4 ->
      covariant.signature = .lorentzianMostlyPlus ->
      covariant.orientation = .spacetimeOrientedAndTimeOriented ->
      0 < c.epsilon0 -> 0 < c.mu0 ->
      CoordinateDecomposition ops c classical covariant ->
      ClassicalMaxwellSystem ops c classical -> CovariantMaxwellSystem covariant

end Stage1Instances.THM_M_1527

set_option pp.explicit true in
#print Stage1Instances.THM_M_1527.MaxwellCoordinateEquivalence

set_option pp.explicit true in
#print Stage1Instances.THM_M_1527.mutationRemovedPositiveConstants

set_option pp.explicit true in
#print Stage1Instances.THM_M_1527.mutationChangedSpacetimeDomain

set_option pp.explicit true in
#print Stage1Instances.THM_M_1527.mutationChangedBinderScope

set_option pp.explicit true in
#print Stage1Instances.THM_M_1527.mutationOneWayConclusion
