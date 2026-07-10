import Mathlib.AlgebraicGeometry.EllipticCurve.Affine.Point
import Mathlib.AlgebraicGeometry.EllipticCurve.Weierstrass
import Mathlib.Analysis.Calculus.Deriv.Basic
import Mathlib.NumberTheory.Height.Basic
import Mathlib.NumberTheory.Height.NumberField
import Mathlib.NumberTheory.LSeries.DirichletContinuation

/-!
# S1-M-044 / THM-M-0125: Gross-Zagier formula

This Stage1 file records a conservative Lean statement boundary for the Gross-Zagier formula.
It deliberately does not claim a proof of the formula.  The local, kernel-checked content is:

* a statement-shape structure making the elliptic curve, central derivative, height pairing, and
  normalization factor explicit;
* wrappers around mathlib anchors for Weierstrass elliptic curves and differentiability of
  Dirichlet L-functions.

The missing bridge is the genuine Hasse-Weil/modular L-function, Heegner point, Neron-Tate height,
and the Gross-Zagier equality between them.
-/

noncomputable section

open Complex
open scoped WeierstrassCurve.Affine

universe u

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_044

/--
Interface target for the missing Hasse-Weil/modular-form L-function API needed by Gross-Zagier.

This is deliberately an API contract, not a construction of the actual L-function.  It records the
minimum analytic payload needed by the Gross-Zagier statement shape: a complex-valued L-function,
a chosen central point, and a proof that the stored central derivative is the actual complex
derivative there.
-/
structure CentralDerivativeLFunctionAPI (K : Type u) [Field K] where
  /-- A Weierstrass model of the elliptic curve whose L-function is represented. -/
  curve : WeierstrassCurve K
  /-- The nonsingularity condition available in mathlib for Weierstrass elliptic curves. -/
  elliptic : curve.IsElliptic
  /-- Placeholder for the eventual Hasse-Weil or modular-form L-function. -/
  LFunction : ℂ → ℂ
  /-- The central point at which Gross-Zagier uses the first derivative. -/
  centralPoint : ℂ
  /-- The stored central derivative value. -/
  centralDerivative : ℂ
  /-- Kernel-checked evidence that `centralDerivative` is the derivative of `LFunction`. -/
  hasDerivAt_centralPoint : HasDerivAt LFunction centralDerivative centralPoint
  /-- Placeholder for conductor, modularity, sign, analytic continuation, and local hypotheses. -/
  arithmeticHypotheses : Prop

namespace CentralDerivativeLFunctionAPI

variable {K : Type u} [Field K]

/-- The same central derivative, computed through mathlib's `deriv` operator. -/
def centralDerivativeViaDeriv (A : CentralDerivativeLFunctionAPI K) : ℂ :=
  deriv A.LFunction A.centralPoint

/-- The API's derivative witness implies differentiability at the central point. -/
theorem differentiableAt_centralPoint (A : CentralDerivativeLFunctionAPI K) :
    DifferentiableAt ℂ A.LFunction A.centralPoint :=
  A.hasDerivAt_centralPoint.differentiableAt

/-- The stored derivative is definitionally compatible with mathlib's `deriv` value. -/
theorem centralDerivativeViaDeriv_eq (A : CentralDerivativeLFunctionAPI K) :
    A.centralDerivativeViaDeriv = A.centralDerivative := by
  simpa [centralDerivativeViaDeriv] using A.hasDerivAt_centralPoint.deriv

/-- Re-express the derivative witness using mathlib's `deriv` notation. -/
theorem hasDerivAt_deriv_centralPoint (A : CentralDerivativeLFunctionAPI K) :
    HasDerivAt A.LFunction (deriv A.LFunction A.centralPoint) A.centralPoint :=
  A.differentiableAt_centralPoint.hasDerivAt

end CentralDerivativeLFunctionAPI

/--
Interface target for the missing Neron-Tate canonical height and height-pairing API.

This is deliberately an API contract for elliptic-curve rational points, not a construction of the
canonical height.  It records the pairing operations and the algebraic laws needed by the
Gross-Zagier statement shape.  A future Jacobian version should expose the same fields over the
chosen Jacobian rational-point group and then map Heegner divisors into that group.
-/
structure NeronTateHeightPairingAPI (K : Type u) [Field K] [DecidableEq K] [NumberField K]
    (E : WeierstrassCurve K) [E.IsElliptic] where
  /-- The Neron-Tate canonical height on rational points of the elliptic curve. -/
  canonicalHeight : E⟮K⟯ → ℝ
  /-- The symmetric bilinear height pairing associated to the canonical height. -/
  heightPairing : E⟮K⟯ → E⟮K⟯ → ℝ
  /-- The canonical height is recovered as the self-pairing. -/
  heightPairing_self : ∀ P : E⟮K⟯, heightPairing P P = canonicalHeight P
  /-- Symmetry of the height pairing. -/
  heightPairing_symm : ∀ P Q : E⟮K⟯, heightPairing P Q = heightPairing Q P
  /-- Additivity in the left argument. -/
  heightPairing_add_left :
    ∀ P Q R : E⟮K⟯, heightPairing (P + Q) R = heightPairing P R + heightPairing Q R
  /-- Additivity in the right argument. -/
  heightPairing_add_right :
    ∀ P Q R : E⟮K⟯, heightPairing P (Q + R) = heightPairing P Q + heightPairing P R
  /-- The canonical height is nonnegative. -/
  canonicalHeight_nonnegative : ∀ P : E⟮K⟯, 0 ≤ canonicalHeight P
  /-- The canonical height is quadratic under multiplication by natural numbers. -/
  canonicalHeight_nsmul :
    ∀ (n : ℕ) (P : E⟮K⟯), canonicalHeight (n • P) = (n : ℝ) ^ 2 * canonicalHeight P
  /-- The associated quadratic form satisfies the parallelogram law. -/
  canonicalHeight_parallelogram :
    ∀ P Q : E⟮K⟯,
      canonicalHeight (P + Q) + canonicalHeight (P - Q) =
        2 * canonicalHeight P + 2 * canonicalHeight Q

