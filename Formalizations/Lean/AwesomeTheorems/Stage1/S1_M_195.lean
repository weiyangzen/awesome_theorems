import Mathlib.Analysis.Calculus.DifferentialForm.Basic
import Mathlib.Analysis.InnerProductSpace.Laplacian
import Mathlib.MeasureTheory.Integral.DivergenceTheorem
import Mathlib.Analysis.Distribution.DerivNotation
import Mathlib.Analysis.Distribution.TestFunction
import Mathlib.Analysis.Distribution.TemperedDistribution

/-!
# S1-M-195 / THM-M-1527: Maxwell equations

This Stage1 artifact records statement-shape interfaces for Maxwell's
equations in Lean 4.  The source item is a physics formulation, so the local
formal boundary is an abstract mathematical model:

* a classical vector-calculus interface, together with concrete Euclidean
  `ℝ^3` operators built from `fderiv`;
* a differential-form interface using mathlib's exterior derivative `extDeriv`,
  with the Hodge star kept as model data because the current repo-local
  dependency closure has no terminal Lorentzian Hodge-star electromagnetic API.

The checked declarations below are wrappers around the chosen statement shapes
and existing mathlib differential-form facts.  They do not claim a terminal
formal proof of electrodynamics from physical postulates.
-/

noncomputable section

open scoped BigOperators Topology InnerProductSpace

namespace AwesomeTheorems.Stage1.S1_M_195

universe u v

/-- A scalar field on a space. -/
abbrev ScalarField (Space : Type u) := Space -> ℝ

/-- A vector field on a real normed vector space. -/
abbrev VectorField (Space : Type u) := Space -> Space

/-- A time-dependent scalar field. -/
abbrev TimeScalarField (Space : Type u) := ℝ -> ScalarField Space

/-- A time-dependent vector field. -/
abbrev TimeVectorField (Space : Type u) := ℝ -> VectorField Space

/-- The concrete Euclidean three-space used by the repo-local classical operator API. -/
abbrev Euclidean3 := Fin 3 -> ℝ

/--
Abstract vector-calculus operators needed to state the classical Maxwell
equations.  The analytic meaning of these operators is deliberately not baked
into this structure; later work must instantiate it from concrete differentiable
or distributional APIs.
-/
structure ClassicalMaxwellOperators
    (Space : Type u) [NormedAddCommGroup Space] [NormedSpace ℝ Space] where
  div : VectorField Space -> ScalarField Space
  curl : VectorField Space -> VectorField Space
  timeDerivVector : TimeVectorField Space -> TimeVectorField Space
  timeDerivScalar : TimeScalarField Space -> TimeScalarField Space

section ConcreteClassicalOperators

/--
Concrete divergence on `ℝ^3`, expressed as the trace of the Fréchet derivative
in the standard coordinate basis.
-/
def concreteDiv (field : VectorField Euclidean3) : ScalarField Euclidean3 :=
  fun x => ∑ i : Fin 3, fderiv ℝ field x (Pi.single i 1) i

/--
Concrete curl on `ℝ^3`, using the standard coordinate formula
`(∂₂F₃ - ∂₃F₂, ∂₃F₁ - ∂₁F₃, ∂₁F₂ - ∂₂F₁)`.
-/
def concreteCurl (field : VectorField Euclidean3) : VectorField Euclidean3 :=
  fun x i =>
    if i = (0 : Fin 3) then
      fderiv ℝ field x (Pi.single (1 : Fin 3) 1) (2 : Fin 3) -
        fderiv ℝ field x (Pi.single (2 : Fin 3) 1) (1 : Fin 3)
    else if i = (1 : Fin 3) then
      fderiv ℝ field x (Pi.single (2 : Fin 3) 1) (0 : Fin 3) -
        fderiv ℝ field x (Pi.single (0 : Fin 3) 1) (2 : Fin 3)
    else
      fderiv ℝ field x (Pi.single (0 : Fin 3) 1) (1 : Fin 3) -
        fderiv ℝ field x (Pi.single (1 : Fin 3) 1) (0 : Fin 3)

/-- Concrete time derivative for time-dependent vector fields on `ℝ^3`. -/
def concreteTimeDerivVector
    (field : TimeVectorField Euclidean3) : TimeVectorField Euclidean3 :=
  fun t x => fderiv ℝ (fun τ : ℝ => field τ x) t 1

/-- Concrete time derivative for time-dependent scalar fields on `ℝ^3`. -/
def concreteTimeDerivScalar
    (field : TimeScalarField Euclidean3) : TimeScalarField Euclidean3 :=
  fun t x => fderiv ℝ (fun τ : ℝ => field τ x) t 1

/--
Concrete `ℝ^3` instance of the classical Maxwell operator interface.

This is not a terminal proof of the physical Maxwell equations; it replaces the
operator placeholder for the classical statement shape with repo-local
definitions built from mathlib's Fréchet derivative.
-/
def concreteClassicalMaxwellOperators : ClassicalMaxwellOperators Euclidean3 where
  div := concreteDiv
  curl := concreteCurl
  timeDerivVector := concreteTimeDerivVector
  timeDerivScalar := concreteTimeDerivScalar

/-- Checked bridge from the classical operator interface to concrete Euclidean divergence. -/
theorem concreteClassicalMaxwellOperators_div :
    concreteClassicalMaxwellOperators.div = concreteDiv :=
  rfl

/-- Checked bridge from the classical operator interface to concrete Euclidean curl. -/
theorem concreteClassicalMaxwellOperators_curl :
    concreteClassicalMaxwellOperators.curl = concreteCurl :=
  rfl

/-- Checked bridge from the classical operator interface to the concrete vector time derivative. -/
theorem concreteClassicalMaxwellOperators_timeDerivVector :
    concreteClassicalMaxwellOperators.timeDerivVector = concreteTimeDerivVector :=
  rfl

/-- Checked bridge from the classical operator interface to the concrete scalar time derivative. -/
theorem concreteClassicalMaxwellOperators_timeDerivScalar :
    concreteClassicalMaxwellOperators.timeDerivScalar = concreteTimeDerivScalar :=
  rfl

