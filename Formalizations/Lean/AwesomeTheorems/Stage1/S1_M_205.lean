import Mathlib.AlgebraicGeometry.EllipticCurve.Jacobian.Basic
import Mathlib.AlgebraicGeometry.Group.Abelian
import Mathlib.AlgebraicGeometry.Morphisms.Proper
import Mathlib.AlgebraicGeometry.Morphisms.Smooth
import Mathlib.AlgebraicGeometry.Scheme
import Mathlib.Algebra.Algebra.Spectrum.Basic
import Mathlib.Analysis.Complex.Basic
import Mathlib.Analysis.Normed.Operator.Basic
import Mathlib.Data.Complex.Basic
import Mathlib.Geometry.Manifold.VectorBundle.Basic
import Mathlib.Geometry.Manifold.VectorField.LieBracket
import Mathlib.LinearAlgebra.Dimension.Finrank
import Mathlib.LinearAlgebra.SymplecticGroup

/-!
# S1-M-205 / THM-M-1546: Hitchin system

This Stage1 artifact records a conservative Lean 4 statement boundary for the
Hitchin system as an algebraically completely integrable system.

The phrase "the Hitchin system is algebraically integrable" is not yet a
repo-local mathlib theorem.  The declarations below isolate the mathematical
interfaces a later proof must instantiate: a Higgs-moduli phase space, a
Hitchin base, the Hitchin map, spectral-curve data, Hamiltonians, a Poisson
bracket, generic abelian-variety fibers, Lagrangian fibers, and the half
dimension condition.  Only low-risk wrappers and a zero-bracket toy case are
proved here.
-/

noncomputable section

universe uM uB uS uι uV

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_205

/-- Hamiltonian functions on the chosen moduli/phase space. -/
abbrev HamiltonianFunction (M : Type uM) :=
  M → ℂ

/--
Stage1 Poisson bracket boundary on Hamiltonian functions.

At this boundary it is just a binary operation on functions.  A later
formalization must replace this with the bracket induced by the holomorphic
symplectic form on the Higgs-bundle moduli space.
-/
abbrev PoissonBracket (M : Type uM) :=
  HamiltonianFunction M → HamiltonianFunction M → HamiltonianFunction M

/-- A family of Hamiltonians is pairwise Poisson-commuting. -/
def PairwisePoissonCommuting {M : Type uM} {ι : Type uι}
    (bracket : PoissonBracket M) (H : ι → HamiltonianFunction M) : Prop :=
  ∀ i j : ι, ∀ x : M, bracket (H i) (H j) x = 0

/-- The zero Poisson bracket, used as a checked special-parameter anchor. -/
def zeroPoissonBracket (M : Type uM) : PoissonBracket M :=
  fun _ _ _ => 0

/-- Every Hamiltonian family pairwise commutes for the zero Poisson bracket. -/
theorem pairwisePoissonCommuting_zero {M : Type uM} {ι : Type uι}
    (H : ι → HamiltonianFunction M) :
    PairwisePoissonCommuting (zeroPoissonBracket M) H := by
  intro i j x
  rfl

/--
A linearized operator around a point of the Hitchin system.

This is not the spectral curve.  It is only a local mathlib anchor for the
operator/spectrum interface mentioned in the Stage1 partial-verification scope.
-/
abbrev HitchinLinearizedOperator
    (V : Type uV) [NormedAddCommGroup V] [NormedSpace ℂ V] : Type uV :=
  V →L[ℂ] V

/-- Spectrum of a linearized operator, using mathlib's algebra spectrum. -/
def LinearizedSpectrum
    {V : Type uV} [NormedAddCommGroup V] [NormedSpace ℂ V]
    (T : HitchinLinearizedOperator V) : Set ℂ :=
  spectrum ℂ T

/-- Checked operator anchor: the identity linearized operator acts as identity. -/
theorem identityLinearizedOperator_apply
    {V : Type uV} [NormedAddCommGroup V] [NormedSpace ℂ V] (v : V) :
    (ContinuousLinearMap.id ℂ V : HitchinLinearizedOperator V) v = v :=
  ContinuousLinearMap.id_apply v

/-- A small finite-dimensional substrate anchor used for later dimension accounting. -/
theorem complex_finrank_self : Module.finrank ℂ ℂ = 1 := by
  simp

/--
Input data for an abstract-model Hitchin-system theorem.

Concrete fields:
* `hitchinMap` is a map from the Higgs-moduli phase space to the Hitchin base.
* `hamiltonian` is a finite or indexed family of functions on the phase space.
* `poissonBracket` is the bracket whose involutivity must be connected to the
  holomorphic symplectic form.

