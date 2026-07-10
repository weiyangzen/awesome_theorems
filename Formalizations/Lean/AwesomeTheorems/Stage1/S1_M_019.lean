import Mathlib.AlgebraicGeometry.Scheme
import Mathlib.AlgebraicGeometry.Morphisms.Basic
import Mathlib.AlgebraicGeometry.Morphisms.ClosedImmersion
import Mathlib.AlgebraicGeometry.Morphisms.FiniteType
import Mathlib.AlgebraicGeometry.Morphisms.OpenImmersion
import Mathlib.AlgebraicGeometry.Morphisms.Proper
import Mathlib.AlgebraicGeometry.Morphisms.Smooth
import Mathlib.NumberTheory.DiophantineApproximation.Basic
import Mathlib.NumberTheory.Height.Basic
import Mathlib.NumberTheory.Height.Northcott
import Mathlib.NumberTheory.NumberField.Completion.FinitePlace
import Mathlib.NumberTheory.NumberField.ProductFormula
import Mathlib.NumberTheory.SiegelsLemma

/-!
# S1-M-019 / THM-M-0406: Corvaja--Zannier integral-points degeneracy

This Stage1 artifact resolves the local naming mismatch for `THM-M-0406`.
The canonical target selected here is the Corvaja--Zannier 2004 surface
degeneracy theorem, not a Corlette--Evertse theorem and not the
Evertse--Ferretti projective-variety inequality itself.

Primary-source alignment recorded by the child ledger:

* Pietro Corvaja and Umberto Zannier, "On integral points on surfaces",
  Annals of Mathematics 160 (2004), 705-726, DOI 10.4007/annals.2004.160.705.
* The 2004 result uses a Schmidt Subspace Theorem method and concludes,
  under hypotheses on divisors at infinity, that integral points on a surface
  lie on a curve.
* Evertse--Ferretti inequalities are relevant arithmetic-input technology for
  nearby subspace-theorem generalizations, but they do not match the Stage0
  year/content row as the root theorem for `THM-M-0406`.

The declarations below freeze a conservative theorem-internal data shape
without using kernel holes or axiomatizing the theorem.
-/

noncomputable section

open AlgebraicGeometry

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_019

universe u v

/-- Candidate roots considered during the naming-mismatch audit. -/
inductive CandidateTarget where
  | corvajaZannier2004SurfaceDegeneracy
  | corvajaZannier2002CurveSiegelMethod
  | evertseFerrettiProjectiveVarietyInequality
  | unresolvedCorvajaEvertseLabel
  deriving DecidableEq, Repr

/--
Canonical target selected for `THM-M-0406`.

This is intentionally machine-checked as data: downstream public-doc backfill
can cite the checked artifact for the local decision, while still treating the
mathematical theorem as unformalized.
-/
def canonicalTarget : CandidateTarget :=
  CandidateTarget.corvajaZannier2004SurfaceDegeneracy

/-- The local naming audit selects the Corvaja--Zannier 2004 surface theorem. -/
theorem canonicalTarget_eq_corvajaZannier2004 :
    canonicalTarget =
      CandidateTarget.corvajaZannier2004SurfaceDegeneracy :=
  rfl

/-- Source anchors used to disambiguate the Stage1 root theorem. -/
def primarySourceAnchors : List String := [
  "Pietro Corvaja and Umberto Zannier, On integral points on surfaces, Annals of Mathematics 160 (2004), 705-726",
  "DOI 10.4007/annals.2004.160.705",
  "arXiv math/0206100, On integral points on surfaces"
]

/--
Arithmetic base data for an integral-points-on-surfaces statement.

`S` is the set of allowed finite places.  The finiteness assertion is kept as
an explicit field so that later work can replace it by the preferred mathlib
`Set.Finite`/`Finset` encoding for the selected statement.
-/
structure ArithmeticBase where
  K : Type u
  fieldK : Field K
  numberFieldK : NumberField K
  admissibleAbsValues : Height.AdmissibleAbsValues K
  S : Set (NumberField.FinitePlace K)
  SFinite : Prop

attribute [instance] ArithmeticBase.fieldK
attribute [instance] ArithmeticBase.numberFieldK
attribute [instance] ArithmeticBase.admissibleAbsValues

/--
Surface and boundary data for the Corvaja--Zannier degeneracy theorem.

The current local artifact intentionally keeps the geometric predicates as
named propositions.  This avoids pretending that the scheme, divisor,
intersection-theory, and `S`-integral-point APIs for the full theorem have
already been selected.
-/
structure SurfaceBoundaryData (B : ArithmeticBase.{u}) :
    Type (max (u + 1) (v + 1)) where
  compactSurface : Scheme.{v}
  openSurface : Scheme.{v}
  integralModel : Type v
  boundaryDivisorFamily : Type v
  isSmoothProjectiveSurface : Prop
  openSurfaceIsComplementOfBoundary : Prop
  modelIsSIntegral : Prop
  boundaryIntersectionHypothesis : Prop
  heightFunction : openSurface.carrier -> ℝ
  integralPoint : Type v
  pointToSurface : integralPoint -> openSurface.carrier
  isSIntegralPoint : integralPoint -> Prop
  degeneracyCurve : Set openSurface.carrier
  degeneracyCurveProper : Prop
  pointInDegeneracyCurve : integralPoint -> Prop

/--
The theorem-internal hypothesis package expected before the
Corvaja--Zannier conclusion can be invoked.
-/
def HasCorvajaZannierHypotheses
    {B : ArithmeticBase.{u}} (X : SurfaceBoundaryData.{u, v} B) : Prop :=
  B.SFinite ∧
    X.isSmoothProjectiveSurface ∧
      X.openSurfaceIsComplementOfBoundary ∧
        X.modelIsSIntegral ∧
          X.boundaryIntersectionHypothesis ∧
            X.degeneracyCurveProper

/--
Degeneracy conclusion: every selected `S`-integral point maps into the recorded
proper curve.
-/
def IntegralPointsDegenerate
    {B : ArithmeticBase.{u}} (X : SurfaceBoundaryData.{u, v} B) : Prop :=
  ∀ P : X.integralPoint,
    X.isSIntegralPoint P ->
      X.pointInDegeneracyCurve P

/--
Consistency condition tying the point-level predicate to the underlying subset
of the open surface.
-/
def DegeneracyPredicateMatchesCurve
    {B : ArithmeticBase.{u}} (X : SurfaceBoundaryData.{u, v} B) : Prop :=
  ∀ P : X.integralPoint,
    X.pointInDegeneracyCurve P ↔
      X.pointToSurface P ∈ X.degeneracyCurve

