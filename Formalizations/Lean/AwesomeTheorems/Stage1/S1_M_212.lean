import Mathlib.Analysis.Calculus.ContDiff.Basic
import Mathlib.Data.Complex.Basic
import Mathlib.LinearAlgebra.BilinearMap

/-!
# S1-M-212 / THM-M-1553: Hirota bilinear method

This Stage1 artifact records a conservative Lean 4 boundary for the Hirota
bilinear method in integrable systems.

The informal theorem says that a nonlinear integrable equation can be rewritten
in tau-function form as a bilinear Hirota equation, and that tau functions
satisfying the associated dispersion relations generate solution families.
The current pinned mathlib snapshot has bilinear-map and differential-calculus
infrastructure, but no terminal API for Hirota `D`-operators, tau functions, KdV
/ KP / Toda bilinear identities, or soliton determinant/Wronskian solutions.

Accordingly this file provides a precise certificate interface.  A concrete
future formalization must instantiate the bilinear operator, dependent-variable
transform, dispersion relation, and PDE bridge; this file only proves that such
a certificate yields transformed nonlinear-equation solutions.
-/

noncomputable section

universe uR uTau uSol uParam

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_212

/--
An abstract bilinear operator on tau objects.

For an actual Hirota formalization, `Tau` should be a concrete function space
and this operator should be the polynomial in Hirota derivatives such as
`P(D_x, D_t)`.
-/
abbrev BilinearOperator (R : Type uR) (Tau : Type uTau)
    [CommSemiring R] [AddCommMonoid Tau] [Module R Tau] :=
  Tau →ₗ[R] Tau →ₗ[R] Tau

variable {R : Type uR} {Tau : Type uTau}
variable [CommSemiring R] [AddCommMonoid Tau] [Module R Tau]

/-- The diagonal bilinear equation `B tau tau = 0`. -/
def TauSolvesBilinearEquation (B : BilinearOperator R Tau) (tau : Tau) : Prop :=
  B tau tau = 0

/-- The zero tau object solves every diagonal bilinear equation. -/
theorem TauSolvesBilinearEquation_zero (B : BilinearOperator R Tau) :
    TauSolvesBilinearEquation B (0 : Tau) := by
  simp [TauSolvesBilinearEquation]

/-- Left additivity of the bundled bilinear Hirota operator. -/
theorem BilinearOperator.map_add_left (B : BilinearOperator R Tau)
    (tau₁ tau₂ sigma : Tau) :
    B (tau₁ + tau₂) sigma = B tau₁ sigma + B tau₂ sigma :=
  LinearMap.map_add₂ B tau₁ tau₂ sigma

/-- Left scalar compatibility of the bundled bilinear Hirota operator. -/
theorem BilinearOperator.map_smul_left (B : BilinearOperator R Tau)
    (c : R) (tau sigma : Tau) :
    B (c • tau) sigma = c • B tau sigma :=
  LinearMap.map_smul₂ B c tau sigma

/-- Right additivity of the bundled bilinear Hirota operator. -/
theorem BilinearOperator.map_add_right (B : BilinearOperator R Tau)
    (tau sigma₁ sigma₂ : Tau) :
    B tau (sigma₁ + sigma₂) = B tau sigma₁ + B tau sigma₂ :=
  (B tau).map_add sigma₁ sigma₂

/-- Right scalar compatibility of the bundled bilinear Hirota operator. -/
theorem BilinearOperator.map_smul_right (B : BilinearOperator R Tau)
    (c : R) (tau sigma : Tau) :
    B tau (c • sigma) = c • B tau sigma :=
  (B tau).map_smul c sigma

/--
Precompose a bundled bilinear operator by linear maps in both tau slots.