namespace NeronTateHeightPairingAPI

variable {K : Type u} [Field K] [DecidableEq K] [NumberField K]
variable {E : WeierstrassCurve K} [E.IsElliptic]

/-- The real Neron-Tate self-pairing promoted to the complex scalar used in Gross-Zagier. -/
def selfPairingAsComplex (H : NeronTateHeightPairingAPI K E) (P : E⟮K⟯) : ℂ :=
  (H.heightPairing P P : ℂ)

/-- The complex self-pairing is the complex coercion of the canonical height. -/
theorem selfPairingAsComplex_eq_canonicalHeight (H : NeronTateHeightPairingAPI K E)
    (P : E⟮K⟯) : H.selfPairingAsComplex P = (H.canonicalHeight P : ℂ) := by
  simp [selfPairingAsComplex, H.heightPairing_self P]

/-- Nonnegativity of the real self-pairing follows from the canonical-height field. -/
theorem heightPairing_self_nonnegative (H : NeronTateHeightPairingAPI K E) (P : E⟮K⟯) :
    0 ≤ H.heightPairing P P := by
  simpa [H.heightPairing_self P] using H.canonicalHeight_nonnegative P

/-- Symmetry wrapper with the arguments named for later Gross-Zagier height-pairing use. -/
theorem heightPairing_comm (H : NeronTateHeightPairingAPI K E) (P Q : E⟮K⟯) :
    H.heightPairing P Q = H.heightPairing Q P :=
  H.heightPairing_symm P Q

end NeronTateHeightPairingAPI

/--
Interface target for the missing Heegner-hypotheses, CM-point, Heegner-divisor, and trace-map API.

This is deliberately an API contract rather than a construction.  It keeps the arithmetic and
geometric pieces separate: an imaginary quadratic/order side, a CM-point space, a divisor target,
and a trace map that produces the elliptic-curve rational point used by the height pairing.
-/
structure HeegnerPackageAPI (K : Type u) [Field K] [DecidableEq K] [NumberField K]
    (E : WeierstrassCurve K) [E.IsElliptic] where
  /-- Placeholder for the future imaginary quadratic field. -/
  quadraticField : Type u
  /-- Placeholder for the future order in the imaginary quadratic field. -/
  order : Type u
  /-- Placeholder for the splitting/conductor Heegner hypotheses. -/
  heegnerHypotheses : Prop
  /-- Placeholder for CM points on the chosen modular or Shimura curve. -/
  cmPointSpace : Type u
  /-- Placeholder for the condition that the selected CM point has the chosen order. -/
  cmPointSatisfiesOrder : Prop
  /-- Placeholder for the divisor-class target before mapping to the elliptic curve or Jacobian. -/
  heegnerDivisorGroup : Type u
  /-- The selected CM point. -/
  selectedCMPoint : cmPointSpace
  /-- The map from CM points to Heegner divisors or divisor classes. -/
  divisorOfCMPoint : cmPointSpace → heegnerDivisorGroup
  /-- The selected Heegner divisor or divisor class. -/
  selectedDivisor : heegnerDivisorGroup
  /-- Evidence that the selected divisor is the divisor attached to the selected CM point. -/
  selectedDivisor_eq : selectedDivisor = divisorOfCMPoint selectedCMPoint
  /-- Placeholder for the source field of definition before applying trace. -/
  traceSourceField : Type u
  /-- Placeholder for the target field after applying trace. -/
  traceTargetField : Type u
  /-- Placeholder for ring-class-field, field-of-definition, and trace-compatibility hypotheses. -/
  fieldOfDefinitionHypotheses : Prop
  /-- The trace or norm map producing a rational point on the elliptic curve. -/
  traceMap : heegnerDivisorGroup → E⟮K⟯
  /-- The Heegner point used by the Gross-Zagier height side. -/
  heegnerPoint : E⟮K⟯
  /-- Evidence that the Heegner point is obtained by tracing the selected divisor. -/
  heegnerPoint_eq_trace : heegnerPoint = traceMap selectedDivisor