/--
Normalized Stage1 statement shape for THM-M-0406.

This is a `Prop` boundary, not a proof that the Corvaja--Zannier theorem has
been formalized locally.  Later work should replace the abstract geometric
fields with the exact selected formulation and either a local proof body, a
mathlib wrapper, or a pinned external Lean 4 dependency.
-/
def StatementShape : Prop :=
  canonicalTarget =
      CandidateTarget.corvajaZannier2004SurfaceDegeneracy ∧
    ∀ (B : ArithmeticBase.{u}) (X : SurfaceBoundaryData.{u, v} B),
      HasCorvajaZannierHypotheses X ->
        DegeneracyPredicateMatchesCurve X ->
          IntegralPointsDegenerate X

/-- The statement shape unfolds to the explicit target-selection plus theorem implication. -/
theorem statementShape_iff :
    StatementShape.{u, v} ↔
      canonicalTarget =
          CandidateTarget.corvajaZannier2004SurfaceDegeneracy ∧
        ∀ (B : ArithmeticBase.{u}) (X : SurfaceBoundaryData.{u, v} B),
          HasCorvajaZannierHypotheses X ->
            DegeneracyPredicateMatchesCurve X ->
              IntegralPointsDegenerate X :=
  Iff.rfl

/-- Projection wrapper for the finite-place hypothesis in the arithmetic base. -/
theorem finitePlaceSet_premise
    {B : ArithmeticBase.{u}} {X : SurfaceBoundaryData.{u, v} B}
    (h : HasCorvajaZannierHypotheses X) :
    B.SFinite :=
  h.1

/-- Projection wrapper for the selected boundary intersection hypothesis. -/
theorem boundaryIntersection_premise
    {B : ArithmeticBase.{u}} {X : SurfaceBoundaryData.{u, v} B}
    (h : HasCorvajaZannierHypotheses X) :
    X.boundaryIntersectionHypothesis :=
  h.2.2.2.2.1

/-- Projection wrapper for the properness of the recorded degeneracy curve. -/
theorem degeneracyCurveProper_premise
    {B : ArithmeticBase.{u}} (X : SurfaceBoundaryData.{u, v} B)
    (h : HasCorvajaZannierHypotheses X) :
    X.degeneracyCurveProper :=
  h.2.2.2.2.2

/--
Checked local wrapper: a proof of `StatementShape` supplies the degeneracy
conclusion for a particular arithmetic base and surface package.
-/
theorem integralPointsDegenerate_of_statementShape
    (h : StatementShape.{u, v})
    (B : ArithmeticBase.{u}) (X : SurfaceBoundaryData.{u, v} B)
    (hX : HasCorvajaZannierHypotheses X)
    (hmatch : DegeneracyPredicateMatchesCurve X) :
    IntegralPointsDegenerate X :=
  h.2 B X hX hmatch

/--
Checked local wrapper: a degenerate empty integral-point type satisfies the
conclusion for any recorded surface package.
-/
theorem integralPointsDegenerate_of_isEmpty
    {B : ArithmeticBase.{u}} (X : SurfaceBoundaryData.{u, v} B)
    [IsEmpty X.integralPoint] :
    IntegralPointsDegenerate X := by
  intro P
  exact False.elim (isEmptyElim P)

/-! ## Subspace-method proof-package split

The declarations in this section are an executable inventory for the
Corvaja--Zannier proof route.  They intentionally record package boundaries
and machine-state gates only; they do not assert that the subspace-method proof
has been formalized in this repository.
-/

/-- Statement/audit/proof-package classification for this Stage1 slot. -/
inductive WorkSurface where
  | statement
  | audit
  | proofPackage
  | integrationGate
  deriving DecidableEq, Repr

/-- Machine states allowed by the M0387-level completion gate. -/
inductive MachineState where
  | localProofBody
  | localWrapperUpstreamMathlib
  | externalUpstreamPinned
  | externalUpstreamAnchorOnly
  | notRepoLocalClosed
  deriving DecidableEq, Repr

/-- Machine-proof debt labels used by the Stage1 audit. -/
inductive MachineProofDebt where
  | mathematicalDebt
  | formalizationDebt
  | repoLocalIntegrationDebt
  deriving DecidableEq, Repr

/--
Proof packages for the Corvaja--Zannier subspace-method route.

These names are stable local handles for public backfill.  They are not
competing canonical theorem names and they are not completion certificates.
-/
inductive SubspaceMethodPackage where
  | statementAndBoundaryNormalization
  | divisorIntersectionGeometry
  | heightAndSIntegralPointSetup
  | subspaceTheoremInput
  | auxiliarySectionOrFunctionConstruction
  | exceptionalSubspaceToCurveDescent
  | repoLocalIntegrationGate
  deriving DecidableEq, Repr

/-- A checked row in the package-level proof split. -/
structure SubspaceMethodPackageRow where
  package : SubspaceMethodPackage
  surface : WorkSurface
  label : String
  upstreamInput : String
  obligation : String
  downstreamOutput : String
  leafBudget : String
  status : String
  debt : MachineProofDebt
  machineState : MachineState

/--
Package split for the Corvaja--Zannier 2004 surface theorem.