end ConcreteClassicalOperators

/-- Physical constants appearing in the SI-style classical Maxwell equations. -/
structure ClassicalMaxwellConstants where
  epsilon0 : ℝ
  mu0 : ℝ

/-- The electromagnetic fields and source terms in classical vector form. -/
structure ClassicalMaxwellFields
    (Space : Type u) [NormedAddCommGroup Space] [NormedSpace ℝ Space] where
  electricField : TimeVectorField Space
  magneticField : TimeVectorField Space
  chargeDensity : TimeScalarField Space
  currentDensity : TimeVectorField Space

section Classical

variable {Space : Type u} [NormedAddCommGroup Space] [NormedSpace ℝ Space]
variable (ops : ClassicalMaxwellOperators Space)
variable (constants : ClassicalMaxwellConstants)
variable (fields : ClassicalMaxwellFields Space)

/-- Gauss's law for the electric field. -/
def GaussElectricEquation : Prop :=
  ∀ t x, ops.div (fields.electricField t) x =
    fields.chargeDensity t x / constants.epsilon0

/-- Gauss's law for magnetism. -/
def GaussMagneticEquation : Prop :=
  ∀ t x, ops.div (fields.magneticField t) x = 0

/-- Faraday's induction law. -/
def FaradayEquation : Prop :=
  ∀ t x, ops.curl (fields.electricField t) x =
    - ops.timeDerivVector fields.magneticField t x

/-- Ampere-Maxwell law. -/
def AmpereMaxwellEquation : Prop :=
  ∀ t x, ops.curl (fields.magneticField t) x =
    constants.mu0 • fields.currentDensity t x +
      (constants.mu0 * constants.epsilon0) • ops.timeDerivVector fields.electricField t x

/-- The four classical Maxwell equations as a statement-shape predicate. -/
structure IsClassicalMaxwellSolution : Prop where
  gaussElectric : GaussElectricEquation ops constants fields
  gaussMagnetic : GaussMagneticEquation ops fields
  faraday : FaradayEquation ops fields
  ampereMaxwell : AmpereMaxwellEquation ops constants fields

/-- A packaged version of the classical Maxwell system. -/
def ClassicalStatementShape : Prop :=
  ∀ (ops : ClassicalMaxwellOperators Space)
    (constants : ClassicalMaxwellConstants)
    (fields : ClassicalMaxwellFields Space),
    IsClassicalMaxwellSolution ops constants fields ->
      GaussElectricEquation ops constants fields ∧
        GaussMagneticEquation ops fields ∧
          FaradayEquation ops fields ∧
            AmpereMaxwellEquation ops constants fields

/-- Checked wrapper projecting Gauss's electric law from the packaged solution predicate. -/
theorem classical_gaussElectric
    (h : IsClassicalMaxwellSolution ops constants fields) :
    GaussElectricEquation ops constants fields :=
  h.gaussElectric

/-- Checked wrapper projecting Gauss's magnetic law from the packaged solution predicate. -/
theorem classical_gaussMagnetic
    (h : IsClassicalMaxwellSolution ops constants fields) :
    GaussMagneticEquation ops fields :=
  h.gaussMagnetic

/-- Checked wrapper projecting Faraday's law from the packaged solution predicate. -/
theorem classical_faraday
    (h : IsClassicalMaxwellSolution ops constants fields) :
    FaradayEquation ops fields :=
  h.faraday

/-- Checked wrapper projecting the Ampere-Maxwell law from the packaged solution predicate. -/
theorem classical_ampereMaxwell
    (h : IsClassicalMaxwellSolution ops constants fields) :
    AmpereMaxwellEquation ops constants fields :=
  h.ampereMaxwell

/-- The classical statement shape is witnessed by the packaged four-equation predicate. -/
theorem classicalStatementShape_checked :
    ClassicalStatementShape (Space := Space) := by
  intro ops constants fields h
  exact ⟨h.gaussElectric, h.gaussMagnetic, h.faraday, h.ampereMaxwell⟩

end Classical

section DifferentialForms

variable {Spacetime : Type u} [NormedAddCommGroup Spacetime] [NormedSpace ℝ Spacetime]

/-- An unbundled real-valued differential form on a normed vector space. -/
abbrev DifferentialForm (Spacetime : Type u) [NormedAddCommGroup Spacetime]
    [NormedSpace ℝ Spacetime] (degree : ℕ) :=
  Spacetime -> Spacetime [⋀^Fin degree]→L[ℝ] ℝ

/--
Signature convention selected for the relativistic differential-form Maxwell
branch.  The chosen convention is the four-dimensional Lorentzian
`(-,+,+,+)` convention; it is recorded as data because the current local
mathlib closure has no geometric Hodge-star API to import.
-/
inductive RelativisticSignatureConvention where
  | lorentzianMostlyPlusFour
deriving DecidableEq, Repr

/-- Orientation convention selected for the relativistic Hodge-star branch. -/
inductive RelativisticOrientationConvention where
  | spacetimeOrientation
deriving DecidableEq, Repr

/--
A repo-local Hodge-star choice for two-forms in the relativistic Maxwell model.

The `metric` field is an explicit model token for the selected metric.  The
operator field is the two-form Hodge star supplied by that metric/orientation
choice.  This structure is not a construction theorem for the Lorentzian
Hodge star; it is the checked API boundary until a concrete mathlib or pinned
external geometric construction is available.
-/
structure RelativisticHodgeStarChoice where
  metric : Spacetime -> Spacetime -> Spacetime -> ℝ
  orientation : RelativisticOrientationConvention
  signature : RelativisticSignatureConvention
  hodgeStarOnTwoForms : DifferentialForm Spacetime 2 -> DifferentialForm Spacetime 2
  orientation_selected : orientation = RelativisticOrientationConvention.spacetimeOrientation
  signature_selected : signature = RelativisticSignatureConvention.lorentzianMostlyPlusFour

/--
Differential-form data for a relativistic Maxwell model.