namespace HeegnerPackageAPI

variable {K : Type u} [Field K] [DecidableEq K] [NumberField K]
variable {E : WeierstrassCurve K} [E.IsElliptic]

/-- The traced point computed from the selected Heegner divisor. -/
def tracedPoint (P : HeegnerPackageAPI K E) : E⟮K⟯ :=
  P.traceMap P.selectedDivisor

/-- The traced point agrees with the stored Heegner point. -/
theorem tracedPoint_eq_heegnerPoint (P : HeegnerPackageAPI K E) :
    P.tracedPoint = P.heegnerPoint := by
  simpa [tracedPoint] using P.heegnerPoint_eq_trace.symm

/-- The selected divisor is the divisor attached to the selected CM point. -/
theorem selectedDivisor_from_cmPoint (P : HeegnerPackageAPI K E) :
    P.selectedDivisor = P.divisorOfCMPoint P.selectedCMPoint :=
  P.selectedDivisor_eq

/-- The stored Heegner point is the trace of the divisor attached to the selected CM point. -/
theorem heegnerPoint_eq_trace_cmPoint (P : HeegnerPackageAPI K E) :
    P.heegnerPoint = P.traceMap (P.divisorOfCMPoint P.selectedCMPoint) := by
  rw [P.heegnerPoint_eq_trace, P.selectedDivisor_eq]

/-- The three arithmetic hypotheses that the Heegner package contributes to Gross-Zagier. -/
def arithmeticHypotheses (P : HeegnerPackageAPI K E) : Prop :=
  P.heegnerHypotheses ∧ P.cmPointSatisfiesOrder ∧ P.fieldOfDefinitionHypotheses

/-- Unfold the bundled arithmetic hypotheses for later statement-normalization work. -/
theorem arithmeticHypotheses_iff (P : HeegnerPackageAPI K E) :
    P.arithmeticHypotheses ↔
      P.heegnerHypotheses ∧ P.cmPointSatisfiesOrder ∧ P.fieldOfDefinitionHypotheses :=
  Iff.rfl

end HeegnerPackageAPI

/--
Interface target for the missing normalization convention in a future Gross-Zagier theorem.

Gross-Zagier formulas vary by L-function normalization, period normalization, local Tamagawa or
Euler-factor conventions, height-pairing conventions, and trace/index conventions.  This structure
does not choose one of those conventions.  It records the exact place where a future proof-bearing
statement must choose one, and it splits the period and local-factor requirements into named
side-condition fields.
-/
structure GrossZagierNormalizationAPI where
  /-- Placeholder type for the source/document convention being followed. -/
  conventionSource : Type u
  /-- The selected convention within the source type. -/
  selectedConvention : conventionSource
  /-- The selected convention has been identified exactly, not just up to prose. -/
  conventionIdentified : Prop
  /-- The central point and derivative normalization agree with the selected convention. -/
  centralDerivativeConvention : Prop
  /-- The height pairing uses the same normalization as the selected Gross-Zagier formula. -/
  heightPairingConvention : Prop
  /-- Period-side hypotheses, split out for a future named lemma. -/
  periodSideConditions : Prop
  /-- Local Euler/Tamagawa/index-factor hypotheses, split out for a future named lemma. -/
  localFactorSideConditions : Prop
  /-- Trace, field-of-definition, and index normalizations not already included above. -/
  traceAndIndexConvention : Prop
  /-- The period contribution to the explicit normalization factor. -/
  periodFactor : ℂ
  /-- The local-factor contribution to the explicit normalization factor. -/
  localFactor : ℂ
  /-- The remaining global scalar after period and local factors have been split. -/
  globalScalarFactor : ℂ
  /-- The full explicit normalization factor in the selected convention. -/
  normalizationFactor : ℂ
  /-- The chosen convention factors the normalization into global, period, and local parts. -/
  normalizationFactor_eq :
    normalizationFactor = globalScalarFactor * periodFactor * localFactor
  /-- Bundled side conditions for feeding the convention into a statement-shape theorem. -/
  normalizationHypotheses : Prop
  /-- The bundled side conditions are exactly the named split conditions above. -/
  normalizationHypotheses_iff :
    normalizationHypotheses ↔
      conventionIdentified ∧
        centralDerivativeConvention ∧
          heightPairingConvention ∧
            periodSideConditions ∧
              localFactorSideConditions ∧ traceAndIndexConvention

namespace GrossZagierNormalizationAPI

/-- The selected Gross-Zagier normalization convention is explicitly identified. -/
theorem conventionIdentified_of_normalizationHypotheses (N : GrossZagierNormalizationAPI)
    (h : N.normalizationHypotheses) : N.conventionIdentified :=
  (N.normalizationHypotheses_iff.mp h).1

/-- The central derivative uses the selected normalization convention. -/
theorem centralDerivativeConvention_of_normalizationHypotheses
    (N : GrossZagierNormalizationAPI) (h : N.normalizationHypotheses) :
    N.centralDerivativeConvention :=
  (N.normalizationHypotheses_iff.mp h).2.1