Every row is intentionally marked open/formalization-debt unless it is merely a
checked statement-boundary scaffold already represented by this file.
-/
def subspaceMethodPackageSplit : List SubspaceMethodPackageRow := [
  {
    package := SubspaceMethodPackage.statementAndBoundaryNormalization
    surface := WorkSurface.statement
    label := "CZ.Pkg01.StatementAndBoundaryNormalization"
    upstreamInput := "primary source theorem statement and Stage1 canonical-target audit"
    obligation := "freeze the number field, finite set of places, surface, open complement, boundary divisors, and proper-curve conclusion"
    downstreamOutput := "ArithmeticBase, SurfaceBoundaryData, HasCorvajaZannierHypotheses, IntegralPointsDegenerate"
    leafBudget := "<=100 per eventual proof leaf"
    status := "partially represented by checked statement-boundary declarations in this file"
    debt := MachineProofDebt.formalizationDebt
    machineState := MachineState.notRepoLocalClosed
  },
  {
    package := SubspaceMethodPackage.divisorIntersectionGeometry
    surface := WorkSurface.proofPackage
    label := "CZ.Pkg02.DivisorIntersectionGeometry"
    upstreamInput := "smooth projective surface plus divisor-at-infinity family"
    obligation := "select a mathlib object model for divisors, supports, complements, intersection data, and the positivity/nondegeneracy hypotheses used by the theorem"
    downstreamOutput := "boundaryIntersectionHypothesis with a concrete divisor/intersection API"
    leafBudget := "unchecked; split into <=100-step local leaves after API selection"
    status := "open formalization debt"
    debt := MachineProofDebt.formalizationDebt
    machineState := MachineState.notRepoLocalClosed
  },
  {
    package := SubspaceMethodPackage.heightAndSIntegralPointSetup
    surface := WorkSurface.proofPackage
    label := "CZ.Pkg03.HeightAndSIntegralPointSetup"
    upstreamInput := "ArithmeticBase, height admissibility, open surface, and integral model"
    obligation := "define S-integral points on the complement and connect their local height/valuation bounds to the chosen divisor package"
    downstreamOutput := "height inequalities for points satisfying isSIntegralPoint"
    leafBudget := "unchecked; split into <=100-step local leaves after height/integral-point API selection"
    status := "open formalization debt"
    debt := MachineProofDebt.formalizationDebt
    machineState := MachineState.notRepoLocalClosed
  },
  {
    package := SubspaceMethodPackage.subspaceTheoremInput
    surface := WorkSurface.proofPackage
    label := "CZ.Pkg04.SubspaceTheoremInput"
    upstreamInput := "height and local divisor inequalities from CZ.Pkg03"
    obligation := "instantiate Schmidt Subspace Theorem or an Evertse--Ferretti-style projective-variety inequality with the linear forms/sections produced by the surface data"
    downstreamOutput := "finite exceptional linear/projective subspace cover for the relevant integral points"
    leafBudget := "unchecked; terminal theorem or pinned dependency still absent"
    status := "open formalization debt; no anchor-only completion claim"
    debt := MachineProofDebt.formalizationDebt
    machineState := MachineState.notRepoLocalClosed
  },
  {
    package := SubspaceMethodPackage.auxiliarySectionOrFunctionConstruction
    surface := WorkSurface.proofPackage
    label := "CZ.Pkg05.AuxiliarySectionOrFunctionConstruction"
    upstreamInput := "boundary divisor geometry and the selected subspace-theorem formulation"
    obligation := "construct the rational functions or projective sections whose local vanishing/divisor behavior feeds the subspace-theorem inequality"
    downstreamOutput := "linear-form or section family satisfying the hypotheses of CZ.Pkg04"
    leafBudget := "unchecked; split after divisor and line-bundle APIs are fixed"
    status := "open formalization debt"
    debt := MachineProofDebt.formalizationDebt
    machineState := MachineState.notRepoLocalClosed
  },
  {
    package := SubspaceMethodPackage.exceptionalSubspaceToCurveDescent
    surface := WorkSurface.proofPackage
    label := "CZ.Pkg06.ExceptionalSubspaceToCurveDescent"
    upstreamInput := "exceptional subspace cover from CZ.Pkg04 and separating functions/sections from CZ.Pkg05"
    obligation := "convert each exceptional subspace alternative into containment in a proper algebraic curve and take the resulting finite union"
    downstreamOutput := "degeneracyCurveProper and pointInDegeneracyCurve for all selected S-integral points"
    leafBudget := "unchecked; split into <=100-step curve-containment leaves"
    status := "open formalization debt"
    debt := MachineProofDebt.formalizationDebt
    machineState := MachineState.notRepoLocalClosed
  },
  {
    package := SubspaceMethodPackage.repoLocalIntegrationGate
    surface := WorkSurface.integrationGate
    label := "CZ.Pkg07.RepoLocalIntegrationGate"
    upstreamInput := "any future local proof body or external Lean 4 proof candidate"
    obligation := "pin/import/check or vendor the terminal proof before any completed state; otherwise record a concrete blocker"
    downstreamOutput := "local_proof_body, local_wrapper_upstream_mathlib, external_upstream_pinned, or explicitly open formalization debt"
    leafBudget := "<=100 per imported/local theorem-tree leaf after integration"
    status := "open gate; no completed state claimed"
    debt := MachineProofDebt.formalizationDebt
    machineState := MachineState.notRepoLocalClosed
  }
]

/-- Machine-proof debt classification for this Stage1 slot. -/
def currentMachineProofDebt : MachineProofDebt :=
  MachineProofDebt.formalizationDebt

/-- Current machine state for the root theorem slot. -/
def currentMachineState : MachineState :=
  MachineState.notRepoLocalClosed

/--
Gate used by the public statement-shape note: the canonical theorem target is
resolved, while the terminal theorem proof remains outside repo-local closure.
-/
def publicStatementShapeNoteGate : Prop :=
  canonicalTarget =
      CandidateTarget.corvajaZannier2004SurfaceDegeneracy ∧
    currentMachineState = MachineState.notRepoLocalClosed

/-- Checked gate for adding the public statement-shape note without a completion claim. -/
theorem publicStatementShapeNoteGate_checked :
    publicStatementShapeNoteGate :=
  ⟨rfl, rfl⟩

/--
Integration-ready statement-shape note for the serial public-doc backfill.

This is checked as local metadata only.  It should be copied into the public
Stage1 surface by a serial integrator, not treated as a theorem proof.
-/
def publicStatementShapeNote : String :=
  "Statement shape: THM-M-0406 is the Corvaja--Zannier 2004 integral-points-on-surfaces degeneracy theorem. Over a number field with a finite set S of places, for a smooth projective surface with an open complement determined by boundary divisors satisfying the selected intersection/divisor-at-infinity hypotheses, the S-integral points on the open surface are contained in a proper algebraic curve. The repo-local Lean artifact records this as StatementShape via ArithmeticBase, SurfaceBoundaryData, HasCorvajaZannierHypotheses, DegeneracyPredicateMatchesCurve, and IntegralPointsDegenerate. This is a checked statement boundary and public-note target only, not a local proof of the Corvaja--Zannier theorem."

/-- Named declarations that should appear in the public statement-shape note. -/
def publicStatementShapeDeclarations : List String := [
  "canonicalTarget",
  "StatementShape",
  "ArithmeticBase",
  "SurfaceBoundaryData",
  "HasCorvajaZannierHypotheses",
  "DegeneracyPredicateMatchesCurve",
  "IntegralPointsDegenerate",
  "publicStatementShapeNoteGate"
]

/-- Closed states that count as repo-local theorem completion. -/
def countsAsRepoLocalCompleted : MachineState -> Prop
  | MachineState.localProofBody => True
  | MachineState.localWrapperUpstreamMathlib => True
  | MachineState.externalUpstreamPinned => True
  | MachineState.externalUpstreamAnchorOnly => False
  | MachineState.notRepoLocalClosed => False