This is the reusable bilinearity transport needed for concrete Hirota
operators built from linear differential operators.
-/
def BilinearOperator.precomp (B : BilinearOperator R Tau)
    (L₁ L₂ : Tau →ₗ[R] Tau) : BilinearOperator R Tau where
  toFun tau :=
    { toFun := fun sigma => B (L₁ tau) (L₂ sigma)
      map_add' := by
        intro sigma₁ sigma₂
        rw [L₂.map_add, BilinearOperator.map_add_right]
      map_smul' := by
        intro c sigma
        rw [L₂.map_smul]
        simp }
  map_add' := by
    intro tau₁ tau₂
    ext sigma
    rw [L₁.map_add]
    simp
  map_smul' := by
    intro c tau
    ext sigma
    rw [L₁.map_smul]
    simp

/-- Symmetry predicate for Hirota operators whose differential polynomial is even. -/
def IsSymmetricBilinearOperator (B : BilinearOperator R Tau) : Prop :=
  ∀ tau sigma : Tau, B tau sigma = B sigma tau

/-- A symmetric bilinear operator is unchanged after swapping the two tau inputs. -/
theorem IsSymmetricBilinearOperator.swap
    {B : BilinearOperator R Tau} (hB : IsSymmetricBilinearOperator B)
    (tau sigma : Tau) :
    B sigma tau = B tau sigma :=
  (hB tau sigma).symm

/--
Machine-readable closure status for this Stage1 artifact.

The full Hirota bilinear method remains in `formalization_debt`; this file only
closes an abstract certificate interface.
-/
inductive ClosureStatus where
  | statementBoundaryFormalizationDebt
  deriving DecidableEq, Repr

/--
Fields that must be instantiated by a concrete equation family before the full
Hirota bilinear method can leave `formalization_debt`.
-/
def formalizationDebtRequiredInstantiations : List String := [
  "concrete equation family, for example KdV, KP, or Toda",
  "tau-function space",
  "Hirota D-operator or differential polynomial",
  "dependent-variable transform from tau functions to nonlinear fields",
  "dispersion relation for the chosen tau family",
  "certificate fields: admissibility, bilinear identity, and bilinear-to-nonlinear bridge"
]

/-- Current status of the full method, as opposed to the abstract certificate API. -/
def fullHirotaMethodClosureStatus : ClosureStatus :=
  ClosureStatus.statementBoundaryFormalizationDebt

/-- The current file deliberately retains the full method as formalization debt. -/
theorem full_hirota_method_retained_as_formalization_debt :
    fullHirotaMethodClosureStatus =
      ClosureStatus.statementBoundaryFormalizationDebt :=
  rfl

/--
Convention record for the first concrete equation-family target.

The strings are deliberately human-readable Stage1 boundary data rather than
definitions of derivatives.  Later children must replace these labels by a
concrete function space, differential operators, and proofs.
-/
structure EquationFamilyConventions where
  familyName : String
  nonlinearEquation : String
  dependentVariableTransform : String
  bilinearEquation : String
  hirotaDOperatorOrientation : String
  oneSolitonPhase : String
  deriving Repr

/--
Frozen first target for the Hirota bridge work: KdV in the standard plus
dispersion convention.

The intended nonlinear equation is `u_t + 6 u u_x + u_xxx = 0`; the intended
tau transform is `u = 2 partial_x^2 log tau`; and the intended bilinear
identity is `(D_x^4 + D_x D_t) tau · tau = 0`.
-/
def firstTargetEquationFamilyConventions : EquationFamilyConventions where
  familyName := "KdV"
  nonlinearEquation := "u_t + 6 u u_x + u_xxx = 0"
  dependentVariableTransform := "u = 2 partial_x^2 log tau"
  bilinearEquation := "(D_x^4 + D_x D_t) tau · tau = 0"
  hirotaDOperatorOrientation :=
    "D_x^m D_t^n f · g = (partial_x - partial_x')^m (partial_t - partial_t')^n f(x,t) g(x',t') at x'=x, t'=t"
  oneSolitonPhase := "theta = k*x - k^3*t + delta"