The algebraic-geometric assertions remain proposition fields because the pinned
local mathlib snapshot does not contain Higgs bundles, the Hitchin fibration, or
the spectral-curve/Jacobian proof package.
-/
structure HitchinSystemData
    (M : Type uM) (B : Type uB) (S : Type uS) (ι : Type uι) :
    Type (max (max uM uB) (max uS uι)) where
  hitchinMap : M → B
  spectralCurve : B → S
  hamiltonian : ι → HamiltonianFunction M
  poissonBracket : PoissonBracket M
  regularBase : Set B
  moduliIsSemistableHiggsBundleModuli : Prop
  baseIsHitchinBase : Prop
  spectralCurveConstructionValid : Prop
  hitchinMapIsAlgebraicMorphism : Prop
  hamiltoniansAreHitchinCoefficients : Prop
  holomorphicSymplecticFormExists : Prop
  pairwisePoissonCommuting : PairwisePoissonCommuting poissonBracket hamiltonian
  regularSpectralCurvesSmooth : Prop
  regularSpectralCurvesSmooth_holds : regularSpectralCurvesSmooth
  genericFiberIsAbelianVariety : Prop
  genericFiberIsAbelianVariety_holds : genericFiberIsAbelianVariety
  regularFibersLagrangian : Prop
  regularFibersLagrangian_holds : regularFibersLagrangian
  dimensionHalfFiber : Prop
  dimensionHalfFiber_holds : dimensionHalfFiber
  completeSetOfHamiltonians : Prop
  completeSetOfHamiltonians_holds : completeSetOfHamiltonians
  algebraicallyCompletelyIntegrable : Prop
  algebraicallyCompletelyIntegrable_holds : algebraicallyCompletelyIntegrable

/-- Fiber of the Hitchin map over a base point. -/
def HitchinFiber {M : Type uM} {B : Type uB} {S : Type uS} {ι : Type uι}
    (D : HitchinSystemData M B S ι) (b : B) : Set M :=
  {x | D.hitchinMap x = b}

/-- Membership in a Hitchin fiber unfolds to the map equation. -/
theorem mem_hitchinFiber_iff
    {M : Type uM} {B : Type uB} {S : Type uS} {ι : Type uι}
    (D : HitchinSystemData M B S ι) (b : B) (x : M) :
    x ∈ HitchinFiber D b ↔ D.hitchinMap x = b :=
  Iff.rfl

/-- Hypotheses retained by the normalized Hitchin-system statement boundary. -/
def HitchinSystemHypotheses
    {M : Type uM} {B : Type uB} {S : Type uS} {ι : Type uι}
    (D : HitchinSystemData M B S ι) : Prop :=
  D.moduliIsSemistableHiggsBundleModuli ∧
    D.baseIsHitchinBase ∧
      D.spectralCurveConstructionValid ∧
        D.hitchinMapIsAlgebraicMorphism ∧
          D.hamiltoniansAreHitchinCoefficients ∧
            D.holomorphicSymplecticFormExists

/-- Conclusion package expected from the Hitchin algebraic-integrability theorem. -/
def HitchinSystemConclusion
    {M : Type uM} {B : Type uB} {S : Type uS} {ι : Type uι}
    (D : HitchinSystemData M B S ι) : Prop :=
  PairwisePoissonCommuting D.poissonBracket D.hamiltonian ∧
    D.regularSpectralCurvesSmooth ∧
      D.genericFiberIsAbelianVariety ∧
        D.regularFibersLagrangian ∧
          D.dimensionHalfFiber ∧
            D.completeSetOfHamiltonians ∧
              D.algebraicallyCompletelyIntegrable

/--
Stage1 normalized statement shape for THM-M-1546.

For every explicitly modeled Hitchin datum satisfying the Higgs-moduli, Hitchin
base, spectral-curve, algebraicity, Hamiltonian, and symplectic-form
hypotheses, the expected output is the algebraically completely integrable
Hitchin fibration: Poisson-commuting Hamiltonians, smooth regular spectral
curves, generic abelian-variety fibers, Lagrangian regular fibers, the half
dimension count, and a complete Hamiltonian family.

This is a statement boundary only; it is not a terminal proof of Hitchin's
theorem.
-/
def StatementShape : Prop :=
  ∀ (M : Type uM) (B : Type uB) (S : Type uS) (ι : Type uι),
    ∀ D : HitchinSystemData M B S ι,
      HitchinSystemHypotheses D → HitchinSystemConclusion D