/-- Checked gate: the current root-theorem machine state is not completed. -/
theorem currentMachineState_not_completed :
    ¬ countsAsRepoLocalCompleted currentMachineState := by
  intro h
  exact h

/-- Checked gate: external anchor-only evidence never counts as completion. -/
theorem externalAnchorOnly_not_completed :
    ¬ countsAsRepoLocalCompleted MachineState.externalUpstreamAnchorOnly := by
  intro h
  exact h

/-- Current package split is a seven-package open formalization plan. -/
theorem subspaceMethodPackageSplit_length :
    subspaceMethodPackageSplit.length = 7 :=
  rfl

/-- Repo-local integration-debt gate statement retained for public backfill. -/
def repoLocalIntegrationDebtGate : String :=
  "no completed state; any future external proof must be pinned/imported/checked or blocked explicitly"

/-- Substrate anchor families probed for `S1-M-019-PUB-03`. -/
inductive SubstrateAnchor where
  | heightBasic
  | heightNorthcott
  | siegelsLemma
  | diophantineApproximationBasic
  | numberFieldProductFormula
  | algebraicGeometryMorphismsBasic
  | algebraicGeometryMorphismsFiniteType
  | algebraicGeometryMorphismsProper
  | algebraicGeometryMorphismsSmooth
  | algebraicGeometryMorphismsOpenImmersion
  | algebraicGeometryMorphismsClosedImmersion
  deriving DecidableEq, Repr

/-- A checked substrate-probe row for the Corvaja--Zannier formalization route. -/
structure SubstrateAnchorProbeRow where
  anchor : SubstrateAnchor
  moduleName : String
  representativeDeclaration : String
  formalizationRole : String
  status : String
  debt : MachineProofDebt
  machineState : MachineState

/--
Repo-local substrate probe for `S1-M-019-PUB-03`.

The listed modules are imported at the top of this file and representative
declarations are retained in `#check` probes below.  These anchors are
infrastructure evidence only; they do not supply the missing
Corvaja--Zannier/Subspace-Theorem terminal proof.
-/
def substrateAnchorProbeRows : List SubstrateAnchorProbeRow := [
  {
    anchor := SubstrateAnchor.heightBasic
    moduleName := "Mathlib.NumberTheory.Height.Basic"
    representativeDeclaration := "Height.AdmissibleAbsValues"
    formalizationRole := "number-field height substrate already used by ArithmeticBase"
    status := "imported and checked locally"
    debt := MachineProofDebt.formalizationDebt
    machineState := MachineState.notRepoLocalClosed
  },
  {
    anchor := SubstrateAnchor.heightNorthcott
    moduleName := "Mathlib.NumberTheory.Height.Northcott"
    representativeDeclaration := "Northcott"
    formalizationRole := "height-finiteness/compactness-style substrate for later bounded-height branches"
    status := "imported and checked locally"
    debt := MachineProofDebt.formalizationDebt
    machineState := MachineState.notRepoLocalClosed
  },
  {
    anchor := SubstrateAnchor.siegelsLemma
    moduleName := "Mathlib.NumberTheory.SiegelsLemma"
    representativeDeclaration := "Int.Matrix.exists_ne_zero_int_vec_norm_le"
    formalizationRole := "auxiliary small-solution technology related to subspace-method inputs"
    status := "imported and checked locally"
    debt := MachineProofDebt.formalizationDebt
    machineState := MachineState.notRepoLocalClosed
  },
  {
    anchor := SubstrateAnchor.diophantineApproximationBasic
    moduleName := "Mathlib.NumberTheory.DiophantineApproximation.Basic"
    representativeDeclaration := "Real.exists_rat_abs_sub_le_and_den_le"
    formalizationRole := "basic Diophantine-approximation substrate; not a Subspace Theorem"
    status := "imported and checked locally"
    debt := MachineProofDebt.formalizationDebt
    machineState := MachineState.notRepoLocalClosed
  },
  {
    anchor := SubstrateAnchor.numberFieldProductFormula
    moduleName := "Mathlib.NumberTheory.NumberField.ProductFormula"
    representativeDeclaration := "NumberField.prod_abs_eq_one"
    formalizationRole := "global height/product-formula arithmetic substrate over number fields"
    status := "imported and checked locally"
    debt := MachineProofDebt.formalizationDebt
    machineState := MachineState.notRepoLocalClosed
  },
  {
    anchor := SubstrateAnchor.algebraicGeometryMorphismsBasic
    moduleName := "Mathlib.AlgebraicGeometry.Morphisms.Basic"
    representativeDeclaration := "AlgebraicGeometry.IsZariskiLocalAtTarget"
    formalizationRole := "scheme-morphism property framework for local geometric hypotheses"
    status := "imported and checked locally"
    debt := MachineProofDebt.formalizationDebt
    machineState := MachineState.notRepoLocalClosed
  },
  {
    anchor := SubstrateAnchor.algebraicGeometryMorphismsFiniteType
    moduleName := "Mathlib.AlgebraicGeometry.Morphisms.FiniteType"
    representativeDeclaration := "AlgebraicGeometry.LocallyOfFiniteType"
    formalizationRole := "finite-type hypothesis substrate for varieties/surfaces"
    status := "imported and checked locally"
    debt := MachineProofDebt.formalizationDebt
    machineState := MachineState.notRepoLocalClosed
  },
  {
    anchor := SubstrateAnchor.algebraicGeometryMorphismsProper
    moduleName := "Mathlib.AlgebraicGeometry.Morphisms.Proper"
    representativeDeclaration := "AlgebraicGeometry.IsProper"
    formalizationRole := "proper/projective compactification substrate"
    status := "imported and checked locally"
    debt := MachineProofDebt.formalizationDebt
    machineState := MachineState.notRepoLocalClosed
  },
  {
    anchor := SubstrateAnchor.algebraicGeometryMorphismsSmooth
    moduleName := "Mathlib.AlgebraicGeometry.Morphisms.Smooth"
    representativeDeclaration := "AlgebraicGeometry.Smooth"
    formalizationRole := "smoothness substrate for the projective surface hypothesis"
    status := "imported and checked locally"
    debt := MachineProofDebt.formalizationDebt
    machineState := MachineState.notRepoLocalClosed
  },
  {
    anchor := SubstrateAnchor.algebraicGeometryMorphismsOpenImmersion
    moduleName := "Mathlib.AlgebraicGeometry.Morphisms.OpenImmersion"
    representativeDeclaration := "AlgebraicGeometry.IsOpenImmersion"
    formalizationRole := "open-complement/subscheme inclusion substrate"
    status := "imported and checked locally"
    debt := MachineProofDebt.formalizationDebt
    machineState := MachineState.notRepoLocalClosed
  },
  {
    anchor := SubstrateAnchor.algebraicGeometryMorphismsClosedImmersion
    moduleName := "Mathlib.AlgebraicGeometry.Morphisms.ClosedImmersion"
    representativeDeclaration := "AlgebraicGeometry.IsClosedImmersion"
    formalizationRole := "closed-subscheme/divisor-support substrate"
    status := "imported and checked locally"
    debt := MachineProofDebt.formalizationDebt
    machineState := MachineState.notRepoLocalClosed
  }
]