/-- The height pairing uses the selected normalization convention. -/
theorem heightPairingConvention_of_normalizationHypotheses
    (N : GrossZagierNormalizationAPI) (h : N.normalizationHypotheses) :
    N.heightPairingConvention :=
  (N.normalizationHypotheses_iff.mp h).2.2.1

/-- Named period-side lemma for the selected Gross-Zagier normalization convention. -/
theorem periodSideConditions_of_normalizationHypotheses (N : GrossZagierNormalizationAPI)
    (h : N.normalizationHypotheses) : N.periodSideConditions :=
  (N.normalizationHypotheses_iff.mp h).2.2.2.1

/-- Named local-factor-side lemma for the selected Gross-Zagier normalization convention. -/
theorem localFactorSideConditions_of_normalizationHypotheses
    (N : GrossZagierNormalizationAPI) (h : N.normalizationHypotheses) :
    N.localFactorSideConditions :=
  (N.normalizationHypotheses_iff.mp h).2.2.2.2.1

/-- Trace and index normalizations follow from the bundled normalization hypotheses. -/
theorem traceAndIndexConvention_of_normalizationHypotheses
    (N : GrossZagierNormalizationAPI) (h : N.normalizationHypotheses) :
    N.traceAndIndexConvention :=
  (N.normalizationHypotheses_iff.mp h).2.2.2.2.2

/-- Re-express the full normalization factor through its named global, period, and local pieces. -/
theorem normalizationFactor_eq_global_period_local (N : GrossZagierNormalizationAPI) :
    N.normalizationFactor = N.globalScalarFactor * N.periodFactor * N.localFactor :=
  N.normalizationFactor_eq

end GrossZagierNormalizationAPI

/--
Input data for a future formal Gross-Zagier statement over a field with a height package.

The `derivativeAtCentralPoint`, `heightPairingOfHeegnerPoint`, and `normalizationFactor` fields are
intentional placeholders for currently missing mathlib objects: the elliptic-curve Hasse-Weil
L-function and its central derivative, the Heegner point, and the Neron-Tate height pairing.
-/
structure GrossZagierStatementData (K : Type u) [Field K] [Height.AdmissibleAbsValues K] where
  /-- A Weierstrass model of the elliptic curve. -/
  curve : WeierstrassCurve K
  /-- The nonsingularity condition available in mathlib for Weierstrass elliptic curves. -/
  elliptic : curve.IsElliptic
  /-- Placeholder for the derivative of the relevant elliptic-curve L-function at the center. -/
  derivativeAtCentralPoint : ℂ
  /-- Placeholder for the canonical-height pairing of the Gross-Zagier Heegner divisor/point. -/
  heightPairingOfHeegnerPoint : ℂ
  /-- Placeholder for the explicit nonzero normalization factor in the formula. -/
  normalizationFactor : ℂ
  /-- Placeholder collecting modularity, Heegner, sign, conductor, and local hypotheses. -/
  hypotheses : Prop

namespace GrossZagierStatementData

variable {K : Type u} [Field K] [Height.AdmissibleAbsValues K]

/-- The normalized Gross-Zagier formula shape once the missing objects are formalized. -/
def expectedFormula (D : GrossZagierStatementData K) : Prop :=
  D.hypotheses →
    D.derivativeAtCentralPoint =
      D.normalizationFactor * D.heightPairingOfHeegnerPoint

/-- The mathlib elliptic-curve anchor exposed by the statement data. -/
theorem elliptic_discriminant_isUnit (D : GrossZagierStatementData K) :
    IsUnit D.curve.Δ := by
  letI : D.curve.IsElliptic := D.elliptic
  exact D.curve.isUnit_Δ

/--
Constructor showing how an explicitly identified normalization convention supplies the
normalization factor and its named side conditions to the Gross-Zagier statement boundary.
-/
def withNormalizationAPI (D : GrossZagierStatementData K) (N : GrossZagierNormalizationAPI) :
    GrossZagierStatementData K where
  curve := D.curve
  elliptic := D.elliptic
  derivativeAtCentralPoint := D.derivativeAtCentralPoint
  heightPairingOfHeegnerPoint := D.heightPairingOfHeegnerPoint
  normalizationFactor := N.normalizationFactor
  hypotheses := D.hypotheses ∧ N.normalizationHypotheses

/-- The normalization constructor preserves the central derivative side of the statement. -/
theorem withNormalizationAPI_derivativeAtCentralPoint (D : GrossZagierStatementData K)
    (N : GrossZagierNormalizationAPI) :
    (D.withNormalizationAPI N).derivativeAtCentralPoint = D.derivativeAtCentralPoint :=
  rfl

/-- The normalization constructor stores the selected explicit normalization factor. -/
theorem withNormalizationAPI_normalizationFactor (D : GrossZagierStatementData K)
    (N : GrossZagierNormalizationAPI) :
    (D.withNormalizationAPI N).normalizationFactor = N.normalizationFactor :=
  rfl