/--
Public statement-normalization note for THM-M-1546.

`AwesomeTheorems.Stage1.S1_M_205.StatementShape` is the current repo-local
Lean boundary for the Hitchin-system entry.  It packages the expected
Higgs-moduli, Hitchin-base, Hitchin-map, spectral-curve, Poisson-involutivity,
abelian-fiber, Lagrangian-fiber, and dimension-count interfaces, but it is not
a terminal proof of the Hitchin system.
-/
def statementNormalizationNote : String :=
  "AwesomeTheorems.Stage1.S1_M_205.StatementShape is the current repo-local " ++
  "Lean boundary for THM-M-1546; it is not a terminal Hitchin-system proof."

/-- The statement shape unfolds to its explicitly quantified implication. -/
theorem statementShape_iff_forall_data :
    StatementShape.{uM, uB, uS, uι} ↔
      ∀ (M : Type uM) (B : Type uB) (S : Type uS) (ι : Type uι),
        ∀ D : HitchinSystemData M B S ι,
          HitchinSystemHypotheses D → HitchinSystemConclusion D :=
  Iff.rfl

/-- Projection wrapper: the data package exposes Poisson involutivity as an assumed field. -/
theorem HitchinSystemData.pairwise_poisson_commuting
    {M : Type uM} {B : Type uB} {S : Type uS} {ι : Type uι}
    (D : HitchinSystemData M B S ι) :
    PairwisePoissonCommuting D.poissonBracket D.hamiltonian :=
  D.pairwisePoissonCommuting

/-- Projection wrapper: the data package exposes its generic abelian-fiber field. -/
theorem HitchinSystemData.generic_fiber_abelian
    {M : Type uM} {B : Type uB} {S : Type uS} {ι : Type uι}
    (D : HitchinSystemData M B S ι) :
    D.genericFiberIsAbelianVariety :=
  D.genericFiberIsAbelianVariety_holds

/-- Projection wrapper: the conclusion exposes the regular-fiber Lagrangian branch. -/
theorem HitchinSystemConclusion.regular_fibers_lagrangian
    {M : Type uM} {B : Type uB} {S : Type uS} {ι : Type uι}
    {D : HitchinSystemData M B S ι}
    (h : HitchinSystemConclusion D) :
    D.regularFibersLagrangian :=
  h.2.2.2.1

/-- Projection wrapper: the conclusion exposes algebraic complete integrability. -/
theorem HitchinSystemConclusion.algebraically_completely_integrable
    {M : Type uM} {B : Type uB} {S : Type uS} {ι : Type uι}
    {D : HitchinSystemData M B S ι}
    (h : HitchinSystemConclusion D) :
    D.algebraicallyCompletelyIntegrable :=
  h.2.2.2.2.2.2

/-- Pinned mathlib revision used by the Stage1 Hitchin-system audit. -/
def pinnedMathlibRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- Adjacent mathlib modules available at the pinned revision for this Hitchin audit. -/
def availableAdjacentModules : List String := [
  "AlgebraicGeometry.Scheme",
  "AlgebraicGeometry.Morphisms.Smooth",
  "AlgebraicGeometry.Morphisms.Proper",
  "AlgebraicGeometry.Group.Abelian",
  "AlgebraicGeometry.EllipticCurve.Jacobian.Basic",
  "Geometry.Manifold.VectorBundle.Basic",
  "Geometry.Manifold.VectorField.LieBracket",
  "LinearAlgebra.SymplecticGroup",
  "Algebra.Algebra.Spectrum.Basic",
  "Analysis.Normed.Operator.Basic",
  "LinearAlgebra.Dimension.Finrank"
]

/-- The pinned-adjacent-module audit records the eleven modules requested by Stage1. -/
theorem availableAdjacentModules_length : availableAdjacentModules.length = 11 := by
  rfl

/-!
## Missing formal API split

`THM-M-1546.missing-api` is a formalization-debt inventory.  The checked
declarations below split the missing Hitchin-system formal surface into stable
M0387-style leaves without adding assumptions, unproved constants, or a
terminal theorem claim.
-/

/-- Canonical missing formal-API packages for the Hitchin-system theorem. -/
inductive HitchinMissingAPIPackage where
  | higgsBundles
  | semistabilityModuli
  | hitchinBase
  | hitchinMap
  | spectralCurves
  | regularLocus
  | spectralCorrespondence
  | jacobianPrymFibers
  | holomorphicSymplecticForm
  | poissonBracket
  | lagrangianFibers
  | dimensionCount
  deriving DecidableEq, Repr