/-- The `S1-M-019-PUB-03` substrate probe currently records eleven checked anchors. -/
theorem substrateAnchorProbeRows_length :
    substrateAnchorProbeRows.length = 11 :=
  rfl

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.AlgebraicGeometry.Scheme",
  "Mathlib.AlgebraicGeometry.Morphisms.Basic",
  "Mathlib.AlgebraicGeometry.Morphisms.ClosedImmersion",
  "Mathlib.AlgebraicGeometry.Morphisms.FiniteType",
  "Mathlib.AlgebraicGeometry.Morphisms.OpenImmersion",
  "Mathlib.AlgebraicGeometry.Morphisms.Proper",
  "Mathlib.AlgebraicGeometry.Morphisms.Smooth",
  "Mathlib.NumberTheory.DiophantineApproximation.Basic",
  "Mathlib.NumberTheory.Height.Basic",
  "Mathlib.NumberTheory.Height.Northcott",
  "Mathlib.NumberTheory.Height.NumberField",
  "Mathlib.NumberTheory.NumberField.Basic",
  "Mathlib.NumberTheory.NumberField.Completion.FinitePlace",
  "Mathlib.NumberTheory.NumberField.ProductFormula",
  "Mathlib.NumberTheory.SiegelsLemma",
  "Mathlib.RingTheory.DedekindDomain.Ideal.Basic",
  "Mathlib.RingTheory.Ideal.Norm.AbsNorm"
]

/-- Terminal theorem-name searches requested by `S1-M-019-PUB-04`. -/
inductive TerminalMathlibSearchTerm where
  | subspaceTheorem
  | schmidt
  | evertseFerretti
  | corvajaZannier
  | integralPoint
  | sIntegral
  | zariskiDense
  deriving DecidableEq, Repr

/-- A declaration-level search row for terminal mathlib anchors. -/
structure TerminalMathlibSearchRow where
  term : TerminalMathlibSearchTerm
  requestedName : String
  declarationLevelQuery : String
  exactNameHitCount : Nat
  broaderNameHitSummary : String
  terminalAnchorVerdict : String
  debt : MachineProofDebt
  machineState : MachineState

/--
Declaration-level `import Mathlib` search for `S1-M-019-PUB-04`.

The search enumerated environment declaration names, not source text.  The
`Schmidt` hits are Gram-Schmidt linear-algebra declarations and do not provide
the arithmetic Schmidt Subspace Theorem.  The lowercase broad probes for
`IntegralPoint` and `ZariskiDense` likewise found only unrelated declarations.
-/
def terminalMathlibSearchRows : List TerminalMathlibSearchRow := [
  {
    term := TerminalMathlibSearchTerm.subspaceTheorem
    requestedName := "SubspaceTheorem"
    declarationLevelQuery := "case-sensitive declaration-name contains `SubspaceTheorem`; broad lowercase query required both `subspace` and `theorem`"
    exactNameHitCount := 0
    broaderNameHitSummary := "0 broad declaration-name hits"
    terminalAnchorVerdict := "no mathlib terminal theorem anchor found"
    debt := MachineProofDebt.formalizationDebt
    machineState := MachineState.notRepoLocalClosed
  },
  {
    term := TerminalMathlibSearchTerm.schmidt
    requestedName := "Schmidt"
    declarationLevelQuery := "case-sensitive declaration-name contains `Schmidt`; broad lowercase query used `schmidt`"
    exactNameHitCount := 70
    broaderNameHitSummary := "70 hits, all in Gram-Schmidt inner-product/orthonormal-basis declarations"
    terminalAnchorVerdict := "no arithmetic Schmidt/Subspace-Theorem terminal anchor found"
    debt := MachineProofDebt.formalizationDebt
    machineState := MachineState.notRepoLocalClosed
  },
  {
    term := TerminalMathlibSearchTerm.evertseFerretti
    requestedName := "EvertseFerretti"
    declarationLevelQuery := "case-sensitive declaration-name contains `EvertseFerretti`; broad lowercase query required both `evertse` and `ferretti`"
    exactNameHitCount := 0
    broaderNameHitSummary := "0 broad declaration-name hits"
    terminalAnchorVerdict := "no mathlib terminal theorem anchor found"
    debt := MachineProofDebt.formalizationDebt
    machineState := MachineState.notRepoLocalClosed
  },
  {
    term := TerminalMathlibSearchTerm.corvajaZannier
    requestedName := "CorvajaZannier"
    declarationLevelQuery := "case-sensitive declaration-name contains `CorvajaZannier`; broad lowercase query required both `corvaja` and `zannier`"
    exactNameHitCount := 0
    broaderNameHitSummary := "0 broad declaration-name hits"
    terminalAnchorVerdict := "no mathlib terminal theorem anchor found"
    debt := MachineProofDebt.formalizationDebt
    machineState := MachineState.notRepoLocalClosed
  },
  {
    term := TerminalMathlibSearchTerm.integralPoint
    requestedName := "IntegralPoint"
    declarationLevelQuery := "case-sensitive declaration-name contains `IntegralPoint`; broad lowercase query required both `integral` and `point`"
    exactNameHitCount := 0
    broaderNameHitSummary := "1 broad hit: `FixedPoints.isIntegral`, unrelated to S-integral points on varieties"
    terminalAnchorVerdict := "no mathlib terminal theorem anchor found"
    debt := MachineProofDebt.formalizationDebt
    machineState := MachineState.notRepoLocalClosed
  },
  {
    term := TerminalMathlibSearchTerm.sIntegral
    requestedName := "SIntegral"
    declarationLevelQuery := "case-sensitive declaration-name contains `SIntegral`"
    exactNameHitCount := 0
    broaderNameHitSummary := "lowercase `sintegral` is too broad because it matches `IsIntegral`; no S-integral-point terminal anchor found"
    terminalAnchorVerdict := "no mathlib terminal theorem anchor found"
    debt := MachineProofDebt.formalizationDebt
    machineState := MachineState.notRepoLocalClosed
  },
  {
    term := TerminalMathlibSearchTerm.zariskiDense
    requestedName := "ZariskiDense"
    declarationLevelQuery := "case-sensitive declaration-name contains `ZariskiDense`; broad lowercase query required both `zariski` and `dense`"
    exactNameHitCount := 0
    broaderNameHitSummary := "2 broad hits in affine Zariski-site density infrastructure, not a Zariski-dense integral-points theorem"
    terminalAnchorVerdict := "no mathlib terminal theorem anchor found"
    debt := MachineProofDebt.formalizationDebt
    machineState := MachineState.notRepoLocalClosed
  }
]