/-- The first concrete target family is fixed as KdV. -/
theorem first_target_equation_family_is_kdv :
    firstTargetEquationFamilyConventions.familyName = "KdV" :=
  rfl

/-- The nonlinear KdV sign convention is fixed before the bridge proof. -/
theorem first_target_kdv_nonlinear_sign_convention :
    firstTargetEquationFamilyConventions.nonlinearEquation =
      "u_t + 6 u u_x + u_xxx = 0" :=
  rfl

/-- The tau-transform normalization is fixed before defining concrete operators. -/
theorem first_target_kdv_tau_transform_normalization :
    firstTargetEquationFamilyConventions.dependentVariableTransform =
      "u = 2 partial_x^2 log tau" :=
  rfl

/-- The Hirota bilinear KdV normalization is fixed for later operator work. -/
theorem first_target_kdv_bilinear_normalization :
    firstTargetEquationFamilyConventions.bilinearEquation =
      "(D_x^4 + D_x D_t) tau · tau = 0" :=
  rfl

/-! ## Concrete KdV Hirota operator boundary -/

/-- The selected KdV tau-function domain: space and evolution-time coordinates. -/
abbrev KdVTauPoint : Type :=
  ℂ × ℂ

/-- Chosen tau-function space for the first concrete Hirota operator package. -/
abbrev KdVTauFunction : Type :=
  KdVTauPoint → ℂ

/--
Pointwise multiplication as a bundled bilinear map on the chosen tau space.

This is the multiplication layer used in each summand of the Hirota
`D`-operator.
-/
def kdvPointwiseMulBilinear : BilinearOperator ℂ KdVTauFunction where
  toFun f :=
    { toFun := fun g z => f z * g z
      map_add' := by
        intro g h
        funext z
        simp [mul_add]
      map_smul' := by
        intro c g
        funext z
        simp [mul_left_comm] }
  map_add' := by
    intro f g
    ext h z
    simp [add_mul]
  map_smul' := by
    intro c f
    ext g z
    simp [mul_assoc]

/-- Linear differential data used to instantiate concrete KdV Hirota operators. -/
structure KdVHirotaDifferentialData where
  Dx : KdVTauFunction →ₗ[ℂ] KdVTauFunction
  Dt : KdVTauFunction →ₗ[ℂ] KdVTauFunction

namespace KdVHirotaDifferentialData

/-- Iterate a bundled linear operator on the KdV tau-function space. -/
def iterateLinear (n : ℕ) (L : KdVTauFunction →ₗ[ℂ] KdVTauFunction) :
    KdVTauFunction →ₗ[ℂ] KdVTauFunction :=
  Nat.rec (LinearMap.id : KdVTauFunction →ₗ[ℂ] KdVTauFunction)
    (fun _ prev => L.comp prev) n

/-- Mixed `x`/`t` derivative operator `∂_t^tOrder ∂_x^xOrder`. -/
def mixedDerivative (D : KdVHirotaDifferentialData)
    (xOrder tOrder : ℕ) : KdVTauFunction →ₗ[ℂ] KdVTauFunction :=
  (iterateLinear tOrder D.Dt).comp (iterateLinear xOrder D.Dx)

end KdVHirotaDifferentialData

/--
Concrete Hirota bilinear differential operator
`D_x^xOrder D_t^tOrder f · g` over the selected KdV tau-function space.

The finite binomial sum is the standard Hirota convention
`(∂_x - ∂_x')^m (∂_t - ∂_t')^n f(x,t) g(x',t')` evaluated on the diagonal,
with the actual differential directions supplied as bundled linear maps.
-/
def kdvHirotaDOperator (D : KdVHirotaDifferentialData)
    (xOrder tOrder : ℕ) : BilinearOperator ℂ KdVTauFunction :=
  ∑ i ∈ Finset.range (xOrder + 1),
    ∑ j ∈ Finset.range (tOrder + 1),
      (((-1 : ℂ) ^ (i + j)) * (Nat.choose xOrder i : ℂ) *
          (Nat.choose tOrder j : ℂ)) •
        (kdvPointwiseMulBilinear.precomp
          (D.mixedDerivative (xOrder - i) (tOrder - j))
          (D.mixedDerivative i j))