namespace HitchinMissingAPIPackage

/-- Stable public task name for a missing formal-API package. -/
def canonicalTaskName : HitchinMissingAPIPackage → String
  | higgsBundles =>
      "THM-M-1546.missing-api.higgs-bundles"
  | semistabilityModuli =>
      "THM-M-1546.missing-api.semistability-moduli"
  | hitchinBase =>
      "THM-M-1546.missing-api.hitchin-base"
  | hitchinMap =>
      "THM-M-1546.missing-api.hitchin-map"
  | spectralCurves =>
      "THM-M-1546.missing-api.spectral-curves"
  | regularLocus =>
      "THM-M-1546.missing-api.regular-locus"
  | spectralCorrespondence =>
      "THM-M-1546.missing-api.spectral-correspondence"
  | jacobianPrymFibers =>
      "THM-M-1546.missing-api.jacobian-prym-fibers"
  | holomorphicSymplecticForm =>
      "THM-M-1546.missing-api.holomorphic-symplectic-form"
  | poissonBracket =>
      "THM-M-1546.missing-api.poisson-bracket"
  | lagrangianFibers =>
      "THM-M-1546.missing-api.lagrangian-fibers"
  | dimensionCount =>
      "THM-M-1546.missing-api.dimension-count"

/-- Human-readable payload required before the package can close repo-locally. -/
def requiredPayload : HitchinMissingAPIPackage → String
  | higgsBundles =>
      "define Higgs bundles over the chosen smooth projective curve, including vector bundle, Higgs field, twisting line bundle, and characteristic-polynomial data"
  | semistabilityModuli =>
      "define stability and semistability for Higgs bundles and construct or import the moduli space or stack used as the Hitchin phase space"
  | hitchinBase =>
      "construct the Hitchin base from invariant polynomials or characteristic coefficients with the needed vector-space and algebraic-geometry structure"
  | hitchinMap =>
      "define the Hitchin map from Higgs-bundle moduli to the Hitchin base and prove its algebraicity/properness properties required by the theorem"
  | spectralCurves =>
      "construct spectral curves from base points and relate them to the characteristic equation inside the total space of the twisting line bundle"
  | regularLocus =>
      "define the regular or smooth spectral-curve locus in the Hitchin base and prove the basic openness/smoothness facts needed downstream"
  | spectralCorrespondence =>
      "formalize the correspondence between regular Higgs bundles and line bundles or torsion-free rank-one sheaves on spectral curves"
  | jacobianPrymFibers =>
      "identify generic Hitchin fibers with Jacobian or Prym-type abelian varieties, including the relevant norm or determinant constraints"
  | holomorphicSymplecticForm =>
      "construct the holomorphic symplectic form on the Higgs-moduli phase space and connect it to tangent-complex or hypercohomology data"
  | poissonBracket =>
      "derive the Poisson bracket on Hamiltonian functions from the holomorphic symplectic form and prove the Hitchin Hamiltonians commute"
  | lagrangianFibers =>
      "prove regular Hitchin fibers are isotropic and half-dimensional, hence Lagrangian with respect to the holomorphic symplectic form"
  | dimensionCount =>
      "prove the dimension formula for the moduli space, Hitchin base, and regular fibers that supplies the complete-integrability count"

/-- Current repo-local boundary for each missing package. -/
def currentBoundary : HitchinMissingAPIPackage → String
  | higgsBundles =>
      "only an abstract proposition field `moduliIsSemistableHiggsBundleModuli` is present"
  | semistabilityModuli =>
      "semistability and the moduli object are not defined; the statement shape assumes them as a proposition"
  | hitchinBase =>
      "only the carrier type `B` and proposition field `baseIsHitchinBase` are present"
  | hitchinMap =>
      "only the function field `hitchinMap : M -> B` and proposition field `hitchinMapIsAlgebraicMorphism` are present"
  | spectralCurves =>
      "only the function field `spectralCurve : B -> S` and proposition field `spectralCurveConstructionValid` are present"
  | regularLocus =>
      "only the set field `regularBase : Set B` and proposition field `regularSpectralCurvesSmooth` are present"
  | spectralCorrespondence =>
      "no repo-local spectral-correspondence structure or theorem exists in this artifact"
  | jacobianPrymFibers =>
      "only proposition fields for generic abelian-variety fibers are present"
  | holomorphicSymplecticForm =>
      "only the proposition field `holomorphicSymplecticFormExists` is present"
  | poissonBracket =>
      "the bracket is an abstract binary operation; only the zero-bracket toy case is proved"
  | lagrangianFibers =>
      "only proposition fields for regular Lagrangian fibers are present"
  | dimensionCount =>
      "only proposition fields and the scalar anchor `Module.finrank C C = 1` are present"