/-- The `S1-M-019-PUB-04` terminal theorem-name audit records seven searches. -/
theorem terminalMathlibSearchRows_length :
    terminalMathlibSearchRows.length = 7 :=
  rfl

/--
Public-doc backfill text for the declaration-level terminal-name search.

This is audit metadata only.  It is not a local proof of the
Corvaja--Zannier theorem and it does not close the repo-local theorem gate.
-/
def terminalMathlibSearchPublicBackfill : String :=
  "PUB-04 declaration-level mathlib search: enumerating `import Mathlib` environment declaration names found no terminal theorem declarations named `SubspaceTheorem`, `EvertseFerretti`, `CorvajaZannier`, `IntegralPoint`, `SIntegral`, or `ZariskiDense`. The requested `Schmidt` spelling appears only in Gram-Schmidt inner-product/orthonormal-basis declarations, not in an arithmetic Schmidt Subspace Theorem. Broader lowercase probes found only unrelated `FixedPoints.isIntegral` and affine Zariski-site density infrastructure. Result: no mathlib terminal theorem anchor for the Corvaja--Zannier/Subspace-Theorem proof route; keep the slot in formalization_debt, not repo_local_integration_debt."

/-- Search terms retained for the external Lean 4 anchor audit. -/
def externalAnchorSearchTerms : List String := [
  "Corvaja Zannier On integral points on surfaces Lean 4",
  "Corvaja Zannier integral points surfaces Lean",
  "Corvaja Zannier subspace theorem integral points Lean",
  "Evertse Ferretti projective variety inequality Lean",
  "integral points on surfaces Lean mathlib",
  "S-integral points surface Lean",
  "Zariski dense integral points Lean"
]

/-!
## External Lean 4 proof audit for `S1-M-019-PUB-05`

This section records negative external-anchor evidence as checked metadata.
It does not claim an exhaustive public-web search and it does not prove the
Corvaja--Zannier theorem.  The key M0387 gate is that no external theorem body
was found that could be left as anchor-only completion evidence.
-/

/-- One row in the `S1-M-019-PUB-05` external Lean 4 proof audit. -/
structure ExternalLeanProofAuditRow where
  source : String
  repositoryURL : String
  commitOrSnapshot : String
  leanVersion : String
  license : String
  searchedSurface : String
  theoremNames : List String
  result : String
  integrationAction : String
  debt : MachineProofDebt
  machineState : MachineState
  deriving Repr

/--
External Lean 4 repositories/search surfaces checked for a terminal
Corvaja--Zannier/Evertse--Ferretti/Subspace-Theorem proof.

Rows with `theoremNames := []` found no relevant theorem declarations.  The
`AwesomeTheorems/Stage1` hits are intentionally excluded from this table
because they are repo-local statement-boundary metadata, not external proofs.
-/
def externalLeanProofAuditRows : List ExternalLeanProofAuditRow := [
  {
    source := "repo-local pinned mathlib4 dependency"
    repositoryURL := "https://github.com/leanprover-community/mathlib4.git"
    commitOrSnapshot := "8a178386ffc0f5fef0b77738bb5449d50efeea95"
    leanVersion := "leanprover/lean4:v4.29.0"
    license := "Apache-2.0"
    searchedSurface :=
      "rg over pinned Mathlib Lean sources for Corvaja, Zannier, Evertse, Ferretti, SubspaceTheorem, Subspace Theorem, SIntegral, IntegralPoint, ZariskiDense, and integral-points phrases"
    theoremNames := []
    result :=
      "no Corvaja--Zannier, Evertse--Ferretti, Schmidt Subspace Theorem, or S-integral-points degeneracy theorem found; only unrelated olympiad integral-point prose in Archive"
    integrationAction :=
      "no mathlib terminal theorem to wrap; keep root theorem not_repo_local_closed/formalization_debt"
    debt := MachineProofDebt.formalizationDebt
    machineState := MachineState.notRepoLocalClosed
  },
  {
    source := "repo-local pinned flt-regular dependency"
    repositoryURL := "https://github.com/leanprover-community/flt-regular.git"
    commitOrSnapshot := "56161b6eb5281fbfe9c38f2bcec0f429ebc11a27"
    leanVersion := "leanprover/lean4:v4.29.0"
    license := "Apache-2.0"
    searchedSurface :=
      "rg over all pinned flt-regular Lean sources for Corvaja, Zannier, Evertse, Ferretti, SubspaceTheorem, SIntegral, IntegralPoint, ZariskiDense, and integral-points phrases"
    theoremNames := []
    result :=
      "no relevant Corvaja--Zannier/Evertse--Ferretti/Subspace-Theorem proof or theorem declaration found"
    integrationAction := "no integration target"
    debt := MachineProofDebt.formalizationDebt
    machineState := MachineState.notRepoLocalClosed
  },
  {
    source := "GitHub CLI code search"
    repositoryURL := "https://github.com/search"
    commitOrSnapshot := "queried on 2026-05-01 from this worker environment"
    leanVersion := "not applicable"
    license := "not applicable"
    searchedSurface :=
      "gh search code queries for `Corvaja Zannier language:Lean`, `Evertse Ferretti language:Lean`, `SubspaceTheorem language:Lean`, and `SIntegral language:Lean`"
    theoremNames := []
    result :=
      "blocked because gh has no authenticated host in this environment; no repository-level proof candidate was identified through this route"
    integrationAction :=
      "remaining public-audit leaf: rerun authenticated GitHub code search before any future completion claim"
    debt := MachineProofDebt.formalizationDebt
    machineState := MachineState.notRepoLocalClosed
  },
  {
    source := "GitHub REST code search"
    repositoryURL := "https://api.github.com/search/code"
    commitOrSnapshot := "queried on 2026-05-01 from this worker environment"
    leanVersion := "not applicable"
    license := "not applicable"
    searchedSurface :=
      "REST code queries for quoted Corvaja/Zannier, Evertse/Ferretti, SubspaceTheorem, and SIntegral in Lean code"
    theoremNames := []
    result :=
      "blocked by unauthenticated GitHub API rate-limit exhaustion; no proof candidate was identified through this route"
    integrationAction :=
      "remaining public-audit leaf: rerun authenticated GitHub REST/code search and record URL, commit, theorem names, Lean version, and license if a proof is found"
    debt := MachineProofDebt.formalizationDebt
    machineState := MachineState.notRepoLocalClosed
  }
]