In four-dimensional Lorentzian geometry, Maxwell's equations are usually
written as `dF = 0` and `d(*F) = J`.  This Stage1 file uses mathlib's
`extDeriv` for `d`, while the Hodge-star operator on two-forms is kept as data.
-/
structure RelativisticMaxwellData where
  fieldStrength : DifferentialForm Spacetime 2
  current : DifferentialForm Spacetime 3
  hodgeStarOnTwoForms : DifferentialForm Spacetime 2 -> DifferentialForm Spacetime 2
  constitutiveLaw : Prop
  currentConservationInput : Prop

/--
Build relativistic Maxwell data from an explicit Hodge-star choice.

This is the repo-local connection required by the Hodge-star API child task:
the model's `hodgeStarOnTwoForms` field is definitionally the operator stored
in the selected metric/orientation/signature choice.
-/
def RelativisticMaxwellData.ofHodgeStarChoice
    (fieldStrength : DifferentialForm Spacetime 2)
    (current : DifferentialForm Spacetime 3)
    (hodgeChoice : RelativisticHodgeStarChoice (Spacetime := Spacetime))
    (constitutiveLaw currentConservationInput : Prop) :
    RelativisticMaxwellData (Spacetime := Spacetime) where
  fieldStrength := fieldStrength
  current := current
  hodgeStarOnTwoForms := hodgeChoice.hodgeStarOnTwoForms
  constitutiveLaw := constitutiveLaw
  currentConservationInput := currentConservationInput

/-- Predicate recording that a model uses the selected Hodge-star choice. -/
def UsesHodgeStarChoice
    (hodgeChoice : RelativisticHodgeStarChoice (Spacetime := Spacetime))
    (model : RelativisticMaxwellData (Spacetime := Spacetime)) : Prop :=
  model.hodgeStarOnTwoForms = hodgeChoice.hodgeStarOnTwoForms

/-- Checked bridge from `RelativisticMaxwellData` to the selected Hodge-star operator. -/
theorem ofHodgeStarChoice_hodgeStarOnTwoForms
    (fieldStrength : DifferentialForm Spacetime 2)
    (current : DifferentialForm Spacetime 3)
    (hodgeChoice : RelativisticHodgeStarChoice (Spacetime := Spacetime))
    (constitutiveLaw currentConservationInput : Prop) :
    (RelativisticMaxwellData.ofHodgeStarChoice
      (Spacetime := Spacetime)
      fieldStrength current hodgeChoice constitutiveLaw currentConservationInput).hodgeStarOnTwoForms =
        hodgeChoice.hodgeStarOnTwoForms :=
  rfl

/-- Checked bridge that the constructed model uses the selected Hodge-star choice. -/
theorem ofHodgeStarChoice_usesHodgeStarChoice
    (fieldStrength : DifferentialForm Spacetime 2)
    (current : DifferentialForm Spacetime 3)
    (hodgeChoice : RelativisticHodgeStarChoice (Spacetime := Spacetime))
    (constitutiveLaw currentConservationInput : Prop) :
    UsesHodgeStarChoice hodgeChoice
      (RelativisticMaxwellData.ofHodgeStarChoice
        (Spacetime := Spacetime)
        fieldStrength current hodgeChoice constitutiveLaw currentConservationInput) :=
  rfl

/-- The homogeneous Maxwell equation `dF = 0`. -/
def HomogeneousEquation (model : RelativisticMaxwellData (Spacetime := Spacetime)) : Prop :=
  ∀ x, extDeriv model.fieldStrength x = 0

/-- The inhomogeneous Maxwell equation `d(*F) = J`. -/
def InhomogeneousEquation (model : RelativisticMaxwellData (Spacetime := Spacetime)) : Prop :=
  ∀ x, extDeriv (model.hodgeStarOnTwoForms model.fieldStrength) x = model.current x

/-- The inhomogeneous equation for a model built from a selected Hodge-star choice. -/
theorem inhomogeneousEquation_ofHodgeStarChoice_iff
    (fieldStrength : DifferentialForm Spacetime 2)
    (current : DifferentialForm Spacetime 3)
    (hodgeChoice : RelativisticHodgeStarChoice (Spacetime := Spacetime))
    (constitutiveLaw currentConservationInput : Prop) :
    InhomogeneousEquation
      (RelativisticMaxwellData.ofHodgeStarChoice
        (Spacetime := Spacetime)
        fieldStrength current hodgeChoice constitutiveLaw currentConservationInput) ↔
      ∀ x, extDeriv (hodgeChoice.hodgeStarOnTwoForms fieldStrength) x = current x :=
  Iff.rfl

/-- A packaged solution predicate for the differential-form Maxwell system. -/
structure IsRelativisticMaxwellSolution
    (model : RelativisticMaxwellData (Spacetime := Spacetime)) : Prop where
  homogeneous : HomogeneousEquation model
  inhomogeneous : InhomogeneousEquation model
  constitutiveLaw : model.constitutiveLaw
  currentConservationInput : model.currentConservationInput

/-- Differential-form statement shape for Maxwell's equations. -/
def RelativisticStatementShape : Prop :=
  ∀ model : RelativisticMaxwellData (Spacetime := Spacetime),
    IsRelativisticMaxwellSolution model ->
      HomogeneousEquation model ∧ InhomogeneousEquation model

/-- Checked wrapper projecting `dF = 0` from the differential-form solution predicate. -/
theorem relativistic_homogeneous
    {model : RelativisticMaxwellData (Spacetime := Spacetime)}
    (h : IsRelativisticMaxwellSolution model) :
    HomogeneousEquation model :=
  h.homogeneous

/-- Checked wrapper projecting `d(*F) = J` from the differential-form solution predicate. -/
theorem relativistic_inhomogeneous
    {model : RelativisticMaxwellData (Spacetime := Spacetime)}
    (h : IsRelativisticMaxwellSolution model) :
    InhomogeneousEquation model :=
  h.inhomogeneous

/-- The differential-form statement shape is witnessed by the packaged solution predicate. -/
theorem relativisticStatementShape_checked :
    RelativisticStatementShape (Spacetime := Spacetime) := by
  intro model h
  exact ⟨h.homogeneous, h.inhomogeneous⟩