end HitchinMissingAPIPackage

/-- One M0387-style repo-local leaf for a missing Hitchin formal-API package. -/
structure HitchinMissingAPILeaf where
  package : HitchinMissingAPIPackage
  taskName : String
  requiredPayload : String
  currentBoundary : String
  currentStatus : String
  debtClass : String
  repoLocalClosed : Bool
  leafBudgetBound : Nat
  derivesFromPackageName : taskName = package.canonicalTaskName

/--
Integration-ready split of `THM-M-1546.missing-api`.

Every leaf is currently unchecked `formalization_debt`: this file records the
missing API frontier but does not construct Higgs-bundle moduli, the Hitchin
fibration, spectral correspondence, Jacobian/Prym fibers, symplectic geometry,
Poisson involutivity, Lagrangian fibers, or the terminal dimension count.
-/
def hitchinMissingAPILeaves : List HitchinMissingAPILeaf := [
  {
    package := .higgsBundles
    taskName := HitchinMissingAPIPackage.higgsBundles.canonicalTaskName
    requiredPayload := HitchinMissingAPIPackage.higgsBundles.requiredPayload
    currentBoundary := HitchinMissingAPIPackage.higgsBundles.currentBoundary
    currentStatus := "unchecked"
    debtClass := "formalization_debt"
    repoLocalClosed := false
    leafBudgetBound := 100
    derivesFromPackageName := rfl
  },
  {
    package := .semistabilityModuli
    taskName := HitchinMissingAPIPackage.semistabilityModuli.canonicalTaskName
    requiredPayload := HitchinMissingAPIPackage.semistabilityModuli.requiredPayload
    currentBoundary := HitchinMissingAPIPackage.semistabilityModuli.currentBoundary
    currentStatus := "unchecked"
    debtClass := "formalization_debt"
    repoLocalClosed := false
    leafBudgetBound := 100
    derivesFromPackageName := rfl
  },
  {
    package := .hitchinBase
    taskName := HitchinMissingAPIPackage.hitchinBase.canonicalTaskName
    requiredPayload := HitchinMissingAPIPackage.hitchinBase.requiredPayload
    currentBoundary := HitchinMissingAPIPackage.hitchinBase.currentBoundary
    currentStatus := "unchecked"
    debtClass := "formalization_debt"
    repoLocalClosed := false
    leafBudgetBound := 100
    derivesFromPackageName := rfl
  },
  {
    package := .hitchinMap
    taskName := HitchinMissingAPIPackage.hitchinMap.canonicalTaskName
    requiredPayload := HitchinMissingAPIPackage.hitchinMap.requiredPayload
    currentBoundary := HitchinMissingAPIPackage.hitchinMap.currentBoundary
    currentStatus := "unchecked"
    debtClass := "formalization_debt"
    repoLocalClosed := false
    leafBudgetBound := 100
    derivesFromPackageName := rfl
  },
  {
    package := .spectralCurves
    taskName := HitchinMissingAPIPackage.spectralCurves.canonicalTaskName
    requiredPayload := HitchinMissingAPIPackage.spectralCurves.requiredPayload
    currentBoundary := HitchinMissingAPIPackage.spectralCurves.currentBoundary
    currentStatus := "unchecked"
    debtClass := "formalization_debt"
    repoLocalClosed := false
    leafBudgetBound := 100
    derivesFromPackageName := rfl
  },
  {
    package := .regularLocus
    taskName := HitchinMissingAPIPackage.regularLocus.canonicalTaskName
    requiredPayload := HitchinMissingAPIPackage.regularLocus.requiredPayload
    currentBoundary := HitchinMissingAPIPackage.regularLocus.currentBoundary
    currentStatus := "unchecked"
    debtClass := "formalization_debt"
    repoLocalClosed := false
    leafBudgetBound := 100
    derivesFromPackageName := rfl
  },
  {
    package := .spectralCorrespondence
    taskName := HitchinMissingAPIPackage.spectralCorrespondence.canonicalTaskName
    requiredPayload := HitchinMissingAPIPackage.spectralCorrespondence.requiredPayload
    currentBoundary := HitchinMissingAPIPackage.spectralCorrespondence.currentBoundary
    currentStatus := "unchecked"
    debtClass := "formalization_debt"
    repoLocalClosed := false
    leafBudgetBound := 100
    derivesFromPackageName := rfl
  },
  {
    package := .jacobianPrymFibers
    taskName := HitchinMissingAPIPackage.jacobianPrymFibers.canonicalTaskName
    requiredPayload := HitchinMissingAPIPackage.jacobianPrymFibers.requiredPayload
    currentBoundary := HitchinMissingAPIPackage.jacobianPrymFibers.currentBoundary
    currentStatus := "unchecked"
    debtClass := "formalization_debt"
    repoLocalClosed := false
    leafBudgetBound := 100
    derivesFromPackageName := rfl
  },
  {
    package := .holomorphicSymplecticForm
    taskName := HitchinMissingAPIPackage.holomorphicSymplecticForm.canonicalTaskName
    requiredPayload := HitchinMissingAPIPackage.holomorphicSymplecticForm.requiredPayload
    currentBoundary := HitchinMissingAPIPackage.holomorphicSymplecticForm.currentBoundary
    currentStatus := "unchecked"
    debtClass := "formalization_debt"
    repoLocalClosed := false
    leafBudgetBound := 100
    derivesFromPackageName := rfl
  },
  {
    package := .poissonBracket
    taskName := HitchinMissingAPIPackage.poissonBracket.canonicalTaskName
    requiredPayload := HitchinMissingAPIPackage.poissonBracket.requiredPayload
    currentBoundary := HitchinMissingAPIPackage.poissonBracket.currentBoundary
    currentStatus := "unchecked"
    debtClass := "formalization_debt"
    repoLocalClosed := false
    leafBudgetBound := 100
    derivesFromPackageName := rfl
  },
  {
    package := .lagrangianFibers
    taskName := HitchinMissingAPIPackage.lagrangianFibers.canonicalTaskName
    requiredPayload := HitchinMissingAPIPackage.lagrangianFibers.requiredPayload
    currentBoundary := HitchinMissingAPIPackage.lagrangianFibers.currentBoundary
    currentStatus := "unchecked"
    debtClass := "formalization_debt"
    repoLocalClosed := false
    leafBudgetBound := 100
    derivesFromPackageName := rfl
  },
  {
    package := .dimensionCount
    taskName := HitchinMissingAPIPackage.dimensionCount.canonicalTaskName
    requiredPayload := HitchinMissingAPIPackage.dimensionCount.requiredPayload
    currentBoundary := HitchinMissingAPIPackage.dimensionCount.currentBoundary
    currentStatus := "unchecked"
    debtClass := "formalization_debt"
    repoLocalClosed := false
    leafBudgetBound := 100
    derivesFromPackageName := rfl
  }
]