/-- The normalization constructor exposes the formula with the selected convention factor. -/
theorem withNormalizationAPI_expectedFormula_iff (D : GrossZagierStatementData K)
    (N : GrossZagierNormalizationAPI) :
    (D.withNormalizationAPI N).expectedFormula ↔
      D.hypotheses ∧ N.normalizationHypotheses →
        D.derivativeAtCentralPoint =
          N.normalizationFactor * D.heightPairingOfHeegnerPoint :=
  Iff.rfl

/--
The normalization constructor exposes the formula after splitting the normalization factor into
global, period, and local-factor pieces.
-/
theorem withNormalizationAPI_expectedFormula_splitFactor (D : GrossZagierStatementData K)
    (N : GrossZagierNormalizationAPI) :
    (D.withNormalizationAPI N).expectedFormula ↔
      D.hypotheses ∧ N.normalizationHypotheses →
        D.derivativeAtCentralPoint =
          (N.globalScalarFactor * N.periodFactor * N.localFactor) *
            D.heightPairingOfHeegnerPoint := by
  rw [withNormalizationAPI_expectedFormula_iff, N.normalizationFactor_eq]

/--
Constructor showing how a future central-derivative L-function API plugs into the current
Gross-Zagier statement boundary once the height pairing and normalization side are supplied.
-/
def fromCentralDerivativeAPI (A : CentralDerivativeLFunctionAPI K)
    (heightPairingOfHeegnerPoint normalizationFactor : ℂ) (hypotheses : Prop) :
    GrossZagierStatementData K where
  curve := A.curve
  elliptic := A.elliptic
  derivativeAtCentralPoint := A.centralDerivative
  heightPairingOfHeegnerPoint := heightPairingOfHeegnerPoint
  normalizationFactor := normalizationFactor
  hypotheses := hypotheses

/-- The L-function API constructor preserves the checked central derivative field. -/
theorem fromCentralDerivativeAPI_derivativeAtCentralPoint (A : CentralDerivativeLFunctionAPI K)
    (heightPairingOfHeegnerPoint normalizationFactor : ℂ) (hypotheses : Prop) :
    (fromCentralDerivativeAPI A heightPairingOfHeegnerPoint normalizationFactor hypotheses).derivativeAtCentralPoint =
      A.centralDerivative :=
  rfl

/-- Unfolding the constructor exposes the exact formula shape expected from Gross-Zagier. -/
theorem fromCentralDerivativeAPI_expectedFormula_iff (A : CentralDerivativeLFunctionAPI K)
    (heightPairingOfHeegnerPoint normalizationFactor : ℂ) (hypotheses : Prop) :
    (fromCentralDerivativeAPI A heightPairingOfHeegnerPoint normalizationFactor hypotheses).expectedFormula ↔
        hypotheses → A.centralDerivative =
          normalizationFactor * heightPairingOfHeegnerPoint :=
  Iff.rfl

/--
Constructor showing how a future Neron-Tate height-pairing API supplies the height side of the
Gross-Zagier statement boundary once a Heegner point, central derivative, and normalization factor
are supplied.
-/
def fromHeightPairingAPI {K : Type u} [Field K] [DecidableEq K] [NumberField K]
    [Height.AdmissibleAbsValues K] {E : WeierstrassCurve K} [E.IsElliptic]
    (H : NeronTateHeightPairingAPI K E) (heegnerPoint : E⟮K⟯)
    (derivativeAtCentralPoint normalizationFactor : ℂ) (hypotheses : Prop) :
    GrossZagierStatementData K where
  curve := E
  elliptic := inferInstance
  derivativeAtCentralPoint := derivativeAtCentralPoint
  heightPairingOfHeegnerPoint := H.selfPairingAsComplex heegnerPoint
  normalizationFactor := normalizationFactor
  hypotheses := hypotheses

/-- The height-pairing API constructor preserves the supplied central derivative field. -/
theorem fromHeightPairingAPI_derivativeAtCentralPoint {K : Type u} [Field K] [DecidableEq K]
    [NumberField K] [Height.AdmissibleAbsValues K] {E : WeierstrassCurve K} [E.IsElliptic]
    (H : NeronTateHeightPairingAPI K E) (heegnerPoint : E⟮K⟯)
    (derivativeAtCentralPoint normalizationFactor : ℂ) (hypotheses : Prop) :
    (fromHeightPairingAPI H heegnerPoint derivativeAtCentralPoint normalizationFactor hypotheses).derivativeAtCentralPoint =
      derivativeAtCentralPoint :=
  rfl

/-- The height-pairing API constructor stores the Heegner self-pairing as a complex number. -/
theorem fromHeightPairingAPI_heightPairingOfHeegnerPoint {K : Type u} [Field K]
    [DecidableEq K] [NumberField K] [Height.AdmissibleAbsValues K] {E : WeierstrassCurve K}
    [E.IsElliptic] (H : NeronTateHeightPairingAPI K E) (heegnerPoint : E⟮K⟯)
    (derivativeAtCentralPoint normalizationFactor : ℂ) (hypotheses : Prop) :
    (fromHeightPairingAPI H heegnerPoint derivativeAtCentralPoint normalizationFactor hypotheses).heightPairingOfHeegnerPoint =
      H.selfPairingAsComplex heegnerPoint :=
  rfl