/-- Checked mathlib anchor: the exterior derivative squares to zero under smoothness. -/
theorem exteriorDerivative_square_zero
    {degree : ℕ} {r : WithTop ℕ∞} {ω : DifferentialForm Spacetime degree}
    (hω : ContDiff ℝ r ω) (hr : minSmoothness ℝ 2 ≤ r) :
    extDeriv (extDeriv ω) = 0 :=
  extDeriv_extDeriv hω hr

/-- Checked mathlib anchor: exterior derivative commutes with scalar multiplication. -/
theorem exteriorDerivative_smul
    {degree : ℕ} (c : ℝ) (ω : DifferentialForm Spacetime degree) (x : Spacetime) :
    extDeriv (c • ω) x = c • extDeriv ω x :=
  extDeriv_smul c ω

end DifferentialForms

section SourceConservation

variable {Space : Type u} [NormedAddCommGroup Space] [NormedSpace ℝ Space]
variable {Spacetime : Type v} [NormedAddCommGroup Spacetime] [NormedSpace ℝ Spacetime]

/--
The two current-conservation branches considered by the Stage1 Maxwell slot.

This child selects the relativistic differential-form branch `dJ = 0`.  The
classical continuity equation remains available as a bridge target once the
coordinate equivalence between the classical and relativistic systems is built.
-/
inductive SourceConservationBranch where
  | relativisticClosedCurrent
  | classicalContinuityEquation
deriving DecidableEq, Repr

/-- Repo-local branch choice for `THM-M-1527.source-conservation`. -/
def chosenSourceConservationBranch : SourceConservationBranch :=
  .relativisticClosedCurrent

/-- Checked wrapper recording the source-conservation branch choice. -/
theorem chosenSourceConservationBranch_checked :
    chosenSourceConservationBranch = SourceConservationBranch.relativisticClosedCurrent :=
  rfl

/--
The classical charge-current continuity equation
`∂rho/∂t + div J = 0`, stated using the current operator interface.
-/
def ClassicalContinuityEquation
    (ops : ClassicalMaxwellOperators Space)
    (fields : ClassicalMaxwellFields Space) : Prop :=
  ∀ t x,
    ops.timeDerivScalar fields.chargeDensity t x +
      ops.div (fields.currentDensity t) x = 0

/-- The selected relativistic current-conservation equation `dJ = 0`. -/
def RelativisticCurrentConservationEquation
    (model : RelativisticMaxwellData (Spacetime := Spacetime)) : Prop :=
  ∀ x, extDeriv model.current x = 0

/--
Current conservation from the inhomogeneous Maxwell equation.

If `d(*F) = J` and the source potential `*F` has the smoothness required by
mathlib's `extDeriv_extDeriv`, then `dJ = d(d(*F)) = 0`.
-/
theorem relativistic_currentConservation_from_inhomogeneous
    {model : RelativisticMaxwellData (Spacetime := Spacetime)}
    {r : WithTop ℕ∞}
    (hInhomogeneous : InhomogeneousEquation model)
    (hSmooth : ContDiff ℝ r (model.hodgeStarOnTwoForms model.fieldStrength))
    (hr : minSmoothness ℝ 2 ≤ r) :
    RelativisticCurrentConservationEquation model := by
  intro x
  have hCurrent :
      model.current = extDeriv (model.hodgeStarOnTwoForms model.fieldStrength) := by
    funext y
    exact (hInhomogeneous y).symm
  rw [hCurrent]
  simpa using congrFun (extDeriv_extDeriv hSmooth hr) x

/--
Current conservation projected from a packaged relativistic solution, with the
same smoothness side condition required by `extDeriv_extDeriv`.
-/
theorem relativistic_solution_currentConservation
    {model : RelativisticMaxwellData (Spacetime := Spacetime)}
    {r : WithTop ℕ∞}
    (h : IsRelativisticMaxwellSolution model)
    (hSmooth : ContDiff ℝ r (model.hodgeStarOnTwoForms model.fieldStrength))
    (hr : minSmoothness ℝ 2 ≤ r) :
    RelativisticCurrentConservationEquation model :=
  relativistic_currentConservation_from_inhomogeneous
    h.inhomogeneous hSmooth hr

end SourceConservation

section ClassicalRelativisticBridge

variable {Spacetime : Type u} [NormedAddCommGroup Spacetime] [NormedSpace ℝ Spacetime]

/--
Explicit unit and sign conventions needed before a coordinate comparison between
the classical vector equations and the relativistic differential-form equations
can be meaningful.

The scalar fields are intentionally data, not hidden defaults: later work must
instantiate them with the selected SI/geometric-unit normalization, temporal
coordinate scale, field-strength sign, Hodge-star sign, and source-current
normalization.
-/
structure ClassicalRelativisticConventions
    (constants : ClassicalMaxwellConstants) where
  vacuumPermittivity : ℝ
  vacuumPermeability : ℝ
  speedOfLight : ℝ
  temporalCoordinateScale : ℝ
  electricFieldScale : ℝ
  magneticFieldScale : ℝ
  chargeDensityScale : ℝ
  currentDensityScale : ℝ
  fieldStrengthSign : ℝ
  hodgeStarSign : ℝ
  sourceThreeFormSign : ℝ
  orientation : RelativisticOrientationConvention
  signature : RelativisticSignatureConvention
  vacuumPermittivity_matches : vacuumPermittivity = constants.epsilon0
  vacuumPermeability_matches : vacuumPermeability = constants.mu0
  orientation_selected : orientation = RelativisticOrientationConvention.spacetimeOrientation
  signature_selected : signature = RelativisticSignatureConvention.lorentzianMostlyPlusFour

/-- The two differential-form Maxwell equations, separated from auxiliary model hypotheses. -/
def DifferentialFormMaxwellEquations
    (model : RelativisticMaxwellData (Spacetime := Spacetime)) : Prop :=
  HomogeneousEquation model ∧ InhomogeneousEquation model

/--
Coordinate-realization obligations for the classical/relativistic bridge.