/-- The selected KdV bilinear combination `(D_x^4 + D_x D_t)`. -/
def kdvBilinearCombinationOperator
    (D : KdVHirotaDifferentialData) : BilinearOperator ℂ KdVTauFunction :=
  kdvHirotaDOperator D 4 0 + kdvHirotaDOperator D 1 1

/-- The concrete KdV Hirota equation on the chosen tau-function space. -/
def KdVTauSolvesConcreteBilinearEquation
    (D : KdVHirotaDifferentialData) (tau : KdVTauFunction) : Prop :=
  TauSolvesBilinearEquation (kdvBilinearCombinationOperator D) tau

/-! ## Basic tau-family identities for the selected KdV bilinear operator -/

/-- The zero tau function in the selected KdV tau-function space. -/
def kdvZeroTauFunction : KdVTauFunction :=
  0

/--
The first checked basic-tau identity for the selected KdV bilinear combination:
the zero tau function satisfies `(D_x^4 + D_x D_t) tau · tau = 0` for any
bundled differential data.
-/
theorem kdv_zero_tau_solves_concrete_bilinear_equation
    (D : KdVHirotaDifferentialData) :
    KdVTauSolvesConcreteBilinearEquation D kdvZeroTauFunction := by
  simpa [KdVTauSolvesConcreteBilinearEquation, kdvZeroTauFunction]
    using TauSolvesBilinearEquation_zero
      (B := kdvBilinearCombinationOperator D)

/-- Constant tau functions in the selected KdV tau-function space. -/
def kdvConstantTauFunction (c : ℂ) : KdVTauFunction :=
  fun _ => c

/--
The summand-level condition needed to close the constant-tau identity for the
selected KdV bilinear combination.

For analytic derivative data this condition should follow from proving that
the concrete `Dx` and `Dt` operators annihilate constants.  It is kept explicit
here because `KdVHirotaDifferentialData` currently contains abstract bundled
linear maps rather than an `fderiv`/`iteratedFDeriv` implementation.
-/
def KdVSelectedSummandsVanishOnConstant
    (D : KdVHirotaDifferentialData) (c : ℂ) : Prop :=
  kdvHirotaDOperator D 4 0 (kdvConstantTauFunction c)
      (kdvConstantTauFunction c) = 0 ∧
    kdvHirotaDOperator D 1 1 (kdvConstantTauFunction c)
      (kdvConstantTauFunction c) = 0

/--
Conditional constant-tau identity for the selected KdV bilinear combination.

This is the checked local reduction from the two Hirota summands to
`(D_x^4 + D_x D_t) tau · tau = 0`; the remaining analytic leaf is proving the
summand condition for derivative data that really differentiates constants to
zero.
-/
theorem kdv_constant_tau_solves_concrete_bilinear_equation_of_summands
    (D : KdVHirotaDifferentialData) (c : ℂ)
    (h : KdVSelectedSummandsVanishOnConstant D c) :
    KdVTauSolvesConcreteBilinearEquation D (kdvConstantTauFunction c) := by
  rcases h with ⟨hDx4, hDxDt⟩
  simp [KdVTauSolvesConcreteBilinearEquation, TauSolvesBilinearEquation,
    kdvBilinearCombinationOperator, hDx4, hDxDt]

/-- Left additivity of the concrete KdV Hirota differential operator. -/
theorem kdvHirotaDOperator_map_add_left
    (D : KdVHirotaDifferentialData) (xOrder tOrder : ℕ)
    (tau₁ tau₂ sigma : KdVTauFunction) :
    kdvHirotaDOperator D xOrder tOrder (tau₁ + tau₂) sigma =
      kdvHirotaDOperator D xOrder tOrder tau₁ sigma +
        kdvHirotaDOperator D xOrder tOrder tau₂ sigma :=
  BilinearOperator.map_add_left _ tau₁ tau₂ sigma