/-- The `S1-M-019-PUB-05` external Lean proof audit records four rows. -/
theorem externalLeanProofAuditRows_length :
    externalLeanProofAuditRows.length = 4 :=
  rfl

/-- `PUB-05` audit gate: no external Lean proof body was identified in this pass. -/
def pub05FoundExternalLeanProofBody : Bool := false

/-- Checked negative gate: no anchor-only external proof can be treated as completed. -/
theorem pub05FoundExternalLeanProofBody_eq_false :
    pub05FoundExternalLeanProofBody = false :=
  rfl

/-!
## Integration decision for `S1-M-019-PUB-06`

Because the external-proof audit did not identify a Lean 4 proof body, this
worker has no dependency or vendored proof to add within the owned artifact.
The checked decision is therefore to keep the theorem in formalization debt
and not to claim a completed repo-local integration state.
-/

/-- Actions allowed by the `PUB-06` external-proof integration gate. -/
inductive Pub06IntegrationAction where
  | pinExternalDependency
  | vendorProofBody
  | keepFormalizationDebt
  | recordConcreteIntegrationBlocker
  deriving DecidableEq, Repr

/-- Checked metadata row for the `PUB-06` integration decision. -/
structure Pub06IntegrationDecision where
  foundExternalProofBody : Bool
  action : Pub06IntegrationAction
  currentDebt : MachineProofDebt
  currentState : MachineState
  noLakeDependencyEdit : Bool
  noVendoredProofBody : Bool
  rationale : String
  deriving Repr

/--
`PUB-06` decision for this worker pass.

No external Lean 4 proof body was found by `PUB-05`, so there is no concrete
dependency to pin and no proof body to vendor.  The theorem remains
`formalization_debt` / `not_repo_local_closed`; this is not a completed state.
-/
def pub06IntegrationDecision : Pub06IntegrationDecision := {
  foundExternalProofBody := pub05FoundExternalLeanProofBody
  action := Pub06IntegrationAction.keepFormalizationDebt
  currentDebt := MachineProofDebt.formalizationDebt
  currentState := MachineState.notRepoLocalClosed
  noLakeDependencyEdit := true
  noVendoredProofBody := true
  rationale :=
    "PUB-05 found no external Lean 4 proof body to pin or vendor; keep THM-M-0406 in formalization_debt until a local proof body, mathlib wrapper, or pinned external dependency validates."
}

/-- Checked `PUB-06` gate: no external proof was found, so no integration claim is made. -/
theorem pub06IntegrationDecision_checked :
    pub06IntegrationDecision.foundExternalProofBody = false ∧
      pub06IntegrationDecision.action =
        Pub06IntegrationAction.keepFormalizationDebt ∧
      pub06IntegrationDecision.currentDebt =
        MachineProofDebt.formalizationDebt ∧
      pub06IntegrationDecision.currentState =
        MachineState.notRepoLocalClosed ∧
      pub06IntegrationDecision.noLakeDependencyEdit = true ∧
      pub06IntegrationDecision.noVendoredProofBody = true :=
  ⟨rfl, rfl, rfl, rfl, rfl, rfl⟩

/-- Checked `PUB-06` gate: the current integration decision is not completion. -/
theorem pub06IntegrationDecision_not_completed :
    ¬ countsAsRepoLocalCompleted pub06IntegrationDecision.currentState := by
  intro h
  exact h

/--
Public-doc backfill text for `S1-M-019-PUB-06`.

This text is for a later serial integrator; this worker did not edit public
planning documents or shared Lake/import aggregators.
-/
def pub06IntegrationPublicBackfill : String :=
  "PUB-06 integration gate: no external Lean 4 proof body was found by the current PUB-05 audit, so this worker did not add a Lake dependency, edit shared import aggregators, or vendor a proof body. The checked local decision `pub06IntegrationDecision` records `foundExternalProofBody = false`, `action = keepFormalizationDebt`, `currentDebt = formalizationDebt`, and `currentState = notRepoLocalClosed`; `pub06IntegrationDecision_not_completed` verifies that this is not a repo-local completion state. Keep THM-M-0406 in `formalization_debt` until a local proof body, a pinned mathlib wrapper, or an external dependency/vendored proof body validates with the repo-local Lean command. If an external proof is later found, pin/import/check it or record a concrete dependency/toolchain/license blocker; do not count anchor-only evidence as completed."

/--
Public-doc backfill text for the external Lean 4 proof audit.

This text is intended for a serial public-doc integrator.  It is deliberately a
negative audit note, not a proof-completion statement.
-/
def externalLeanProofAuditPublicBackfill : String :=
  "PUB-05 external Lean 4 proof audit: checked the repo-local pinned mathlib4 dependency (`https://github.com/leanprover-community/mathlib4.git`, commit `8a178386ffc0f5fef0b77738bb5449d50efeea95`, Lean `leanprover/lean4:v4.29.0`, Apache-2.0) and pinned `flt-regular` dependency (`https://github.com/leanprover-community/flt-regular.git`, commit `56161b6eb5281fbfe9c38f2bcec0f429ebc11a27`, Lean `leanprover/lean4:v4.29.0`, Apache-2.0) for Corvaja, Zannier, Evertse, Ferretti, SubspaceTheorem/Subspace Theorem, SIntegral, IntegralPoint, ZariskiDense, and integral-points phrases. No terminal Corvaja--Zannier/Evertse--Ferretti/Subspace-Theorem Lean proof or theorem declaration was found. GitHub CLI and REST code-search reruns were blocked by missing authentication/rate-limit exhaustion in this worker environment; an authenticated rerun remains an open audit leaf before any future completion claim. Result: no external proof is currently available to pin/import/check, so the root theorem remains formalization_debt/not_repo_local_closed with no repo_local_integration_debt completion state."

/-!
## Public backfill gate for `S1-M-019-PUB-07`

The public theorem tree must be merged by a serial integrator only after the
machine anchor and process-audit surfaces are stable.  This worker records an
integration-ready proposal in checked local metadata, but it does not edit the
shared public blueprint/todo surfaces and it does not claim theorem completion.
-/