These fields are proposition slots rather than theorem claims.  They mark the
missing analytic construction: a spacetime coordinate chart, formulas turning
`E`, `B`, `rho`, and `J` into `F` and the source three-form, and compatibility
with the chosen Hodge-star/units/sign conventions.
-/
structure ClassicalRelativisticCoordinateRealization
    (constants : ClassicalMaxwellConstants)
    (fields : ClassicalMaxwellFields Euclidean3)
    (model : RelativisticMaxwellData (Spacetime := Spacetime)) where
  conventions : ClassicalRelativisticConventions constants
  fieldStrength_realizes_electric_magnetic_fields : Prop
  sourceThreeForm_realizes_charge_current_densities : Prop
  hodgeStar_realizes_selected_metric_orientation_signature : Prop
  coordinate_derivatives_realize_div_curl_timeDeriv : Prop
  units_and_signs_are_compatible :
    fieldStrength_realizes_electric_magnetic_fields →
      sourceThreeForm_realizes_charge_current_densities →
        hodgeStar_realizes_selected_metric_orientation_signature →
          coordinate_derivatives_realize_div_curl_timeDeriv → Prop

/--
The explicit compatibility witness demanded by the coordinate bridge.

This keeps the bridge gate stronger than an anchor-only checklist: a realization
does not pass merely by naming the four obligations; it must provide witnesses
for the field/source/Hodge/derivative realizations and satisfy the selected
unit and sign compatibility predicate.
-/
def ClassicalRelativisticCoordinateRealization.UnitSignCompatibility
    {constants : ClassicalMaxwellConstants}
    {fields : ClassicalMaxwellFields Euclidean3}
    {model : RelativisticMaxwellData (Spacetime := Spacetime)}
    (realization :
      ClassicalRelativisticCoordinateRealization constants fields model) : Prop :=
  ∃ hF : realization.fieldStrength_realizes_electric_magnetic_fields,
  ∃ hJ : realization.sourceThreeForm_realizes_charge_current_densities,
  ∃ hH : realization.hodgeStar_realizes_selected_metric_orientation_signature,
  ∃ hD : realization.coordinate_derivatives_realize_div_curl_timeDeriv,
    realization.units_and_signs_are_compatible hF hJ hH hD

/--
Coordinate-realization package with the unit/sign/coordinate compatibility
witness made explicit.
-/
structure VerifiedClassicalRelativisticCoordinateRealization
    (constants : ClassicalMaxwellConstants)
    (fields : ClassicalMaxwellFields Euclidean3)
    (model : RelativisticMaxwellData (Spacetime := Spacetime)) where
  realization : ClassicalRelativisticCoordinateRealization constants fields model
  unitSignCompatibility : realization.UnitSignCompatibility

/-- Checked projection of the explicit unit/sign compatibility gate. -/
theorem verifiedCoordinateRealization_unitSignCompatibility
    {constants : ClassicalMaxwellConstants}
    {fields : ClassicalMaxwellFields Euclidean3}
    {model : RelativisticMaxwellData (Spacetime := Spacetime)}
    (realization :
      VerifiedClassicalRelativisticCoordinateRealization constants fields model) :
    realization.realization.UnitSignCompatibility :=
  realization.unitSignCompatibility

/--
The target equivalence for `THM-M-1527.classical-relativistic-bridge`: the four
classical equations with the repo-local concrete Euclidean operators are
equivalent to the two differential-form equations for the chosen relativistic
model.
-/
def ClassicalRelativisticEquivalence
    (constants : ClassicalMaxwellConstants)
    (fields : ClassicalMaxwellFields Euclidean3)
    (model : RelativisticMaxwellData (Spacetime := Spacetime)) : Prop :=
  IsClassicalMaxwellSolution concreteClassicalMaxwellOperators constants fields ↔
    DifferentialFormMaxwellEquations model

/--
Integration-ready package for a completed coordinate bridge.

This structure avoids treating an anchor-only bridge as complete: a value of
this type must contain both the coordinate-realization obligations and the
actual classical/differential-form equivalence theorem for that realization.
-/
structure CoordinateClassicalRelativisticBridge
    (constants : ClassicalMaxwellConstants)
    (fields : ClassicalMaxwellFields Euclidean3)
    (model : RelativisticMaxwellData (Spacetime := Spacetime)) where
  realization : ClassicalRelativisticCoordinateRealization constants fields model
  equivalence : ClassicalRelativisticEquivalence constants fields model

/--
Stronger completed bridge package for the child task.

The ordinary `CoordinateClassicalRelativisticBridge` keeps the statement-shape
target available, while this verified package records the full local gate:
realization witnesses, unit/sign compatibility, and the actual equivalence
proof.  The repository does not currently construct a value of this type.
-/
structure VerifiedCoordinateClassicalRelativisticBridge
    (constants : ClassicalMaxwellConstants)
    (fields : ClassicalMaxwellFields Euclidean3)
    (model : RelativisticMaxwellData (Spacetime := Spacetime)) where
  realization :
    VerifiedClassicalRelativisticCoordinateRealization constants fields model
  equivalence : ClassicalRelativisticEquivalence constants fields model

/-- Checked projection of the classical-to-differential-form direction from a bridge package. -/
theorem coordinateBridge_classical_to_differentialForm
    {constants : ClassicalMaxwellConstants}
    {fields : ClassicalMaxwellFields Euclidean3}
    {model : RelativisticMaxwellData (Spacetime := Spacetime)}
    (bridge : CoordinateClassicalRelativisticBridge constants fields model)
    (h : IsClassicalMaxwellSolution concreteClassicalMaxwellOperators constants fields) :
    DifferentialFormMaxwellEquations model :=
  bridge.equivalence.mp h

/-- Checked projection of the differential-form-to-classical direction from a bridge package. -/
theorem coordinateBridge_differentialForm_to_classical
    {constants : ClassicalMaxwellConstants}
    {fields : ClassicalMaxwellFields Euclidean3}
    {model : RelativisticMaxwellData (Spacetime := Spacetime)}
    (bridge : CoordinateClassicalRelativisticBridge constants fields model)
    (h : DifferentialFormMaxwellEquations model) :
    IsClassicalMaxwellSolution concreteClassicalMaxwellOperators constants fields :=
  bridge.equivalence.mpr h