/-- Left scalar compatibility of the concrete KdV Hirota differential operator. -/
theorem kdvHirotaDOperator_map_smul_left
    (D : KdVHirotaDifferentialData) (xOrder tOrder : ℕ)
    (c : ℂ) (tau sigma : KdVTauFunction) :
    kdvHirotaDOperator D xOrder tOrder (c • tau) sigma =
      c • kdvHirotaDOperator D xOrder tOrder tau sigma :=
  BilinearOperator.map_smul_left _ c tau sigma

/-- Right additivity of the concrete KdV Hirota differential operator. -/
theorem kdvHirotaDOperator_map_add_right
    (D : KdVHirotaDifferentialData) (xOrder tOrder : ℕ)
    (tau sigma₁ sigma₂ : KdVTauFunction) :
    kdvHirotaDOperator D xOrder tOrder tau (sigma₁ + sigma₂) =
      kdvHirotaDOperator D xOrder tOrder tau sigma₁ +
        kdvHirotaDOperator D xOrder tOrder tau sigma₂ :=
  BilinearOperator.map_add_right _ tau sigma₁ sigma₂

/-- Right scalar compatibility of the concrete KdV Hirota differential operator. -/
theorem kdvHirotaDOperator_map_smul_right
    (D : KdVHirotaDifferentialData) (xOrder tOrder : ℕ)
    (c : ℂ) (tau sigma : KdVTauFunction) :
    kdvHirotaDOperator D xOrder tOrder tau (c • sigma) =
      c • kdvHirotaDOperator D xOrder tOrder tau sigma :=
  BilinearOperator.map_smul_right _ c tau sigma

/-- Left additivity of the selected KdV bilinear combination. -/
theorem kdvBilinearCombinationOperator_map_add_left
    (D : KdVHirotaDifferentialData)
    (tau₁ tau₂ sigma : KdVTauFunction) :
    kdvBilinearCombinationOperator D (tau₁ + tau₂) sigma =
      kdvBilinearCombinationOperator D tau₁ sigma +
        kdvBilinearCombinationOperator D tau₂ sigma :=
  BilinearOperator.map_add_left _ tau₁ tau₂ sigma

/-- Left scalar compatibility of the selected KdV bilinear combination. -/
theorem kdvBilinearCombinationOperator_map_smul_left
    (D : KdVHirotaDifferentialData)
    (c : ℂ) (tau sigma : KdVTauFunction) :
    kdvBilinearCombinationOperator D (c • tau) sigma =
      c • kdvBilinearCombinationOperator D tau sigma :=
  BilinearOperator.map_smul_left _ c tau sigma

/-- Right additivity of the selected KdV bilinear combination. -/
theorem kdvBilinearCombinationOperator_map_add_right
    (D : KdVHirotaDifferentialData)
    (tau sigma₁ sigma₂ : KdVTauFunction) :
    kdvBilinearCombinationOperator D tau (sigma₁ + sigma₂) =
      kdvBilinearCombinationOperator D tau sigma₁ +
        kdvBilinearCombinationOperator D tau sigma₂ :=
  BilinearOperator.map_add_right _ tau sigma₁ sigma₂

/-- Right scalar compatibility of the selected KdV bilinear combination. -/
theorem kdvBilinearCombinationOperator_map_smul_right
    (D : KdVHirotaDifferentialData)
    (c : ℂ) (tau sigma : KdVTauFunction) :
    kdvBilinearCombinationOperator D tau (c • sigma) =
      c • kdvBilinearCombinationOperator D tau sigma :=
  BilinearOperator.map_smul_right _ c tau sigma

/--
Abstract data for a Hirota bilinear-method theorem.