/-- The missing formal-API split has exactly the twelve packages requested by Stage1. -/
theorem hitchinMissingAPILeaves_length :
    hitchinMissingAPILeaves.length = 12 :=
  rfl

/-- The missing formal-API split records the requested packages in public order. -/
theorem hitchinMissingAPILeaves_packages_eq :
    hitchinMissingAPILeaves.map (fun leaf => leaf.package) = [
      HitchinMissingAPIPackage.higgsBundles,
      HitchinMissingAPIPackage.semistabilityModuli,
      HitchinMissingAPIPackage.hitchinBase,
      HitchinMissingAPIPackage.hitchinMap,
      HitchinMissingAPIPackage.spectralCurves,
      HitchinMissingAPIPackage.regularLocus,
      HitchinMissingAPIPackage.spectralCorrespondence,
      HitchinMissingAPIPackage.jacobianPrymFibers,
      HitchinMissingAPIPackage.holomorphicSymplecticForm,
      HitchinMissingAPIPackage.poissonBracket,
      HitchinMissingAPIPackage.lagrangianFibers,
      HitchinMissingAPIPackage.dimensionCount
    ] :=
  rfl

/-- No missing formal-API leaf is repo-locally closed by this Stage1 scaffold. -/
theorem hitchinMissingAPILeaves_repoLocalClosed_eq :
    hitchinMissingAPILeaves.map (fun leaf => leaf.repoLocalClosed) =
      [false, false, false, false, false, false, false, false, false, false, false, false] :=
  rfl

/-- Each missing formal-API leaf keeps the M0387 local expansion budget at `100`. -/
theorem hitchinMissingAPILeaves_budget_eq :
    hitchinMissingAPILeaves.map (fun leaf => leaf.leafBudgetBound) =
      [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100] :=
  rfl