/-- Checked projection of the full coordinate equivalence from a bridge package. -/
theorem coordinateBridge_classical_iff_differentialForm
    {constants : ClassicalMaxwellConstants}
    {fields : ClassicalMaxwellFields Euclidean3}
    {model : RelativisticMaxwellData (Spacetime := Spacetime)}
    (bridge : CoordinateClassicalRelativisticBridge constants fields model) :
    IsClassicalMaxwellSolution concreteClassicalMaxwellOperators constants fields ↔
      DifferentialFormMaxwellEquations model :=
  bridge.equivalence

/-- Checked projection of the explicit unit/sign gate from a verified bridge package. -/
theorem verifiedCoordinateBridge_unitSignCompatibility
    {constants : ClassicalMaxwellConstants}
    {fields : ClassicalMaxwellFields Euclidean3}
    {model : RelativisticMaxwellData (Spacetime := Spacetime)}
    (bridge : VerifiedCoordinateClassicalRelativisticBridge constants fields model) :
    bridge.realization.realization.UnitSignCompatibility :=
  bridge.realization.unitSignCompatibility

/-- Checked projection of the full coordinate equivalence from a verified bridge package. -/
theorem verifiedCoordinateBridge_classical_iff_differentialForm
    {constants : ClassicalMaxwellConstants}
    {fields : ClassicalMaxwellFields Euclidean3}
    {model : RelativisticMaxwellData (Spacetime := Spacetime)}
    (bridge : VerifiedCoordinateClassicalRelativisticBridge constants fields model) :
    IsClassicalMaxwellSolution concreteClassicalMaxwellOperators constants fields ↔
      DifferentialFormMaxwellEquations model :=
  bridge.equivalence

end ClassicalRelativisticBridge

section MathlibAudit

/--
Pinned mathlib revision audited for this Stage1 slot.

This string mirrors the Lake pin; it is a repo-local audit datum, not a proof
that Maxwell's equations have been terminally formalized.
-/
def pinnedMathlibRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- mathlib anchors checked while locating repo-local Maxwell-adjacent APIs. -/
def mathlibAuditAnchors : List String := [
  "extDeriv",
  "extDeriv_extDeriv",
  "extDeriv_smul",
  "InnerProductSpace.laplacianWithin",
  "MeasureTheory.integral_divergence_of_hasFDerivAt_off_countable",
  "LineDeriv.laplacianCLM",
  "TestFunction.fderivCLM",
  "TemperedDistribution.derivCLM",
  "TemperedDistribution.lineDerivOp_apply_apply",
  "TemperedDistribution.laplacianCLM_apply"
]

section LaplacianAnchors

variable {E : Type u} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
  [FiniteDimensional ℝ E]
variable {F : Type v} [NormedAddCommGroup F] [NormedSpace ℝ F]

/-- Checked mathlib anchor: the within-set Laplacian specializes to the global Laplacian. -/
theorem laplacianWithin_univ_anchor (f : E → F) :
    InnerProductSpace.laplacianWithin f Set.univ = Laplacian.laplacian f :=
  InnerProductSpace.laplacianWithin_univ

/-- Checked mathlib anchor: Schwartz-space Laplacian through `LineDeriv.laplacianCLM`. -/
theorem schwartz_laplacianCLM_anchor
    (f : SchwartzMap E F) :
    (LineDeriv.laplacianCLM ℝ E (SchwartzMap E F)) f = Laplacian.laplacian f :=
  SchwartzMap.laplacianCLM_eq ℝ f

end LaplacianAnchors

section DivergenceTheoremAnchor

variable {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]