`Sol` is the nonlinear-field side, while `Tau` is the tau-function side.  The
proposition fields name the mathematical boundaries that a future concrete
formalization must replace by definitions and proofs.
-/
structure HirotaBilinearData
    (R : Type uR) (Tau : Type uTau) (Sol : Type uSol) (Param : Type uParam)
    [CommSemiring R] [AddCommMonoid Tau] [Module R Tau] :
    Type (max (max uR uTau) (max uSol uParam)) where
  bilinearOperator : BilinearOperator R Tau
  tauAdmissible : Tau → Prop
  nonlinearEquation : Sol → Prop
  dependentVariableTransform : Tau → Sol
  parameterAdmissible : Param → Prop
  solitonTau : Param → Tau
  dispersionRelation : Param → Prop
  operatorRepresentsHirotaPolynomial : Prop
  dependentVariableTransformIsHirota : Prop

variable {Sol : Type uSol} {Param : Type uParam}

namespace HirotaBilinearData

/-- The tau-side bilinear equation associated to the data package. -/
def TauSolvesBilinear (D : HirotaBilinearData R Tau Sol Param)
    (tau : Tau) : Prop :=
  TauSolvesBilinearEquation D.bilinearOperator tau

/-- The nonlinear equation after applying the dependent-variable transform. -/
def TransformedTauSolvesNonlinear
    (D : HirotaBilinearData R Tau Sol Param) (tau : Tau) : Prop :=
  D.nonlinearEquation (D.dependentVariableTransform tau)

/--
Certificate required to use the Hirota method in this abstract interface.

The hard mathematical work is in the fields:
* the bilinear-to-nonlinear change-of-variables proof;
* admissibility of the tau family;
* the proof that the tau family satisfies the bilinear equation.
-/
structure Certificate (D : HirotaBilinearData R Tau Sol Param) : Prop where
  bilinear_to_nonlinear :
    ∀ tau : Tau, D.tauAdmissible tau → D.TauSolvesBilinear tau →
      D.TransformedTauSolvesNonlinear tau
  soliton_tau_admissible :
    ∀ p : Param, D.parameterAdmissible p → D.dispersionRelation p →
      D.tauAdmissible (D.solitonTau p)
  soliton_tau_bilinear :
    ∀ p : Param, D.parameterAdmissible p → D.dispersionRelation p →
      D.TauSolvesBilinear (D.solitonTau p)

/-- Conclusion supplied by a closed Hirota certificate. -/
def Conclusion (D : HirotaBilinearData R Tau Sol Param) : Prop :=
  ∀ p : Param, D.parameterAdmissible p → D.dispersionRelation p →
    D.nonlinearEquation (D.dependentVariableTransform (D.solitonTau p))

/-- A certificate turns admissible soliton tau functions into nonlinear solutions. -/
theorem Certificate.conclusion
    {D : HirotaBilinearData R Tau Sol Param} (C : D.Certificate) :
    D.Conclusion := by
  intro p hp hdisp
  exact C.bilinear_to_nonlinear (D.solitonTau p)
    (C.soliton_tau_admissible p hp hdisp)
    (C.soliton_tau_bilinear p hp hdisp)

/-- Projection wrapper for a single parameter value. -/
theorem nonlinear_solution_of_certificate
    {D : HirotaBilinearData R Tau Sol Param} (C : D.Certificate)
    {p : Param} (hp : D.parameterAdmissible p) (hdisp : D.dispersionRelation p) :
    D.nonlinearEquation (D.dependentVariableTransform (D.solitonTau p)) :=
  C.conclusion p hp hdisp

end HirotaBilinearData

/--
Integration-ready package shape for the first concrete equation-family
formalization.