/-- Readiness states for the `PUB-07` public theorem-tree backfill. -/
inductive PublicBackfillReadiness where
  | blockedUntilMachineAuditUpdated
  | integrationReadyNotMerged
  | publiclyMerged
  deriving DecidableEq, Repr

/-- Checked metadata for the `PUB-07` public backfill gate. -/
structure Pub07PublicBackfillGate where
  machineAnchorAuditUpdated : Bool
  processAuditUpdated : Bool
  externalProofAuditUpdated : Bool
  publicDocsEditedByWorker : Bool
  publicCompletionClaim : Bool
  serialIntegratorRequired : Bool
  readiness : PublicBackfillReadiness
  rootDebt : MachineProofDebt
  rootMachineState : MachineState
  rationale : String
  deriving Repr

/--
`PUB-07` gate for this worker pass.

The local machine/process audit metadata is present in this Lean file, so a
serial integrator can backfill the public theorem tree from the strings and
package rows recorded here.  The public docs have not been edited by this
worker and the theorem remains open formalization debt.
-/
def pub07PublicBackfillGate : Pub07PublicBackfillGate := {
  machineAnchorAuditUpdated := true
  processAuditUpdated := true
  externalProofAuditUpdated := true
  publicDocsEditedByWorker := false
  publicCompletionClaim := false
  serialIntegratorRequired := true
  readiness := PublicBackfillReadiness.integrationReadyNotMerged
  rootDebt := MachineProofDebt.formalizationDebt
  rootMachineState := MachineState.notRepoLocalClosed
  rationale :=
    "PUB-07 may be serially backfilled into public docs as an open theorem-tree/audit entry only; this worker made no shared public-doc edits and no completion claim."
}

/-- Checked `PUB-07` gate: public backfill is prepared but not merged or completed. -/
theorem pub07PublicBackfillGate_checked :
    pub07PublicBackfillGate.machineAnchorAuditUpdated = true ∧
      pub07PublicBackfillGate.processAuditUpdated = true ∧
      pub07PublicBackfillGate.externalProofAuditUpdated = true ∧
      pub07PublicBackfillGate.publicDocsEditedByWorker = false ∧
      pub07PublicBackfillGate.publicCompletionClaim = false ∧
      pub07PublicBackfillGate.serialIntegratorRequired = true ∧
      pub07PublicBackfillGate.readiness =
        PublicBackfillReadiness.integrationReadyNotMerged ∧
      pub07PublicBackfillGate.rootDebt =
        MachineProofDebt.formalizationDebt ∧
      pub07PublicBackfillGate.rootMachineState =
        MachineState.notRepoLocalClosed :=
  ⟨rfl, rfl, rfl, rfl, rfl, rfl, rfl, rfl, rfl⟩

/-- Checked `PUB-07` gate: the proposed public backfill is not completion. -/
theorem pub07PublicBackfillGate_not_completed :
    ¬ countsAsRepoLocalCompleted pub07PublicBackfillGate.rootMachineState := by
  intro h
  exact h

/--
Public-doc theorem-tree backfill text for `S1-M-019-PUB-07`.

This text is integration-ready for a serial public-doc editor.  It must not be
treated as a private-ledger completion surface.
-/
def pub07PublicBackfillProposal : String :=
  "PUB-07 public theorem-tree backfill proposal: after merging the machine anchor/process audit, add an open theorem-tree note for THM-M-0406 with canonical target `Corvaja--Zannier 2004 integral-points-on-surfaces degeneracy theorem`; statement boundary `StatementShape`; package leaves `CZ.Pkg01.StatementAndBoundaryNormalization`, `CZ.Pkg02.DivisorIntersectionGeometry`, `CZ.Pkg03.HeightAndSIntegralPointSetup`, `CZ.Pkg04.SubspaceTheoremInput`, `CZ.Pkg05.AuxiliarySectionOrFunctionConstruction`, `CZ.Pkg06.ExceptionalSubspaceToCurveDescent`, and `CZ.Pkg07.RepoLocalIntegrationGate`; local validation command `cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_019.lean`; status `open formalization_debt/not_repo_local_closed`; and gate text `no public completion claim until a local proof body, a pinned mathlib wrapper, or a pinned/vendored external proof validates and every <=100 leaf ledger is independently closed`. Do not mark this public backfill completed from this private ledger alone."

/-! ## Audit probes retained in the checked file. -/

#check CandidateTarget
#check canonicalTarget
#check canonicalTarget_eq_corvajaZannier2004
#check ArithmeticBase
#check SurfaceBoundaryData
#check StatementShape
#check HasCorvajaZannierHypotheses
#check IntegralPointsDegenerate
#check integralPointsDegenerate_of_statementShape
#check subspaceMethodPackageSplit
#check currentMachineProofDebt
#check currentMachineState_not_completed
#check externalAnchorOnly_not_completed
#check publicStatementShapeNoteGate_checked
#check publicStatementShapeNote
#check publicStatementShapeDeclarations
#check subspaceMethodPackageSplit_length
#check repoLocalIntegrationDebtGate
#check SubstrateAnchor
#check substrateAnchorProbeRows
#check substrateAnchorProbeRows_length
#check TerminalMathlibSearchTerm
#check terminalMathlibSearchRows
#check terminalMathlibSearchRows_length
#check terminalMathlibSearchPublicBackfill
#check ExternalLeanProofAuditRow
#check externalLeanProofAuditRows
#check externalLeanProofAuditRows_length
#check pub05FoundExternalLeanProofBody
#check pub05FoundExternalLeanProofBody_eq_false
#check Pub06IntegrationAction
#check Pub06IntegrationDecision
#check pub06IntegrationDecision
#check pub06IntegrationDecision_checked
#check pub06IntegrationDecision_not_completed
#check pub06IntegrationPublicBackfill
#check externalLeanProofAuditPublicBackfill
#check PublicBackfillReadiness
#check Pub07PublicBackfillGate
#check pub07PublicBackfillGate
#check pub07PublicBackfillGate_checked
#check pub07PublicBackfillGate_not_completed
#check pub07PublicBackfillProposal
#check Height.AdmissibleAbsValues
#check Northcott
#check Int.Matrix.exists_ne_zero_int_vec_norm_le
#check Real.exists_rat_abs_sub_le_and_den_le
#check NumberField.prod_abs_eq_one
#check AlgebraicGeometry.IsZariskiLocalAtTarget
#check AlgebraicGeometry.LocallyOfFiniteType
#check AlgebraicGeometry.IsProper
#check AlgebraicGeometry.Smooth
#check AlgebraicGeometry.IsOpenImmersion
#check AlgebraicGeometry.IsClosedImmersion

end S1_M_019
end Stage1
end AwesomeTheorems