/-- Unfolding the height-side constructor exposes the exact Gross-Zagier formula shape. -/
theorem fromHeightPairingAPI_expectedFormula_iff {K : Type u} [Field K] [DecidableEq K]
    [NumberField K] [Height.AdmissibleAbsValues K] {E : WeierstrassCurve K} [E.IsElliptic]
    (H : NeronTateHeightPairingAPI K E) (heegnerPoint : E⟮K⟯)
    (derivativeAtCentralPoint normalizationFactor : ℂ) (hypotheses : Prop) :
    (fromHeightPairingAPI H heegnerPoint derivativeAtCentralPoint normalizationFactor hypotheses).expectedFormula ↔
        hypotheses → derivativeAtCentralPoint =
          normalizationFactor * H.selfPairingAsComplex heegnerPoint :=
  Iff.rfl

/--
Constructor showing how a future Heegner package and height-pairing package jointly supply the
height side of the Gross-Zagier statement boundary.
-/
def fromHeegnerPackageAPI {K : Type u} [Field K] [DecidableEq K] [NumberField K]
    [Height.AdmissibleAbsValues K] {E : WeierstrassCurve K} [E.IsElliptic]
    (H : NeronTateHeightPairingAPI K E) (P : HeegnerPackageAPI K E)
    (derivativeAtCentralPoint normalizationFactor : ℂ) (hypotheses : Prop) :
    GrossZagierStatementData K :=
  fromHeightPairingAPI H P.heegnerPoint derivativeAtCentralPoint normalizationFactor
    (P.arithmeticHypotheses ∧ hypotheses)

/-- The Heegner-package constructor preserves the supplied central derivative field. -/
theorem fromHeegnerPackageAPI_derivativeAtCentralPoint {K : Type u} [Field K] [DecidableEq K]
    [NumberField K] [Height.AdmissibleAbsValues K] {E : WeierstrassCurve K} [E.IsElliptic]
    (H : NeronTateHeightPairingAPI K E) (P : HeegnerPackageAPI K E)
    (derivativeAtCentralPoint normalizationFactor : ℂ) (hypotheses : Prop) :
    (fromHeegnerPackageAPI H P derivativeAtCentralPoint normalizationFactor hypotheses).derivativeAtCentralPoint =
      derivativeAtCentralPoint :=
  rfl

/-- The Heegner-package constructor stores the height pairing of the traced Heegner point. -/
theorem fromHeegnerPackageAPI_heightPairingOfHeegnerPoint {K : Type u} [Field K]
    [DecidableEq K] [NumberField K] [Height.AdmissibleAbsValues K] {E : WeierstrassCurve K}
    [E.IsElliptic] (H : NeronTateHeightPairingAPI K E) (P : HeegnerPackageAPI K E)
    (derivativeAtCentralPoint normalizationFactor : ℂ) (hypotheses : Prop) :
    (fromHeegnerPackageAPI H P derivativeAtCentralPoint normalizationFactor hypotheses).heightPairingOfHeegnerPoint =
      H.selfPairingAsComplex P.heegnerPoint :=
  rfl

/-- Unfolding the Heegner-package constructor exposes the trace-fed Gross-Zagier formula shape. -/
theorem fromHeegnerPackageAPI_expectedFormula_iff {K : Type u} [Field K] [DecidableEq K]
    [NumberField K] [Height.AdmissibleAbsValues K] {E : WeierstrassCurve K} [E.IsElliptic]
    (H : NeronTateHeightPairingAPI K E) (P : HeegnerPackageAPI K E)
    (derivativeAtCentralPoint normalizationFactor : ℂ) (hypotheses : Prop) :
    (fromHeegnerPackageAPI H P derivativeAtCentralPoint normalizationFactor hypotheses).expectedFormula ↔
        P.arithmeticHypotheses ∧ hypotheses → derivativeAtCentralPoint =
          normalizationFactor * H.selfPairingAsComplex P.heegnerPoint :=
  Iff.rfl

end GrossZagierStatementData

/-- Stage1 statement-shape target: no local proof of this proposition is claimed. -/
def StatementShape : Prop :=
  ∀ {K : Type u} [Field K] [Height.AdmissibleAbsValues K],
    ∀ D : GrossZagierStatementData K, D.expectedFormula

/-- A directly checked mathlib wrapper for the Weierstrass discriminant identity. -/
theorem weierstrass_c_relation_anchor {R : Type u} [CommRing R] (W : WeierstrassCurve R) :
    1728 * W.Δ = W.c₄ ^ 3 - W.c₆ ^ 2 :=
  W.c_relation