/-- Checked mathlib anchor: divergence theorem outside a countable exceptional set. -/
theorem integral_divergence_of_hasFDerivAt_off_countable_anchor
    {n : ℕ} (a b : Fin (n + 1) → ℝ) (hle : a ≤ b)
    (f : (Fin (n + 1) → ℝ) → Fin (n + 1) → E)
    (f' : (Fin (n + 1) → ℝ) → (Fin (n + 1) → ℝ) →L[ℝ] Fin (n + 1) → E)
    (s : Set (Fin (n + 1) → ℝ)) (hs : s.Countable)
    (Hc : ContinuousOn f (Set.Icc a b))
    (Hd : ∀ x ∈ (Set.univ.pi fun i => Set.Ioo (a i) (b i)) \ s, HasFDerivAt f (f' x) x)
    (Hi : MeasureTheory.IntegrableOn
      (fun x => ∑ i, (f' x) (Pi.single i 1) i) (Set.Icc a b) MeasureTheory.volume) :
    ∫ (x : Fin (n + 1) → ℝ) in Set.Icc a b, ∑ i, (f' x) (Pi.single i 1) i =
      ∑ i,
        ((∫ (x : Fin n → ℝ) in Set.Icc (a ∘ i.succAbove) (b ∘ i.succAbove),
            f (i.insertNth (b i) x) i) -
          ∫ (x : Fin n → ℝ) in Set.Icc (a ∘ i.succAbove) (b ∘ i.succAbove),
            f (i.insertNth (a i) x) i) :=
  MeasureTheory.integral_divergence_of_hasFDerivAt_off_countable
    a b hle f f' s hs Hc Hd Hi

end DivergenceTheoremAnchor

section TemperedDistributionLaplacian

variable {E : Type u} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
  [FiniteDimensional ℝ E]
variable {F : Type v} [NormedAddCommGroup F] [NormedSpace ℂ F]

/-- Checked mathlib anchor: tempered-distribution Laplacian through `LineDeriv.laplacianCLM`. -/
theorem temperedDistribution_laplacianCLM_anchor
    (T : TemperedDistribution E F) :
    (LineDeriv.laplacianCLM ℂ E (TemperedDistribution E F)) T =
      Laplacian.laplacian T :=
  TemperedDistribution.laplacianCLM_apply T

end TemperedDistributionLaplacian

section DistributionDerivatives

variable {G : Type v} [NormedAddCommGroup G] [NormedSpace ℂ G]

/-- Checked mathlib anchor: one-dimensional derivative of a tempered distribution. -/
theorem temperedDistribution_derivCLM_anchor
    (T : TemperedDistribution ℝ G) (φ : SchwartzMap ℝ ℂ) :
    ((TemperedDistribution.derivCLM G) T) φ =
      T (-(SchwartzMap.derivCLM ℂ ℂ) φ) :=
  TemperedDistribution.derivCLM_apply_apply T φ

/-- Checked mathlib anchor: directional derivative of a tempered distribution. -/
theorem temperedDistribution_lineDeriv_anchor
    {V : Type u} [NormedAddCommGroup V] [NormedSpace ℝ V]
    (T : TemperedDistribution V G) (φ : SchwartzMap V ℂ) (m : V) :
    (LineDeriv.lineDerivOp m T) φ = T (-LineDeriv.lineDerivOp m φ) :=
  TemperedDistribution.lineDerivOp_apply_apply T φ m

end DistributionDerivatives

section TestFunctionDerivatives

variable {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
variable {G : Type v} [NormedAddCommGroup G] [NormedSpace ℝ G] [NormedSpace ℂ G]
  [IsScalarTower ℝ ℂ G]

/-- Checked mathlib anchor: derivative continuous linear map on test functions. -/
theorem testFunction_fderivCLM_anchor
    {Ω : TopologicalSpace.Opens E} {n k : ℕ∞}
    (φ : TestFunction Ω G n) (hk : k + 1 ≤ n) :
    ⇑((TestFunction.fderivCLM ℂ n k) φ) = fderiv ℝ ⇑φ :=
  TestFunction.fderivCLM_apply_of_le φ hk

end TestFunctionDerivatives

end MathlibAudit

/-- Combined Stage1 statement-shape target for this slot. -/
def StatementShape : Prop :=
  (∀ (Space : Type u) [NormedAddCommGroup Space] [NormedSpace ℝ Space],
      ClassicalStatementShape (Space := Space)) ∧
    (∀ (Spacetime : Type u) [NormedAddCommGroup Spacetime] [NormedSpace ℝ Spacetime],
      RelativisticStatementShape (Spacetime := Spacetime))

/-- Checked combined wrapper for the local Stage1 Maxwell statement shapes. -/
theorem statementShape_checked : StatementShape.{u} := by
  constructor
  · intro Space _ _
    exact classicalStatementShape_checked (Space := Space)
  · intro Spacetime _ _
    exact relativisticStatementShape_checked (Spacetime := Spacetime)

/--
The explicit Stage1 variant menu for the Maxwell slot.

The selected branch below is intentionally a theorem-statement choice, not a
claim that Maxwell's equations have been terminally proved in this repository.
-/
inductive FormalTheoremVariant where
  | classicalFourEquationVectorCalculus
  | relativisticDifferentialForms
  | actionPrincipleDerivation
  | weakDistributionalPDE
  | modelSpecificSolutionPredicate
deriving DecidableEq, Repr

/--
Chosen formal theorem variant for `THM-M-1527.variant-choice`.

The local boundary chooses a model-specific solution predicate.  The concrete
model data use the relativistic differential-form equations `dF = 0` and
`d(*F) = J`; the classical four-equation interface is retained as bridge
material rather than as the primary terminal target.
-/
def chosenFormalTheoremVariant : FormalTheoremVariant :=
  .modelSpecificSolutionPredicate

/-- Checked wrapper recording the repo-local variant choice. -/
theorem chosenFormalTheoremVariant_checked :
    chosenFormalTheoremVariant = FormalTheoremVariant.modelSpecificSolutionPredicate :=
  rfl

/--
Primary statement shape for the chosen model-specific branch.

This expands the chosen variant to a relativistic model predicate with
model-supplied Hodge star and constitutive/current-conservation assumptions.
-/
def PrimaryVariantStatementShape : Prop :=
  ∀ (Spacetime : Type u) [NormedAddCommGroup Spacetime] [NormedSpace ℝ Spacetime]
    (model : RelativisticMaxwellData (Spacetime := Spacetime)),
    IsRelativisticMaxwellSolution model ->
      HomogeneousEquation model ∧ InhomogeneousEquation model

/-- Checked wrapper for the chosen primary variant statement shape. -/
theorem primaryVariantStatementShape_checked : PrimaryVariantStatementShape.{u} := by
  intro Spacetime _ _ model h
  exact relativisticStatementShape_checked (Spacetime := Spacetime) model h

/--
Public statement-normalization note for the Stage1 Maxwell slot.

`AwesomeTheorems.Stage1.S1_M_195.StatementShape` is the current repo-local
Lean boundary for `S1-M-195 / THM-M-1527`: it packages abstract classical
four-equation and relativistic differential-form statement shapes, plus
concrete Euclidean `ℝ^3` definitions for classical `div`, `curl`, and time
derivatives, plus a conditional differential-form current-conservation branch.
It is not a terminal proof of Maxwell's equations and it does not yet construct
the Lorentzian Hodge star or the classical/relativistic bridge APIs.
-/
def statementNormalizationNote : String :=
  "AwesomeTheorems.Stage1.S1_M_195.StatementShape is the current repo-local Lean boundary for S1-M-195 / THM-M-1527. It records classical and relativistic statement shapes with checked wrappers, including concrete Euclidean div/curl/time-derivative definitions for the classical operator API and a conditional differential-form current-conservation branch, but it is not a terminal proof of Maxwell's equations."

/-- Integration-ready public note for the variant-choice child task. -/
def variantChoiceNote : String :=
  "THM-M-1527.variant-choice selects a model-specific solution predicate as the primary Lean target, instantiated by the relativistic differential-form equations dF = 0 and d(*F) = J with Hodge star, constitutive law, and current-conservation input kept as explicit model data. The classical four-equation formulation remains bridge material, not the primary completion target."

/-- Integration-ready public note for the source-conservation child task. -/
def sourceConservationNote : String :=
  "THM-M-1527.source-conservation selects the relativistic closed-current branch dJ = 0. Repo-local Lean states it as RelativisticCurrentConservationEquation and proves relativistic_currentConservation_from_inhomogeneous: from d(*F) = J plus the ContDiff/minSmoothness hypotheses needed for mathlib's extDeriv_extDeriv, dJ follows. The classical continuity equation is also stated as ClassicalContinuityEquation for future bridge work, but the terminal Maxwell theorem remains open."

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Analysis.Calculus.DifferentialForm.Basic",
  "Mathlib.Analysis.Calculus.DifferentialForm.VectorField",
  "Mathlib.Geometry.Manifold.MFDeriv.NormedSpace",
  "Mathlib.Geometry.Manifold.VectorBundle.CovariantDerivative.Basic",
  "Mathlib.Analysis.InnerProductSpace.Laplacian",
  "Mathlib.MeasureTheory.Integral.DivergenceTheorem",
  "Mathlib.Analysis.Distribution.DerivNotation",
  "Mathlib.Analysis.Distribution.TestFunction",
  "Mathlib.Analysis.Distribution.TemperedDistribution"
]

/-- Search terms and terminal gaps checked for the Stage1 audit ledger. -/
def anchorSearchTerms : List String := [
  "Maxwell",
  "Electromagnetic",
  "electric",
  "magnetic",
  "Faraday",
  "Ampere",
  "Gauss",
  "Lorentz",
  "curl",
  "divergence",
  "DifferentialForm",
  "extDeriv",
  "Hodge",
  "wave equation"
]

/--
External Lean 4 Maxwell/electromagnetism audit status for `THM-M-1527.external-audit`.

This worker could not run the required authenticated GitHub code search because
the local `gh` client is not logged in and no `GH_TOKEN`/`GITHUB_TOKEN` is
available in the environment.  Consequently this is a concrete audit blocker,
not evidence that no external proof exists and not a completion claim.
-/
def externalLeanMaxwellAuthenticatedSearchAudit : List String := [
  "2026-05-01 gh auth status: not logged into any GitHub hosts",
  "2026-05-01 environment: no GH_TOKEN or GITHUB_TOKEN available",
  "Authenticated GitHub code search for Lean 4 Maxwell/electromagnetism formalizations was not completed in this pass",
  "No external Maxwell/electromagnetism Lean 4 proof was pinned, imported, or checked by this pass",
  "Do not mark THM-M-1527.external-audit complete until authenticated search runs and any exact terminal candidate is pinned/imported/checked locally or blocked by a concrete integration reason"
]

/-- Repo-local external-audit closure flag for the Maxwell slot. -/
def externalLeanMaxwellRepoLocalClosed : Bool :=
  false

/-- Checked status marker: the external Lean Maxwell audit is not repo-local closed. -/
theorem externalLeanMaxwellRepoLocalClosed_eq_false :
    externalLeanMaxwellRepoLocalClosed = false :=
  rfl

/--
Public-status gate for `THM-M-1527.public-status`.

This is checked process metadata, not a terminal proof of Maxwell's equations.
The public Stage1 checkbox may close only when local Lean validation, theorem
tree leaf budgeting, public merge gates, and repo-local theorem/dependency
closure all agree.  Anchor-only evidence is explicitly excluded.
-/
structure PublicStatusGate where
  localLeanValidationPassed : Bool
  theoremTreeLeafBudgetSatisfied : Bool
  publicMergeGatesSatisfied : Bool
  terminalTheoremRepoLocalClosed : Bool
  noCompletedRepoLocalIntegrationDebt : Bool
  anchorOnlyEvidenceUsedAsCompletion : Bool

/-- The public status may close only when every M0387-level gate is satisfied. -/
def PublicStatusGate.publicStatusMayClose (gate : PublicStatusGate) : Bool :=
  gate.localLeanValidationPassed &&
    gate.theoremTreeLeafBudgetSatisfied &&
      gate.publicMergeGatesSatisfied &&
        gate.terminalTheoremRepoLocalClosed &&
          gate.noCompletedRepoLocalIntegrationDebt &&
            !gate.anchorOnlyEvidenceUsedAsCompletion

/--
Current public-status gate for this child pass.

The Lean file validates locally, and this child does not retain a completed
`repo_local_integration_debt` state.  The public theorem-tree leaf budget,
public merge gates, and terminal repo-local Maxwell theorem closure are still
not satisfied, so the public status must remain open.
-/
def currentPublicStatusGate : PublicStatusGate where
  localLeanValidationPassed := true
  theoremTreeLeafBudgetSatisfied := false
  publicMergeGatesSatisfied := false
  terminalTheoremRepoLocalClosed := false
  noCompletedRepoLocalIntegrationDebt := true
  anchorOnlyEvidenceUsedAsCompletion := false

/-- Checked marker: the parent public status is still not allowed to close. -/
theorem currentPublicStatusMayClose_eq_false :
    currentPublicStatusGate.publicStatusMayClose = false :=
  rfl

/-- Checked marker: this child is not using anchor-only evidence as completion evidence. -/
theorem currentPublicStatus_anchorOnlyEvidence_eq_false :
    currentPublicStatusGate.anchorOnlyEvidenceUsedAsCompletion = false :=
  rfl

/-- Checked marker: no completed status in this child retains repo-local integration debt. -/
theorem currentPublicStatus_noCompletedRepoLocalIntegrationDebt_eq_true :
    currentPublicStatusGate.noCompletedRepoLocalIntegrationDebt = true :=
  rfl

/-- Integration-ready public note for the public-status child task. -/
def publicStatusGateNote : String :=
  "THM-M-1527.public-status remains [ ] open. The repo-local Lean file validates as statement-shape/process metadata, and no completed state retains repo_local_integration_debt, but the theorem-tree leaf budget, public merge gates, external-audit closure, and terminal repo-local Maxwell theorem/dependency closure are not all satisfied. Anchor-only evidence is not completion evidence."

end AwesomeTheorems.Stage1.S1_M_195