This is intentionally uninstantiated here.  Supplying such a value for KdV, KP,
Toda, or another fixed family is the work that would move the full Hirota method
past the current `formalization_debt` boundary.
-/
structure ConcreteEquationFamilyPackage
    (R : Type uR) (Tau : Type uTau) (Sol : Type uSol) (Param : Type uParam)
    [CommSemiring R] [AddCommMonoid Tau] [Module R Tau] :
    Type (max (max uR uTau) (max uSol uParam)) where
  data : HirotaBilinearData R Tau Sol Param
  equationFamilyName : String
  tauSpaceInstantiated : Prop
  hirotaDOperatorInstantiated : Prop
  dependentVariableTransformInstantiated : Prop
  dispersionRelationInstantiated : Prop
  tau_space_instantiated : tauSpaceInstantiated
  hirota_D_operator_instantiated : hirotaDOperatorInstantiated
  dependent_variable_transform_instantiated :
    dependentVariableTransformInstantiated
  dispersion_relation_instantiated : dispersionRelationInstantiated
  certificate : data.Certificate

/--
Normalized Stage1 statement shape for the Hirota bilinear method.

This is not a proof that a specific PDE has a Hirota form.  It says that once a
concrete tau-function certificate is supplied, the transformed tau family
solves the selected nonlinear equation.
-/
def StatementShape : Prop :=
  ∀ (R : Type uR) (Tau : Type uTau) (Sol : Type uSol) (Param : Type uParam)
    [CommSemiring R] [AddCommMonoid Tau] [Module R Tau],
      ∀ D : HirotaBilinearData R Tau Sol Param,
        D.Certificate → D.Conclusion

/-- Checked closure of the abstract certificate interface. -/
theorem statementShape_of_certificate : StatementShape.{uR, uTau, uSol, uParam} := by
  intro R Tau Sol Param _ _ _ D C
  exact C.conclusion

/-- Pinned mathlib revision recorded for this Stage1 anchor audit. -/
def pinnedMathlibRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.LinearAlgebra.BilinearMap",
  "Mathlib.Analysis.Calculus.ContDiff.Basic",
  "Mathlib.Analysis.Calculus.FDeriv.Basic",
  "Mathlib.Analysis.Calculus.IteratedDeriv.Defs",
  "Mathlib.Analysis.Analytic.Basic",
  "Mathlib.Analysis.Distribution.FourierMultiplier",
  "Mathlib.Analysis.Fourier.Convolution"
]

/-- Pinned declaration names used or audited for this Stage1 slot. -/
def mathlibAnchorNames : List String := [
  "LinearMap.BilinMap",
  "IsBilinearMap",
  "LinearMap.map_add₂",
  "LinearMap.map_smul₂",
  "ContDiff",
  "HasFDerivAt",
  "fderiv",
  "iteratedFDeriv",
  "ContinuousMultilinearMap"
]

/--
Search terms that did not locate a terminal Hirota-method theorem in the local
pinned mathlib tree.
-/
def absentTerminalSearchTerms : List String := [
  "Hirota",
  "Hirota bilinear",
  "bilinear method",
  "tau-function",
  "tau function",
  "soliton",
  "KdV",
  "KP",
  "Toda"
]

/-- External-source audit notes for the repo-local integration-debt gate. -/
def externalAnchorAuditNotes : List String := [
  "Local pinned mathlib/source search on 2026-05-01 found no terminal Hirota-method Lean theorem.",
  "Authenticated GitHub search was not closed by this statement-boundary child: gh auth status reported no logged-in GitHub hosts on 2026-05-01.",
  "No external upstream Hirota proof was added to this repo-local Lake closure."
]

/-- C008 authentication state for the requested primary-source GitHub audit. -/
inductive GitHubCodeSearchAuditStatus where
  | blockedNoLoggedInHost
  deriving DecidableEq, Repr

/--
Current C008 GitHub search status.

Because the local `gh` client is not logged in, GitHub code search cannot be
used as an authenticated primary-source audit in this pass.
-/
def githubCodeSearchAuditStatus : GitHubCodeSearchAuditStatus :=
  GitHubCodeSearchAuditStatus.blockedNoLoggedInHost