/-- Each missing formal-API leaf remains unchecked formalization debt. -/
theorem hitchinMissingAPILeaves_statusDebt_eq :
    hitchinMissingAPILeaves.map
        (fun leaf => (leaf.currentStatus, leaf.debtClass)) = [
      ("unchecked", "formalization_debt"),
      ("unchecked", "formalization_debt"),
      ("unchecked", "formalization_debt"),
      ("unchecked", "formalization_debt"),
      ("unchecked", "formalization_debt"),
      ("unchecked", "formalization_debt"),
      ("unchecked", "formalization_debt"),
      ("unchecked", "formalization_debt"),
      ("unchecked", "formalization_debt"),
      ("unchecked", "formalization_debt"),
      ("unchecked", "formalization_debt"),
      ("unchecked", "formalization_debt")
    ] :=
  rfl

/-- Integration-ready public missing-API note for `THM-M-1546.missing-api`. -/
def hitchinMissingAPIPublicBackfillNotes : List String := [
  "THM-M-1546.missing-api is split into twelve repo-local leaves recorded by AwesomeTheorems.Stage1.S1_M_205.HitchinMissingAPIPackage and hitchinMissingAPILeaves.",
  "The twelve leaves are Higgs bundles; semistability/moduli; Hitchin base; Hitchin map; spectral curves; regular locus; spectral correspondence; Jacobian/Prym fibers; holomorphic symplectic form; Poisson bracket; Lagrangian fibers; and dimension-count packages.",
  "The checked guards hitchinMissingAPILeaves_length, hitchinMissingAPILeaves_repoLocalClosed_eq, and hitchinMissingAPILeaves_statusDebt_eq record that this is an unchecked formalization-debt inventory, not terminal Hitchin-system completion."
]

/-- mathlib imports checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.AlgebraicGeometry.Scheme",
  "Mathlib.AlgebraicGeometry.Morphisms.Smooth",
  "Mathlib.AlgebraicGeometry.Morphisms.Proper",
  "Mathlib.AlgebraicGeometry.Group.Abelian",
  "Mathlib.AlgebraicGeometry.EllipticCurve.Jacobian.Basic",
  "Mathlib.Geometry.Manifold.VectorBundle.Basic",
  "Mathlib.Geometry.Manifold.VectorField.LieBracket",
  "Mathlib.LinearAlgebra.SymplecticGroup",
  "Mathlib.Algebra.Algebra.Spectrum.Basic",
  "Mathlib.Analysis.Normed.Operator.Basic",
  "Mathlib.LinearAlgebra.Dimension.Finrank"
]

/-- Nearby checked names used or audited for the Hitchin-system boundary. -/
def mathlibAnchorNames : List String := [
  "AlgebraicGeometry.Scheme",
  "AlgebraicGeometry.IsSmooth",
  "AlgebraicGeometry.IsProper",
  "AlgebraicGeometry.AbelianScheme",
  "AlgebraicGeometry.EllipticCurve.Jacobian",
  "VectorBundle",
  "VectorField.mlieBracket",
  "Matrix.symplecticGroup",
  "ContinuousLinearMap",
  "spectrum",
  "Module.finrank"
]

/-- Search terms that did not locate a terminal Hitchin-system theorem in pinned local mathlib. -/
def absentTerminalSearchTerms : List String := [
  "Hitchin",
  "Hitchin system",
  "Hitchin map",
  "HitchinMap",
  "Higgs bundle",
  "HiggsBundle",
  "spectral curve",
  "algebraic integrable system",
  "Lagrangian fibration"
]

/-- Exact external-primary-source search terms requested by `THM-M-1546.external-audit`. -/
def externalAuditSearchTerms : List String := [
  "Hitchin",
  "Hitchin system",
  "Hitchin map",
  "HitchinMap",
  "Higgs bundle",
  "HiggsBundle",
  "spectral curve",
  "Prym",
  "Jacobian",
  "Lagrangian fibration",
  "algebraic integrable system",
  "completely integrable"
]

/-- The external audit term list records all twelve requested search terms. -/
theorem externalAuditSearchTerms_length :
    externalAuditSearchTerms.length = 12 :=
  rfl

/-!
## Integration gate

`THM-M-1546.integration-gate` is a repo-local completion gate.  It does not
prove any Hitchin-system theorem.  It records that this artifact has not found
or imported a terminal external Lean 4 closure, and that completion cannot be
claimed while the authenticated external audit is still open.
-/