/--
A directly checked analytic anchor from mathlib: nontrivial Dirichlet L-functions are
complex-differentiable.  This is not the elliptic-curve L-function needed for Gross-Zagier, but it
records the available local L-function API family.
-/
theorem dirichlet_LFunction_differentiable_anchor {N : ℕ} [NeZero N]
    {χ : DirichletCharacter ℂ N} (hχ : χ ≠ 1) :
    Differentiable ℂ (DirichletCharacter.LFunction χ) :=
  DirichletCharacter.differentiable_LFunction hχ

/-- Audit row for the external Lean code-search child. -/
structure ExternalLeanCodeSearchAuditRow where
  /-- Search phrase requested by the child task. -/
  searchTerm : String
  /-- Authenticated GitHub CLI query that should be run when credentials are available. -/
  authenticatedQuery : String
  /-- What the pinned local dependency/source grep established in this pass. -/
  localPinnedDependencyFinding : String
  /-- Repo-local pin/import/check action available in this pass. -/
  repoLocalAction : String
  /-- M0387 machine-status classification for this row. -/
  completionStatus : String

/-- Requested external Lean search terms for the Gross-Zagier child audit. -/
def externalLeanGrossZagierSearchTerms : List String :=
  [ "Gross-Zagier",
    "GrossZagier",
    "Heegner",
    "NeronTate",
    "HasseWeil" ]

/--
Authenticated external GitHub code search was blocked in this local worker.

The local `gh auth status` command reported that no GitHub host is logged in, and `GH_TOKEN` was
absent.  Therefore this artifact records a concrete blocker rather than an anchor-only completion
claim.
-/
def externalLeanGrossZagierAuthenticatedSearchBlocker : String :=
  "2026-05-01: authenticated GitHub code search blocked locally; `gh auth status` reports no logged-in GitHub hosts and `GH_TOKEN` is absent."

/--
External Lean audit rows for the requested `Gross-Zagier`, `Heegner`, `NeronTate`, and
`HasseWeil` search family.

Because authenticated GitHub code search was unavailable, these rows only record pinned local
dependency/source grep findings and the exact authenticated queries that must be rerun by an
integrator with credentials.  None of these rows is completion evidence for the Gross-Zagier
formula.
-/
def externalLeanGrossZagierCodeSearchAuditRows : List ExternalLeanCodeSearchAuditRow :=
  [ { searchTerm := "Gross-Zagier",
      authenticatedQuery := "gh search code 'Gross-Zagier' --language Lean --limit 50",
      localPinnedDependencyFinding :=
        "Pinned mathlib revision 8a178386ffc0f5fef0b77738bb5449d50efeea95 and local Stage1 grep found no proof-bearing Lean theorem for the Gross-Zagier formula; only this statement-shape artifact mentions the formula.",
      repoLocalAction :=
        "No external proof candidate was available to pin/import/check in this pass.",
      completionStatus := "not_repo_local_closed; formalization_debt; authenticated_search_blocked" },
    { searchTerm := "GrossZagier",
      authenticatedQuery := "gh search code GrossZagier --language Lean --limit 50",
      localPinnedDependencyFinding :=
        "Pinned local sources expose `GrossZagierStatementData` and `GrossZagierNormalizationAPI` only as repo-local statement-shape/API contracts, not as a proof of the formula.",
      repoLocalAction :=
        "No proof-bearing upstream module or theorem name was found locally, so no dependency was added.",
      completionStatus := "not_repo_local_closed; formalization_debt; authenticated_search_blocked" },
    { searchTerm := "Heegner",
      authenticatedQuery := "gh search code Heegner --language Lean --limit 50",
      localPinnedDependencyFinding :=
        "Pinned mathlib grep only found a comment-level Heegner-number mention in `Mathlib.Analysis.Real.Pi.Chudnovsky`; local Stage1 files contain Heegner placeholders but no Heegner point/divisor proof API.",
      repoLocalAction :=
        "No Heegner-point Gross-Zagier proof dependency was available to integrate.",
      completionStatus := "not_repo_local_closed; formalization_debt; authenticated_search_blocked" },
    { searchTerm := "NeronTate",
      authenticatedQuery := "gh search code NeronTate --language Lean --limit 50",
      localPinnedDependencyFinding :=
        "Pinned mathlib grep found no Neron-Tate canonical-height API; local Stage1 files contain API boundaries such as `NeronTateHeightPairingAPI` and `NeronTateHeightPackage` only.",
      repoLocalAction :=
        "No Neron-Tate Gross-Zagier proof dependency was available to integrate.",
      completionStatus := "not_repo_local_closed; formalization_debt; authenticated_search_blocked" },
    { searchTerm := "HasseWeil",
      authenticatedQuery := "gh search code HasseWeil --language Lean --limit 50",
      localPinnedDependencyFinding :=
        "Pinned local grep found Hasse-Weil references only in Stage1 statement-shape prose/API targets, not a checked elliptic-curve Hasse-Weil L-function theorem for Gross-Zagier.",
      repoLocalAction :=
        "No Hasse-Weil L-function proof dependency was available to integrate.",
      completionStatus := "not_repo_local_closed; formalization_debt; authenticated_search_blocked" } ]