/-- C008 repo-local integration-debt conclusion for external Hirota proofs. -/
def externalHirotaProofIntegrationGate : String :=
  "No terminal external Lean 4 Hirota proof was found through an authenticated search in this pass; the authenticated GitHub code-search step is blocked by missing local credentials, so no repo-local completion or external_upstream_pinned status is claimed."

/-- C009 status for serial public blueprint/todo/README/meta synchronization. -/
inductive PublicSynchronizationGateStatus where
  | blockedPendingSerialIntegratorMerge
  deriving DecidableEq, Repr

/--
Current public synchronization gate.

Parallel child workers must not edit shared public status surfaces directly.
This artifact, child ledgers, and the public merge target still need a serial
integrator pass before checklist status can be synchronized.
-/
def publicSynchronizationGateStatus : PublicSynchronizationGateStatus :=
  PublicSynchronizationGateStatus.blockedPendingSerialIntegratorMerge

/-- C009 integration note retained in the checked artifact. -/
def publicSynchronizationGateNote : String :=
  "Public Stage1 blueprint/todo/README/meta synchronization is pending a serial integrator merge; no public status surface is updated by this child and no full Hirota-method completion is claimed."

/-! ## Audit probes retained in the checked file. -/

#check BilinearOperator
#check TauSolvesBilinearEquation
#check BilinearOperator.map_add_left
#check BilinearOperator.map_smul_left
#check BilinearOperator.map_add_right
#check BilinearOperator.map_smul_right
#check BilinearOperator.precomp
#check IsSymmetricBilinearOperator
#check ClosureStatus
#check formalizationDebtRequiredInstantiations
#check fullHirotaMethodClosureStatus
#check full_hirota_method_retained_as_formalization_debt
#check EquationFamilyConventions
#check firstTargetEquationFamilyConventions
#check first_target_equation_family_is_kdv
#check first_target_kdv_nonlinear_sign_convention
#check first_target_kdv_tau_transform_normalization
#check first_target_kdv_bilinear_normalization
#check KdVTauPoint
#check KdVTauFunction
#check kdvPointwiseMulBilinear
#check KdVHirotaDifferentialData
#check KdVHirotaDifferentialData.iterateLinear
#check KdVHirotaDifferentialData.mixedDerivative
#check kdvHirotaDOperator
#check kdvBilinearCombinationOperator
#check KdVTauSolvesConcreteBilinearEquation
#check kdvZeroTauFunction
#check kdv_zero_tau_solves_concrete_bilinear_equation
#check kdvConstantTauFunction
#check KdVSelectedSummandsVanishOnConstant
#check kdv_constant_tau_solves_concrete_bilinear_equation_of_summands
#check kdvHirotaDOperator_map_add_left
#check kdvHirotaDOperator_map_smul_left
#check kdvHirotaDOperator_map_add_right
#check kdvHirotaDOperator_map_smul_right
#check kdvBilinearCombinationOperator_map_add_left
#check kdvBilinearCombinationOperator_map_smul_left
#check kdvBilinearCombinationOperator_map_add_right
#check kdvBilinearCombinationOperator_map_smul_right
#check HirotaBilinearData
#check HirotaBilinearData.Certificate
#check HirotaBilinearData.Conclusion
#check HirotaBilinearData.Certificate.conclusion
#check HirotaBilinearData.nonlinear_solution_of_certificate
#check ConcreteEquationFamilyPackage
#check StatementShape
#check statementShape_of_certificate
#check pinnedMathlibRevision
#check externalAnchorAuditNotes
#check GitHubCodeSearchAuditStatus
#check githubCodeSearchAuditStatus
#check externalHirotaProofIntegrationGate
#check PublicSynchronizationGateStatus
#check publicSynchronizationGateStatus
#check publicSynchronizationGateNote
#check LinearMap.BilinMap
#check IsBilinearMap
#check LinearMap.map_add₂
#check LinearMap.map_smul₂
#check ContDiff
#check HasFDerivAt
#check fderiv
#check iteratedFDeriv

end S1_M_212
end Stage1
end AwesomeTheorems