/-- Repo-local metadata for the Hitchin-system external integration gate. -/
structure HitchinIntegrationGate where
  externalLeanClosureFound : Bool
  authenticatedExternalSearchComplete : Bool
  externalClosurePinnedImportedChecked : Bool
  concreteIntegrationBlockerRecorded : Bool
  repoLocalIntegrationDebtRetainedAsCompleted : Bool
  publicCompletionClaimAllowed : Bool
  currentMachineStatus : String
  currentDebtClass : String
  gateNote : String

/--
Current repo-local integration-gate status for `THM-M-1546`.

The previous child audit found only adjacent pinned mathlib infrastructure and
did not identify a terminal Lean 4 Hitchin-system proof.  It also recorded that
authenticated GitHub code search was not available in that runtime.  Therefore
the safe gate state is no public completion claim: finish the authenticated
external audit first, and if a terminal upstream proof is later found, pin,
import, and check it, or record the concrete toolchain/license/dependency
blocker.
-/
def hitchinIntegrationGate : HitchinIntegrationGate where
  externalLeanClosureFound := false
  authenticatedExternalSearchComplete := false
  externalClosurePinnedImportedChecked := false
  concreteIntegrationBlockerRecorded := true
  repoLocalIntegrationDebtRetainedAsCompleted := false
  publicCompletionClaimAllowed := false
  currentMachineStatus := "not_repo_local_closed"
  currentDebtClass := "formalization_debt"
  gateNote :=
    "No terminal external Lean 4 Hitchin-system closure is pinned/imported/checked in this repo. " ++
    "Authenticated external search remains open; if an upstream closure is later found, " ++
    "pin/import/check it or record a concrete integration blocker before any completion claim."

/-- The current integration gate does not allow a public completion claim. -/
theorem hitchinIntegrationGate_no_public_completion :
    hitchinIntegrationGate.publicCompletionClaimAllowed = false :=
  rfl

/-- The current integration gate does not retain repo-local integration debt as completed. -/
theorem hitchinIntegrationGate_no_completed_integration_debt :
    hitchinIntegrationGate.repoLocalIntegrationDebtRetainedAsCompleted = false :=
  rfl

/-- The current integration gate records that authenticated external search remains open. -/
theorem hitchinIntegrationGate_external_search_open :
    hitchinIntegrationGate.authenticatedExternalSearchComplete = false :=
  rfl

/-- Integration-ready public note for `THM-M-1546.integration-gate`. -/
def hitchinIntegrationGatePublicBackfillNote : String :=
  "THM-M-1546.integration-gate remains open: the repo-local Lean artifact " ++
  "AwesomeTheorems.Stage1.S1_M_205.hitchinIntegrationGate validates that no public " ++
  "completion claim is allowed, no repo-local integration debt is being retained as " ++
  "completed, and authenticated external search must be completed before any upstream " ++
  "Lean closure can be pinned/imported/checked or blocked."

/-! ## Audit probes retained in the checked file. -/

#check HamiltonianFunction
#check PoissonBracket
#check PairwisePoissonCommuting
#check pairwisePoissonCommuting_zero
#check HitchinLinearizedOperator
#check LinearizedSpectrum
#check identityLinearizedOperator_apply
#check complex_finrank_self
#check HitchinSystemData
#check HitchinFiber
#check mem_hitchinFiber_iff
#check HitchinSystemHypotheses
#check HitchinSystemConclusion
#check StatementShape
#check statementNormalizationNote
#check pinnedMathlibRevision
#check availableAdjacentModules
#check availableAdjacentModules_length
#check HitchinMissingAPIPackage
#check HitchinMissingAPIPackage.canonicalTaskName
#check HitchinMissingAPIPackage.requiredPayload
#check HitchinMissingAPIPackage.currentBoundary
#check HitchinMissingAPILeaf
#check hitchinMissingAPILeaves
#check hitchinMissingAPILeaves_length
#check hitchinMissingAPILeaves_packages_eq
#check hitchinMissingAPILeaves_repoLocalClosed_eq
#check hitchinMissingAPILeaves_budget_eq
#check hitchinMissingAPILeaves_statusDebt_eq
#check hitchinMissingAPIPublicBackfillNotes
#check externalAuditSearchTerms
#check externalAuditSearchTerms_length
#check HitchinIntegrationGate
#check hitchinIntegrationGate
#check hitchinIntegrationGate_no_public_completion
#check hitchinIntegrationGate_no_completed_integration_debt
#check hitchinIntegrationGate_external_search_open
#check hitchinIntegrationGatePublicBackfillNote
#check spectrum
#check ContinuousLinearMap.id
#check Module.finrank
#check Matrix.symplecticGroup

end S1_M_205
end Stage1
end AwesomeTheorems