/--
Repo-local closure marker for the external Lean code-search child.

This must remain `false` until an authenticated search identifies a proof-bearing external Lean
artifact and this repository pins/imports/checks it, or a local proof body/wrapper is supplied.
-/
def externalLeanGrossZagierSearchRepoLocalClosed : Bool :=
  false

/-- The external Lean code-search child is not a repo-local theorem completion. -/
theorem externalLeanGrossZagierSearchRepoLocalClosed_eq_false :
    externalLeanGrossZagierSearchRepoLocalClosed = false :=
  rfl

/-- Remaining child leaves for the external Lean code-search audit. -/
def externalLeanGrossZagierSearchRemainingLeaves : List String :=
  [ "Run authenticated GitHub code search for `Gross-Zagier`, `GrossZagier`, `Heegner`, `NeronTate`, and `HasseWeil` with a logged-in `gh` host or a valid `GH_TOKEN`.",
    "For every candidate, record repository URL, commit, file path, theorem or declaration name, Lean version, Lake/mathlib pins, proof status, and license.",
    "If a proof-bearing external Lean artifact exists, either pin/import/check it in this repository or record a concrete integration blocker such as toolchain incompatibility, dependency conflict, or license restriction.",
    "Keep Gross-Zagier theorem completion open until `externalLeanGrossZagierSearchRepoLocalClosed` is replaced by a locally validated proof-bearing closure." ]

/-- Machine-readable gate for the public completion checkbox child. -/
structure PublicCompletionSynchronizationGate where
  /-- A local proof body, pinned mathlib wrapper, or pinned external proof validates Gross-Zagier. -/
  proofBearingRepoLocalClosure : Bool
  /-- The public blueprint completion checkbox may be checked. -/
  publicCompletionCheckboxMayClose : Bool
  /-- Blueprint, todo, README, and other public status surfaces have been synchronized. -/
  publicStatusSurfacesSynchronized : Bool
  /-- No anchor-only external proof is being treated as a completed repo-local integration state. -/
  noCompletedRepoLocalIntegrationDebt : Bool
  /-- Current machine-status classification for the parent theorem. -/
  machineStatus : String
  /-- Current debt classification for the parent theorem. -/
  debtClass : String
  /-- Human-readable reason the public completion checkbox must remain open. -/
  gateReason : String

/--
Current public completion gate for S1-M-044 / THM-M-0125.

This deliberately keeps the public completion checkbox open.  The local file validates
statement-shape boundaries and auxiliary wrappers only; it does not contain a proof-bearing
Gross-Zagier theorem or a pinned external wrapper.
-/
def publicCompletionSynchronizationGate : PublicCompletionSynchronizationGate where
  proofBearingRepoLocalClosure := false
  publicCompletionCheckboxMayClose := false
  publicStatusSurfacesSynchronized := false
  noCompletedRepoLocalIntegrationDebt := true
  machineStatus := "not_repo_local_closed"
  debtClass := "formalization_debt"
  gateReason :=
    "Keep the public completion checkbox open until a proof-bearing Gross-Zagier theorem or pinned wrapper passes local Lean validation and public status surfaces are synchronized."

/-- S1-M-044 has no proof-bearing repo-local Gross-Zagier closure in this artifact. -/
theorem publicCompletionGate_proofBearingRepoLocalClosure_eq_false :
    publicCompletionSynchronizationGate.proofBearingRepoLocalClosure = false :=
  rfl

/-- The public completion checkbox must remain open in this child state. -/
theorem publicCompletionGate_checkboxMayClose_eq_false :
    publicCompletionSynchronizationGate.publicCompletionCheckboxMayClose = false :=
  rfl

/-- Public status surfaces are not closed by this child-owned private ledger patch. -/
theorem publicCompletionGate_publicStatusSurfacesSynchronized_eq_false :
    publicCompletionSynchronizationGate.publicStatusSurfacesSynchronized = false :=
  rfl

/-- This child does not leave completed-state repo-local integration debt. -/
theorem publicCompletionGate_noCompletedRepoLocalIntegrationDebt_eq_true :
    publicCompletionSynchronizationGate.noCompletedRepoLocalIntegrationDebt = true :=
  rfl

/-- Remaining child leaves for the public completion synchronization gate. -/
def publicCompletionSynchronizationRemainingLeaves : List String :=
  [ "Keep the public S1-M-044 completion checkbox open while `publicCompletionSynchronizationGate.publicCompletionCheckboxMayClose = false`.",
    "Do not synchronize public status surfaces to completed until a proof-bearing local theorem, pinned mathlib wrapper, or pinned external proof wrapper validates locally.",
    "If a future external Lean proof is found, pin/import/check it in this Lake closure or record a concrete integration blocker before any completion claim.",
    "After proof-bearing validation exists, synchronize blueprint, todo, README, and other public status surfaces in a serial integrator-owned patch." ]

end S1_M_044
end Stage1
end AwesomeTheorems
