import Mathlib.AlgebraicGeometry.Scheme
import Mathlib.AlgebraicGeometry.IdealSheaf.Functorial
import Mathlib.AlgebraicGeometry.Morphisms.ClosedImmersion
import Mathlib.AlgebraicGeometry.ProjectiveSpectrum.Basic
import Mathlib.AlgebraicGeometry.ProjectiveSpectrum.Scheme
import Mathlib.AlgebraicGeometry.Pullbacks
import Mathlib.RingTheory.FiniteLength
import Mathlib.RingTheory.GradedAlgebra.Homogeneous.Ideal
import Mathlib.RingTheory.MvPolynomial.Homogeneous
import Mathlib.RingTheory.Polynomial.HilbertPoly

/-!
# S1-M-029 / THM-M-0104: Bezout theorem, Stage1 statement shape

This file records a conservative Lean 4 boundary artifact for the projective
plane length form of Bezout's theorem.  The current local mathlib checkout
supplies schemes, Proj infrastructure, multivariable polynomials, homogeneous
polynomials, and total degree.  This artifact does not claim the terminal
intersection-theoretic theorem; it names the missing curve/intersection
payload as explicit proposition fields and keeps the machine-checked layer to
statement shape plus small imported-API wrappers.
-/

noncomputable section

open AlgebraicGeometry
open CategoryTheory
open CategoryTheory.Limits

universe u v

namespace AwesomeTheorems.Stage1.S1_M_029

/-- Public statement-normalization choice for the Stage1 Bezout slot. -/
inductive BezoutStatementVariant where
  | projectivePlaneLengthTheorem
  | geometricPointBound
  | affineSpecialCase

/--
The canonical Stage1 target is the projective plane length theorem: two
homogeneous plane curves over an algebraically closed field, with no common
component, have intersection scheme length `degreeF * degreeG`.
-/
def selectedStatementVariant : BezoutStatementVariant :=
  .projectivePlaneLengthTheorem

/--
The geometric point bound and affine special case are downstream bridge
targets, not the canonical terminal statement for this slot.
-/
def nonCanonicalStatementVariants : List BezoutStatementVariant :=
  [.geometricPointBound, .affineSpecialCase]

/-- Homogeneous ternary polynomials, the usual equation model for plane projective curves. -/
def HomogeneousPlanePolynomial (K : Type u) [CommSemiring K] (d : Nat) : Type u :=
  {F : MvPolynomial (Fin 3) K // F.IsHomogeneous d}

/--
Stage1 data for the standard projective-plane intersection-length form of
Bezout's theorem.

The fields `noCommonComponent`, `intersectionSupportIsProjective`,
`localIntersectionMultiplicity`, and `multiplicitySumMatchesLocalData` are the
deliberate theorem-internal boundary: later work must replace them with the
chosen mathlib or repo-local projective curve, local ring, and intersection
multiplicity APIs before any terminal proof claim.
-/
structure PlaneCurveIntersectionData where
  K : Type u
  [field : Field K]
  degreeF : Nat
  degreeG : Nat
  F : MvPolynomial (Fin 3) K
  G : MvPolynomial (Fin 3) K
  F_homogeneous : F.IsHomogeneous degreeF
  G_homogeneous : G.IsHomogeneous degreeG
  F_nonzero : F ≠ 0
  G_nonzero : G ≠ 0
  algebraicallyClosedBase : Prop
  projectivePlaneModel : Type u
  curveF : Type u
  curveG : Type u
  noCommonComponent : Prop
  finiteIntersectionSupport : Prop
  intersectionSupportIsProjective : Prop
  localIntersectionMultiplicity : projectivePlaneModel → Nat
  totalIntersectionMultiplicity : Nat
  multiplicitySumMatchesLocalData : Prop

attribute [instance] PlaneCurveIntersectionData.field

/-- The hypotheses normally imposed before applying the plane-curve Bezout bound. -/
def BezoutHypotheses (D : PlaneCurveIntersectionData.{u}) : Prop :=
  D.algebraicallyClosedBase ∧
    D.noCommonComponent ∧
    D.finiteIntersectionSupport ∧
    D.intersectionSupportIsProjective ∧
    D.multiplicitySumMatchesLocalData

/--
The normalized projective-plane length conclusion: the total local intersection
multiplicity of two projective plane curves is exactly the product of their
degrees.
-/
def BezoutConclusion (D : PlaneCurveIntersectionData.{u}) : Prop :=
  D.totalIntersectionMultiplicity = D.degreeF * D.degreeG

/--
Downstream geometric-count bridge target: the multiplicity-counted length
conclusion implies the weaker numeric bound.  A later file should replace
`totalIntersectionMultiplicity` with an actual finite support cardinality
before claiming the geometric point-count theorem.
-/
def BezoutMultiplicityBoundConclusion (D : PlaneCurveIntersectionData.{u}) : Prop :=
  D.totalIntersectionMultiplicity ≤ D.degreeF * D.degreeG

/--
Repo-local normalized statement shape for THM-M-0104.

This is a `Prop` target for later formalization, not a proof of Bezout's
theorem in this repository.
-/
def StatementShape : Prop :=
  ∀ D : PlaneCurveIntersectionData.{u}, BezoutHypotheses D → BezoutConclusion D

/-- The selected length theorem immediately gives the weaker multiplicity-counted bound. -/
theorem lengthConclusion_implies_multiplicityBound
    {D : PlaneCurveIntersectionData.{u}} (h : BezoutConclusion D) :
    BezoutMultiplicityBoundConclusion D := by
  exact le_of_eq h

/--
Bridge target for the first special case: one of the two projective plane
curves is a line, so the product-of-degrees conclusion specializes to the
degree of the other curve.
-/
def LineCurveBridgeConclusion (D : PlaneCurveIntersectionData.{u}) : Prop :=
  (D.degreeF = 1 → D.totalIntersectionMultiplicity = D.degreeG) ∧
    (D.degreeG = 1 → D.totalIntersectionMultiplicity = D.degreeF)

/--
Statement shape for the line-vs-curve bridge.  This is still downstream of the
full projective-plane length conclusion; it records the first special-case
target without claiming that the intersection-theory hypotheses are already
implemented in this repository.
-/
def LineCurveBridgeStatementShape : Prop :=
  ∀ D : PlaneCurveIntersectionData.{u},
    BezoutHypotheses D → LineCurveBridgeConclusion D

/-- Oriented bridge data where the first projective plane curve is the line. -/
def LineLeftCurveBridgeData : Type (u + 1) :=
  {D : PlaneCurveIntersectionData.{u} // D.degreeF = 1}

/-- Oriented bridge data where the second projective plane curve is the line. -/
def LineRightCurveBridgeData : Type (u + 1) :=
  {D : PlaneCurveIntersectionData.{u} // D.degreeG = 1}

/-- Hypotheses for the oriented bridge with the line as the first curve. -/
def LineLeftCurveBridgeHypotheses (D : LineLeftCurveBridgeData.{u}) : Prop :=
  BezoutHypotheses D.1

/-- Hypotheses for the oriented bridge with the line as the second curve. -/
def LineRightCurveBridgeHypotheses (D : LineRightCurveBridgeData.{u}) : Prop :=
  BezoutHypotheses D.1

/-- The oriented line-left special-case conclusion. -/
def LineLeftCurveBridgeConclusion (D : LineLeftCurveBridgeData.{u}) : Prop :=
  D.1.totalIntersectionMultiplicity = D.1.degreeG

/-- The oriented line-right special-case conclusion. -/
def LineRightCurveBridgeConclusion (D : LineRightCurveBridgeData.{u}) : Prop :=
  D.1.totalIntersectionMultiplicity = D.1.degreeF

/-- First-class statement shape for the case where the first curve is a line. -/
def LineLeftCurveBridgeStatementShape : Prop :=
  ∀ D : LineLeftCurveBridgeData.{u},
    LineLeftCurveBridgeHypotheses D → LineLeftCurveBridgeConclusion D

/-- First-class statement shape for the case where the second curve is a line. -/
def LineRightCurveBridgeStatementShape : Prop :=
  ∀ D : LineRightCurveBridgeData.{u},
    LineRightCurveBridgeHypotheses D → LineRightCurveBridgeConclusion D

/-- If the first curve has degree one, the Bezout length conclusion counts the other degree. -/
theorem lengthConclusion_lineLeft_equals_curveDegree
    {D : PlaneCurveIntersectionData.{u}} (hLine : D.degreeF = 1)
    (h : BezoutConclusion D) :
    D.totalIntersectionMultiplicity = D.degreeG := by
  calc
    D.totalIntersectionMultiplicity = D.degreeF * D.degreeG := h
    _ = 1 * D.degreeG := by rw [hLine]
    _ = D.degreeG := Nat.one_mul D.degreeG

/-- If the second curve has degree one, the Bezout length conclusion counts the other degree. -/
theorem lengthConclusion_lineRight_equals_curveDegree
    {D : PlaneCurveIntersectionData.{u}} (hLine : D.degreeG = 1)
    (h : BezoutConclusion D) :
    D.totalIntersectionMultiplicity = D.degreeF := by
  calc
    D.totalIntersectionMultiplicity = D.degreeF * D.degreeG := h
    _ = D.degreeF * 1 := by rw [hLine]
    _ = D.degreeF := Nat.mul_one D.degreeF

/-- The normalized length conclusion supplies the oriented line-left bridge target. -/
theorem lengthConclusion_implies_lineLeftCurveBridgeTarget
    {D : LineLeftCurveBridgeData.{u}} (h : BezoutConclusion D.1) :
    LineLeftCurveBridgeConclusion D :=
  lengthConclusion_lineLeft_equals_curveDegree D.2 h

/-- The normalized length conclusion supplies the oriented line-right bridge target. -/
theorem lengthConclusion_implies_lineRightCurveBridgeTarget
    {D : LineRightCurveBridgeData.{u}} (h : BezoutConclusion D.1) :
    LineRightCurveBridgeConclusion D :=
  lengthConclusion_lineRight_equals_curveDegree D.2 h

/-- The normalized length conclusion supplies the checked line-vs-curve bridge package. -/
theorem lengthConclusion_implies_lineCurveBridge
    {D : PlaneCurveIntersectionData.{u}} (h : BezoutConclusion D) :
    LineCurveBridgeConclusion D := by
  constructor
  · intro hLine
    exact lengthConclusion_lineLeft_equals_curveDegree hLine h
  · intro hLine
    exact lengthConclusion_lineRight_equals_curveDegree hLine h

/-- The full statement shape implies the line-vs-curve bridge statement shape. -/
theorem statementShape_implies_lineCurveBridgeStatement
    (hStatement : StatementShape.{u}) :
    LineCurveBridgeStatementShape.{u} := by
  intro D hHypotheses
  exact lengthConclusion_implies_lineCurveBridge (hStatement D hHypotheses)

/-- The full statement shape implies the oriented line-left bridge statement shape. -/
theorem statementShape_implies_lineLeftCurveBridgeStatement
    (hStatement : StatementShape.{u}) :
    LineLeftCurveBridgeStatementShape.{u} := by
  intro D hHypotheses
  exact lengthConclusion_implies_lineLeftCurveBridgeTarget (hStatement D.1 hHypotheses)

/-- The full statement shape implies the oriented line-right bridge statement shape. -/
theorem statementShape_implies_lineRightCurveBridgeStatement
    (hStatement : StatementShape.{u}) :
    LineRightCurveBridgeStatementShape.{u} := by
  intro D hHypotheses
  exact lengthConclusion_implies_lineRightCurveBridgeTarget (hStatement D.1 hHypotheses)

namespace MathlibAnchors

variable {K : Type u} [CommSemiring K]
variable {d e : Nat}

/-- One row in the Stage1 mathlib anchor audit table for the Bezout slot. -/
structure AnchorRow where
  topic : String
  moduleName : String
  primaryNames : List String
  repoLocalClosure : String

/--
Integration-ready mathlib anchor table for the requested Bezout dependencies.

These rows document checked local names only.  They do not assert that mathlib
already contains the projective-plane intersection-length theorem.
-/
def bezoutMathlibAnchorTable : List AnchorRow :=
  [ { topic := "Proj and projective spectrum"
      moduleName := "Mathlib.AlgebraicGeometry.ProjectiveSpectrum.Basic"
      primaryNames :=
        [ "AlgebraicGeometry.Proj",
          "ProjectiveSpectrum",
          "ProjectiveSpectrum.basicOpen",
          "AlgebraicGeometry.Proj.basicOpen",
          "AlgebraicGeometry.Proj.basicOpenIsoSpec" ]
      repoLocalClosure :=
        "checked anchors for Proj objects and affine basic-open charts; no Bezout theorem" },
    { topic := "Closed immersions"
      moduleName := "Mathlib.AlgebraicGeometry.Morphisms.ClosedImmersion"
      primaryNames :=
        [ "AlgebraicGeometry.IsClosedImmersion",
          "AlgebraicGeometry.IsClosedImmersion.isClosedEmbedding",
          "AlgebraicGeometry.IsClosedImmersion.iff_isPreimmersion",
          "AlgebraicGeometry.IsClosedImmersion.of_isPreimmersion" ]
      repoLocalClosure :=
        "checked anchors for closed-immersion predicates and topological closed embedding payload" },
    { topic := "Homogeneous ideals"
      moduleName := "Mathlib.RingTheory.GradedAlgebra.Homogeneous.Ideal"
      primaryNames :=
        [ "HomogeneousIdeal",
          "HomogeneousIdeal.toIdeal",
          "HomogeneousIdeal.irrelevant",
          "Ideal.homogeneousCore",
          "Ideal.homogeneousHull" ]
      repoLocalClosure :=
        "checked anchors for homogeneous ideals and the irrelevant ideal used by Proj" },
    { topic := "Finite length"
      moduleName := "Mathlib.RingTheory.FiniteLength"
      primaryNames :=
        [ "IsFiniteLength",
          "isFiniteLength_iff_isNoetherian_isArtinian",
          "isFiniteLength_iff_exists_compositionSeries",
          "CompositionSeries",
          "RelSeries.length" ]
      repoLocalClosure :=
        "checked anchors for finite-length modules via Noetherian-Artinian and composition-series APIs" },
    { topic := "Multivariate degree and homogeneous polynomial APIs"
      moduleName := "Mathlib.RingTheory.MvPolynomial.Homogeneous"
      primaryNames :=
        [ "MvPolynomial.IsHomogeneous",
          "MvPolynomial.homogeneousSubmodule",
          "MvPolynomial.mem_homogeneousSubmodule",
          "MvPolynomial.IsHomogeneous.totalDegree",
          "MvPolynomial.IsHomogeneous.mul",
          "MvPolynomial.homogeneousSubmodule_mul" ]
      repoLocalClosure :=
        "checked anchors for homogeneous ternary polynomial statements and total-degree arithmetic" },
    { topic := "Hilbert polynomial APIs"
      moduleName := "Mathlib.RingTheory.Polynomial.HilbertPoly"
      primaryNames :=
        [ "Polynomial.preHilbertPoly",
          "Polynomial.hilbertPoly",
          "Polynomial.natDegree_preHilbertPoly",
          "Polynomial.hilbertPoly_X_pow_succ",
          "Polynomial.coeff_mul_invOneSubPow_eq_hilbertPoly_eval",
          "Polynomial.existsUnique_hilbertPoly" ]
      repoLocalClosure :=
        "checked anchors for power-series Hilbert polynomial APIs; mathlib TODO still excludes finitely generated graded modules" } ]

/-- Mathlib anchor: a homogeneous plane polynomial is a stable Lean type. -/
def homogeneousPlanePolynomialAnchor (d : Nat) : Type u :=
  HomogeneousPlanePolynomial K d

/-- Mathlib anchor: homogeneous nonzero multivariable polynomials have the expected total degree. -/
theorem homogeneous_totalDegree
    {F : MvPolynomial (Fin 3) K} (hF : F.IsHomogeneous d) (hF0 : F ≠ 0) :
    F.totalDegree = d :=
  hF.totalDegree hF0

/-- Mathlib anchor: products of homogeneous multivariable polynomials remain homogeneous. -/
theorem homogeneous_mul
    {F G : MvPolynomial (Fin 3) K}
    (hF : F.IsHomogeneous d) (hG : G.IsHomogeneous e) :
    (F * G).IsHomogeneous (d + e) :=
  hF.mul hG

/-- Mathlib anchor: the scheme object model is available in the local dependency closure. -/
def schemeAnchor : Type (u + 1) :=
  Scheme.{u}

/-- Mathlib anchor: `Proj` is available as a scheme for `ℕ`-graded rings. -/
def projSchemeAnchor
    {A σ : Type u} [CommRing A] [SetLike σ A] [AddSubgroupClass σ A]
    (𝒜 : Nat → σ) [GradedRing 𝒜] : Scheme.{u} :=
  Proj 𝒜

/-- Mathlib anchor: projective spectrum points are available for graded rings. -/
def projectiveSpectrumAnchor
    {A σ : Type u} [CommRing A] [SetLike σ A] [AddSubmonoidClass σ A]
    (𝒜 : Nat → σ) [GradedRing 𝒜] : Type u :=
  ProjectiveSpectrum 𝒜

/-- Mathlib anchor: projective-spectrum basic opens are named in the pinned checkout. -/
def projectiveSpectrumBasicOpenAnchor
    {A σ : Type u} [CommRing A] [SetLike σ A] [AddSubmonoidClass σ A]
    (𝒜 : Nat → σ) [GradedRing 𝒜] (f : A) :
    TopologicalSpace.Opens (ProjectiveSpectrum 𝒜) :=
  ProjectiveSpectrum.basicOpen 𝒜 f

/-- Mathlib anchor: the scheme-level Proj basic-open chart API is named. -/
def projBasicOpenAnchor
    {A σ : Type u} [CommRing A] [SetLike σ A] [AddSubgroupClass σ A]
    (𝒜 : Nat → σ) [GradedRing 𝒜] (f : A) : (Proj 𝒜).Opens :=
  AlgebraicGeometry.Proj.basicOpen 𝒜 f

/-- Mathlib anchor: closed immersions are available as a scheme morphism property. -/
def closedImmersionAnchor {X Y : Scheme.{u}} (f : X ⟶ Y) : Prop :=
  IsClosedImmersion f

/-- Mathlib anchor: a closed immersion exposes a closed embedding on underlying spaces. -/
theorem closedImmersion_isClosedEmbedding
    {X Y : Scheme.{u}} {f : X ⟶ Y} [IsClosedImmersion f] :
    Topology.IsClosedEmbedding f :=
  IsClosedImmersion.isClosedEmbedding f

/-- Mathlib anchor: homogeneous ideals form a Lean type for graded rings. -/
def homogeneousIdealAnchor
    {A σ : Type u} [Semiring A] [SetLike σ A] [AddSubmonoidClass σ A]
    (𝒜 : Nat → σ) [GradedRing 𝒜] : Type u :=
  HomogeneousIdeal 𝒜

/-- Mathlib anchor: homogeneous ideals coerce back to ordinary ideals. -/
def homogeneousIdealToIdealAnchor
    {A σ : Type u} [Semiring A] [SetLike σ A] [AddSubmonoidClass σ A]
    {𝒜 : Nat → σ} [GradedRing 𝒜] (I : HomogeneousIdeal 𝒜) : Ideal A :=
  I.toIdeal

/-- Mathlib anchor: the irrelevant homogeneous ideal used in `Proj` is named. -/
def homogeneousIrrelevantIdealAnchor
    {A σ : Type u} [Semiring A] [SetLike σ A] [AddSubmonoidClass σ A]
    (𝒜 : Nat → σ) [GradedRing 𝒜] : HomogeneousIdeal 𝒜 :=
  HomogeneousIdeal.irrelevant 𝒜

/-- Mathlib anchor: finite length is the named module predicate in this checkout. -/
def finiteLengthModuleAnchor
    (R : Type u) [Ring R] (M : Type v) [AddCommGroup M] [Module R M] : Prop :=
  IsFiniteLength R M

/-- Mathlib anchor: finite length is equivalent to Noetherian plus Artinian for modules. -/
theorem finiteLength_iff_noetherian_artinian
    {R : Type u} [Ring R] {M : Type v} [AddCommGroup M] [Module R M] :
    IsFiniteLength R M ↔ IsNoetherian R M ∧ IsArtinian R M :=
  isFiniteLength_iff_isNoetherian_isArtinian

/-- Mathlib anchor: finite length is also characterized by composition series. -/
theorem finiteLength_iff_compositionSeries
    {R : Type u} [Ring R] {M : Type v} [AddCommGroup M] [Module R M] :
    IsFiniteLength R M ↔
      ∃ s : CompositionSeries (Submodule R M), s.head = ⊥ ∧ s.last = ⊤ :=
  isFiniteLength_iff_exists_compositionSeries

/-- Mathlib anchor: homogeneous polynomial submodules are exposed as submodules. -/
def homogeneousSubmoduleAnchor (d : Nat) : Submodule K (MvPolynomial (Fin 3) K) :=
  MvPolynomial.homogeneousSubmodule (Fin 3) K d

/-- Mathlib anchor: membership in a homogeneous submodule is the homogeneous predicate. -/
theorem mem_homogeneousSubmoduleAnchor
    {F : MvPolynomial (Fin 3) K} :
    F ∈ homogeneousSubmoduleAnchor (K := K) d ↔ F.IsHomogeneous d :=
  MvPolynomial.mem_homogeneousSubmodule d F

section HilbertPolynomialAnchors

variable (F : Type u) [Field F]

/-- Mathlib anchor: Hilbert polynomials are available for polynomial numerators. -/
noncomputable def hilbertPolynomialAnchor (p : Polynomial F) (d : Nat) : Polynomial F :=
  Polynomial.hilbertPoly p d

/-- Mathlib anchor: the basic pre-Hilbert polynomial family is named. -/
noncomputable def preHilbertPolynomialAnchor (d k : Nat) : Polynomial F :=
  Polynomial.preHilbertPoly F d k

/-- Mathlib anchor: Hilbert polynomials of monomials reduce to pre-Hilbert polynomials. -/
theorem hilbertPolynomialXPowSuccAnchor (d k : Nat) :
    Polynomial.hilbertPoly ((Polynomial.X : Polynomial F) ^ k) (d + 1) =
      Polynomial.preHilbertPoly F d k :=
  Polynomial.hilbertPoly_X_pow_succ d k

variable [CharZero F]

/-- Mathlib anchor: pre-Hilbert polynomials have the expected degree in characteristic zero. -/
theorem preHilbertPolynomialNatDegreeAnchor (d k : Nat) :
    (Polynomial.preHilbertPoly F d k).natDegree = d :=
  Polynomial.natDegree_preHilbertPoly F d k

/-- Mathlib anchor: `Polynomial.hilbertPoly` is uniquely determined by eventual coefficients. -/
theorem hilbertPolynomialExistsUniqueAnchor (p : Polynomial F) (d : Nat) :
    ∃! h : Polynomial F, ∃ N : Nat, ∀ n > N,
      PowerSeries.coeff (R := F) n (p * PowerSeries.invOneSubPow F d) =
        h.eval (n : F) :=
  Polynomial.existsUnique_hilbertPoly p d

end HilbertPolynomialAnchors

end MathlibAnchors

namespace ExternalLeanAudit

/-- One row in the Stage1 external Lean-project audit for the Bezout slot. -/
structure ExternalAnchorRow where
  searchTarget : String
  source : String
  url : String
  revision : String
  observedNames : List String
  lakeClosureFeasibility : String
  verdict : String

/--
Integration-ready external Lean 4 audit rows for `S1-M-029-F`.

No row below is a completion claim: the audit found local Hilbert-polynomial
infrastructure and Groebner-basis bridge projects, but no importable external
Lean 4 proof of the projective plane intersection-length form of Bezout's
theorem.  Therefore this artifact deliberately records blockers instead of
adding any dependency to the shared Lake configuration.
-/
def externalAnchorAuditTable : List ExternalAnchorRow :=
  [ { searchTarget := "Hilbert polynomial"
      source := "pinned mathlib dependency already in this Lake project"
      url :=
        "https://github.com/leanprover-community/mathlib4/blob/8a178386ffc0f5fef0b77738bb5449d50efeea95/Mathlib/RingTheory/Polynomial/HilbertPoly.lean"
      revision := "8a178386ffc0f5fef0b77738bb5449d50efeea95"
      observedNames :=
        [ "Polynomial.preHilbertPoly",
          "Polynomial.hilbertPoly",
          "Polynomial.coeff_mul_invOneSubPow_eq_hilbertPoly_eval",
          "Polynomial.existsUnique_hilbertPoly" ]
      lakeClosureFeasibility :=
        "already importable and checked in this file via Mathlib.RingTheory.Polynomial.HilbertPoly"
      verdict :=
        "useful Hilbert-polynomial substrate; not a Bezout or intersection-multiplicity theorem" },
    { searchTarget := "Bezout"
      source := "pinned mathlib dependency already in this Lake project"
      url :=
        "https://github.com/leanprover-community/mathlib4/blob/8a178386ffc0f5fef0b77738bb5449d50efeea95/Mathlib/RingTheory/Bezout.lean"
      revision := "8a178386ffc0f5fef0b77738bb5449d50efeea95"
      observedNames :=
        [ "IsBezout",
          "IsBezout.iff_span_pair_isPrincipal",
          "IsBezout.TFAE" ]
      lakeClosureFeasibility :=
        "already in the dependency closure, but intentionally not imported here because it concerns Bezout rings"
      verdict :=
        "name collision only; not Bezout's theorem on plane-curve intersections" },
    { searchTarget := "intersection multiplicity"
      source := "pinned mathlib dependency source search"
      url :=
        "https://github.com/leanprover-community/mathlib4/tree/8a178386ffc0f5fef0b77738bb5449d50efeea95/Mathlib"
      revision := "8a178386ffc0f5fef0b77738bb5449d50efeea95"
      observedNames := []
      lakeClosureFeasibility :=
        "no projective plane intersection-multiplicity theorem name was found in the local dependency source"
      verdict :=
        "formalization_debt remains for local intersection multiplicity and length bridges" },
    { searchTarget := "Groebner-basis bridge for affine elimination"
      source := "WuProver/groebner_proj"
      url := "https://github.com/WuProver/groebner_proj"
      revision := "c92d123e526cea653f20b66e6d226038fbd7118f"
      observedNames :=
        [ "Groebner/Groebner.lean",
          "Groebner/Ideal.lean",
          "Groebner/Reduced.lean",
          "Groebner/ComputationExamples.lean" ]
      lakeClosureFeasibility :=
        "not pinned; observed project tree does not expose Bezout, Hilbert polynomial, or intersection-multiplicity theorem names"
      verdict :=
        "possible future affine bridge infrastructure, not terminal closure for THM-M-0104" },
    { searchTarget := "Groebner-basis bridge for affine elimination"
      source := "Hagb/lean-groebner"
      url := "https://github.com/Hagb/lean-groebner"
      revision := "3b9a7bfe8c009cbc5f9fcbfd55942be67e798a03"
      observedNames :=
        [ "Basic.lean",
          "Division.lean",
          "Groebner.lean",
          "Ideal.lean",
          "Multideg.lean",
          "TermOrder.lean" ]
      lakeClosureFeasibility :=
        "not pinned; observed project tree does not expose Bezout, Hilbert polynomial, or intersection-multiplicity theorem names"
      verdict :=
        "possible future affine bridge infrastructure, not terminal closure for THM-M-0104" } ]

/-- External-audit gate: no terminal external Lean 4 proof was found to pin/import/check. -/
def externalAuditClosureGate : String :=
  "no external Lean 4 projective-plane Bezout proof found; nothing qualifies as external_upstream_pinned"

/-- External-audit blocker for any attempted completed status update. -/
def externalAuditCompletionBlocker : String :=
  "completion blocked until a terminal proof is local_proof_body, local_wrapper_upstream_mathlib, or external_upstream_pinned"

end ExternalLeanAudit

namespace ClosedSubschemeIntersectionAudit

variable {X Y S : Scheme.{u}}

/--
Audit verdict for `S1-M-029-D`.

Mathlib has enough generic closed-subscheme machinery to model intersections
inside a fixed ambient scheme by ideal-sheaf sums, and enough pullback/comap
machinery to compare such closed subschemes under morphisms.  It does not yet
provide a Bezout-specific projective-plane curve API tying homogeneous
polynomial degree, no-common-component hypotheses, finite-length intersection
schemes, and local intersection multiplicity into one theorem surface.
-/
def closedSubschemeIntersectionApiVerdict : String :=
  "generic closed-subscheme intersections are available via IdealSheafData; \
  specialized projective plane curve, degree, length, and multiplicity wrappers remain needed"

/-- The ideal-sheaf data type is the repo-local anchor for closed subschemes. -/
def idealSheafDataAnchor (X : Scheme.{u}) : Type u :=
  X.IdealSheafData

variable (I J : X.IdealSheafData)

/-- A closed subscheme is obtained from ideal-sheaf data. -/
def idealSheafSubschemeAnchor : Scheme.{u} :=
  I.subscheme

/-- The canonical map from an ideal-sheaf subscheme to its ambient scheme. -/
def idealSheafSubschemeInclusionAnchor : I.subscheme ⟶ X :=
  I.subschemeι

/-- Ideal-sheaf subscheme inclusions are closed immersions in the local mathlib checkout. -/
theorem idealSheafSubschemeInclusionClosed :
    IsClosedImmersion I.subschemeι := by
  infer_instance

/--
Intersection of two closed subschemes in the same ambient scheme can be
represented by the subscheme associated to the sum of their ideal sheaves.
-/
def closedSubschemeIntersectionByIdealSum : Scheme.{u} :=
  (I ⊔ J).subscheme

/-- The ideal-sum intersection still carries a closed immersion into the ambient scheme. -/
theorem closedSubschemeIntersectionInclusionClosed :
    IsClosedImmersion (I ⊔ J).subschemeι := by
  infer_instance

/-- The topological support of the ideal-sum subscheme is the intersection of supports. -/
theorem idealSheafSupportSupAnchor :
    (I ⊔ J).support = I.support ⊓ J.support :=
  Scheme.IdealSheafData.support_sup I J

/-- The affine-local ideal of an ideal-sum subscheme is exposed by mathlib. -/
theorem idealSheafIdealSupAnchor :
    (I ⊔ J).ideal = I.ideal ⊔ J.ideal :=
  Scheme.IdealSheafData.ideal_sup

variable (f : X ⟶ Y) (K : Y.IdealSheafData)

/-- Ideal sheaves can be pulled back along scheme morphisms. -/
def idealSheafComapAnchor : X.IdealSheafData :=
  K.comap f

/--
The pulled-back ideal-sheaf subscheme is canonically isomorphic to the
categorical pullback of the original closed subscheme.
-/
def idealSheafComapIsoAnchor :
    (K.comap f).subscheme ≅ pullback f K.subschemeι :=
  K.comapIso f

/-- The comap/pullback comparison identifies the first projection with the subscheme inclusion. -/
theorem idealSheafComapIsoHomFstAnchor :
    (K.comapIso f).hom ≫ pullback.fst f K.subschemeι =
      (K.comap f).subschemeι :=
  Scheme.IdealSheafData.comapIso_hom_fst K f

variable (h : X ⟶ S) (g : Y ⟶ S)

/-- The scheme category supplies pullbacks, the generic scheme-theoretic intersection substrate. -/
def schemePullbackAnchor : Scheme.{u} :=
  pullback h g

/-- A closed immersion remains a closed immersion after pullback. -/
theorem closedImmersionPullbackFstAnchor [IsClosedImmersion g] :
    IsClosedImmersion (pullback.fst h g) := by
  infer_instance

end ClosedSubschemeIntersectionAudit

namespace ProofBudgetLeafLedgers

/--
One M0387-style leaf-budget row for the final Bezout theorem tree.

These rows are checked planning data, not proof claims for the terminal
projective-plane Bezout theorem.  A row may be marked checked only when the
corresponding local Lean declaration already validates in this file.
-/
structure LeafLedgerRow where
  leafId : String
  packageId : String
  localObligation : String
  maxProofSteps : Nat
  repoLocalStatus : String
  completionGate : String

/-- Stable package labels for the final theorem-tree split. -/
def finalTheoremTreePackages : List String :=
  [ "BZ-P0.checked_statement_boundary",
    "BZ-P1.statement_normalization",
    "BZ-P2.mathlib_object_model",
    "BZ-P3.projective_curve_model",
    "BZ-P4.intersection_scheme_and_length",
    "BZ-P5.local_intersection_multiplicity",
    "BZ-P6.degree_and_hilbert_bridge",
    "BZ-P7.special_cases_and_bounds",
    "BZ-P8.external_or_terminal_closure",
    "BZ-P9.public_merge_gate" ]

/--
Independent `<=100` proof-budget leaves for the final theorem tree.

The checked rows are limited to statement-shape declarations and small bridge
lemmas already present in this module.  All terminal projective Bezout proof
leaves remain `unchecked_formalization_debt`.
-/
def finalTheoremTreeLeafLedgers : List LeafLedgerRow :=
  [ { leafId := "BZ-L001.checked.variant_freeze"
      packageId := "BZ-P0.checked_statement_boundary"
      localObligation := "Record projective-plane length theorem as the canonical statement variant."
      maxProofSteps := 1
      repoLocalStatus := "checked_local"
      completionGate := "definition selectedStatementVariant typechecks; not a terminal proof" },
    { leafId := "BZ-L002.checked.homogeneous_ternary_type"
      packageId := "BZ-P0.checked_statement_boundary"
      localObligation := "Expose homogeneous ternary polynomial statement type."
      maxProofSteps := 1
      repoLocalStatus := "checked_local"
      completionGate := "definition HomogeneousPlanePolynomial typechecks" },
    { leafId := "BZ-L003.checked.statement_data_shape"
      packageId := "BZ-P0.checked_statement_boundary"
      localObligation := "Expose PlaneCurveIntersectionData, BezoutHypotheses, BezoutConclusion, and StatementShape."
      maxProofSteps := 5
      repoLocalStatus := "checked_local"
      completionGate := "statement-shape declarations typecheck; theorem payload fields remain abstract" },
    { leafId := "BZ-L004.checked.length_implies_bound"
      packageId := "BZ-P7.special_cases_and_bounds"
      localObligation := "Derive the weak multiplicity-counted bound from the normalized equality conclusion."
      maxProofSteps := 1
      repoLocalStatus := "checked_local"
      completionGate := "theorem lengthConclusion_implies_multiplicityBound validates locally" },
    { leafId := "BZ-L005.checked.line_left_arithmetic"
      packageId := "BZ-P7.special_cases_and_bounds"
      localObligation := "Specialize the degree-product equality when the first curve has degree one."
      maxProofSteps := 5
      repoLocalStatus := "checked_local"
      completionGate := "theorem lengthConclusion_lineLeft_equals_curveDegree validates locally" },
    { leafId := "BZ-L006.checked.line_right_arithmetic"
      packageId := "BZ-P7.special_cases_and_bounds"
      localObligation := "Specialize the degree-product equality when the second curve has degree one."
      maxProofSteps := 5
      repoLocalStatus := "checked_local"
      completionGate := "theorem lengthConclusion_lineRight_equals_curveDegree validates locally" },
    { leafId := "BZ-L007.checked.closed_subscheme_anchors"
      packageId := "BZ-P2.mathlib_object_model"
      localObligation := "Check ideal-sheaf subscheme, ideal-sum intersection, comap, and pullback closed-immersion anchors."
      maxProofSteps := 10
      repoLocalStatus := "checked_local"
      completionGate := "ClosedSubschemeIntersectionAudit anchors validate locally; no curve-degree theorem claimed" },
    { leafId := "BZ-L008.unchecked.projective_plane_model"
      packageId := "BZ-P3.projective_curve_model"
      localObligation := "Instantiate the projective plane as the selected Proj/projective-space object over the base field."
      maxProofSteps := 100
      repoLocalStatus := "unchecked_formalization_debt"
      completionGate := "must compile against the chosen mathlib projective-plane API" },
    { leafId := "BZ-L009.unchecked.curve_zero_locus"
      packageId := "BZ-P3.projective_curve_model"
      localObligation := "Turn a homogeneous ternary polynomial into a closed subscheme or equivalent curve object."
      maxProofSteps := 100
      repoLocalStatus := "unchecked_formalization_debt"
      completionGate := "must replace abstract curve fields with concrete checked objects" },
    { leafId := "BZ-L010.unchecked.degree_payload"
      packageId := "BZ-P3.projective_curve_model"
      localObligation := "Connect homogeneous polynomial degree with the chosen curve/divisor degree payload."
      maxProofSteps := 100
      repoLocalStatus := "unchecked_formalization_debt"
      completionGate := "must validate degree coercions and no hidden terminal theorem claim" },
    { leafId := "BZ-L011.unchecked.no_common_component_predicate"
      packageId := "BZ-P1.statement_normalization"
      localObligation := "Choose the no-common-component predicate: homogeneous factors, ideal height, or scheme components."
      maxProofSteps := 100
      repoLocalStatus := "unchecked_formalization_debt"
      completionGate := "predicate must be usable by the selected intersection proof route" },
    { leafId := "BZ-L012.unchecked.no_common_component_equivalence"
      packageId := "BZ-P1.statement_normalization"
      localObligation := "Bridge the chosen algebraic and geometric no-common-component formulations."
      maxProofSteps := 100
      repoLocalStatus := "unchecked_formalization_debt"
      completionGate := "split again if irreducible-factor, ideal, and component APIs do not close under budget" },
    { leafId := "BZ-L013.unchecked.intersection_construction"
      packageId := "BZ-P4.intersection_scheme_and_length"
      localObligation := "Define curve intersection by ideal-sheaf sum, pullback of closed immersions, or quotient algebra."
      maxProofSteps := 100
      repoLocalStatus := "unchecked_formalization_debt"
      completionGate := "must compile as a concrete intersection object" },
    { leafId := "BZ-L014.unchecked.finite_support"
      packageId := "BZ-P4.intersection_scheme_and_length"
      localObligation := "Prove finite intersection support from the no-common-component hypothesis."
      maxProofSteps := 100
      repoLocalStatus := "unchecked_formalization_debt"
      completionGate := "one affine-chart or support bridge per child leaf if this exceeds budget" },
    { leafId := "BZ-L015.unchecked.support_common_zeros"
      packageId := "BZ-P4.intersection_scheme_and_length"
      localObligation := "Relate the scheme support to common zeros of the homogeneous forms."
      maxProofSteps := 100
      repoLocalStatus := "unchecked_formalization_debt"
      completionGate := "must preserve projective-coordinate and closed-point conventions" },
    { leafId := "BZ-L016.unchecked.local_multiplicity_definition"
      packageId := "BZ-P5.local_intersection_multiplicity"
      localObligation := "Define local intersection multiplicity as a local quotient length or selected equivalent."
      maxProofSteps := 100
      repoLocalStatus := "unchecked_formalization_debt"
      completionGate := "must use concrete local ring/module length APIs" },
    { leafId := "BZ-L017.unchecked.local_finite_length"
      packageId := "BZ-P5.local_intersection_multiplicity"
      localObligation := "Prove the local quotient has finite length at every support point."
      maxProofSteps := 100
      repoLocalStatus := "unchecked_formalization_debt"
      completionGate := "split local-ring, quotient, and Artinian/Noetherian leaves if needed" },
    { leafId := "BZ-L018.unchecked.global_sum"
      packageId := "BZ-P5.local_intersection_multiplicity"
      localObligation := "Prove global intersection length equals the finite sum of local multiplicities."
      maxProofSteps := 100
      repoLocalStatus := "unchecked_formalization_debt"
      completionGate := "must validate the finite-indexing and length decomposition APIs" },
    { leafId := "BZ-L019.unchecked.transverse_reduced_multiplicity"
      packageId := "BZ-P7.special_cases_and_bounds"
      localObligation := "Prove multiplicity one under the selected transverse or reduced hypotheses."
      maxProofSteps := 100
      repoLocalStatus := "unchecked_formalization_debt"
      completionGate := "corollary only; not a substitute for the length theorem" },
    { leafId := "BZ-L020.unchecked.hilbert_exact_sequence"
      packageId := "BZ-P6.degree_and_hilbert_bridge"
      localObligation := "Build the graded exact sequence or divisor-degree bridge induced by multiplication by a form."
      maxProofSteps := 100
      repoLocalStatus := "unchecked_formalization_debt"
      completionGate := "must tie current Hilbert-polynomial anchors to graded modules or selected substitute" },
    { leafId := "BZ-L021.unchecked.product_formula_core"
      packageId := "BZ-P6.degree_and_hilbert_bridge"
      localObligation := "Extract the degree-product length formula from Hilbert polynomial, divisor degree, or pinned theorem."
      maxProofSteps := 100
      repoLocalStatus := "unchecked_formalization_debt"
      completionGate := "cannot close by anchor-only evidence" },
    { leafId := "BZ-L022.unchecked.bezout_equality"
      packageId := "BZ-P6.degree_and_hilbert_bridge"
      localObligation := "Assemble hypotheses to prove totalIntersectionMultiplicity = degreeF * degreeG."
      maxProofSteps := 100
      repoLocalStatus := "unchecked_formalization_debt"
      completionGate := "requires concrete curve, intersection, length, and degree APIs" },
    { leafId := "BZ-L023.unchecked.geometric_point_bound"
      packageId := "BZ-P7.special_cases_and_bounds"
      localObligation := "Derive the geometric point-count bound from local multiplicity positivity and the length theorem."
      maxProofSteps := 100
      repoLocalStatus := "unchecked_formalization_debt"
      completionGate := "must remain a corollary or narrowed theorem, not the canonical length theorem" },
    { leafId := "BZ-L024.unchecked.affine_patch_bridge"
      packageId := "BZ-P7.special_cases_and_bounds"
      localObligation := "Prove an affine dehomogenization bridge for common zeros on a selected chart."
      maxProofSteps := 100
      repoLocalStatus := "unchecked_formalization_debt"
      completionGate := "must state chart coverage and points-at-infinity boundary separately" },
    { leafId := "BZ-L025.unchecked.line_curve_terminal_bridge"
      packageId := "BZ-P7.special_cases_and_bounds"
      localObligation := "Reconnect the checked arithmetic line-vs-curve bridge to actual line and curve objects."
      maxProofSteps := 100
      repoLocalStatus := "unchecked_formalization_debt"
      completionGate := "must not rely only on abstract degree fields" },
    { leafId := "BZ-L026.unchecked.external_terminal_pin"
      packageId := "BZ-P8.external_or_terminal_closure"
      localObligation := "If a terminal external Lean 4 Bezout proof is found, pin/import/check it or record a concrete blocker."
      maxProofSteps := 100
      repoLocalStatus := "unchecked_no_external_terminal_anchor_found"
      completionGate := "completed state forbidden with external_upstream_anchor_only" },
    { leafId := "BZ-L027.unchecked.local_terminal_wrapper"
      packageId := "BZ-P8.external_or_terminal_closure"
      localObligation := "Create the terminal repo-local wrapper theorem only after local, mathlib, or pinned external proof closure exists."
      maxProofSteps := 50
      repoLocalStatus := "unchecked_formalization_debt"
      completionGate := "must validate with lake env lean and no proof holes" },
    { leafId := "BZ-L028.unchecked.local_validation"
      packageId := "BZ-P8.external_or_terminal_closure"
      localObligation := "Run the exact local validation command for the terminal wrapper."
      maxProofSteps := 20
      repoLocalStatus := "unchecked_process_gate"
      completionGate := "record command, date, exit code, and warning/error status" },
    { leafId := "BZ-L029.unchecked.public_merge_sync"
      packageId := "BZ-P9.public_merge_gate"
      localObligation := "Merge public theorem tree, human-readable expansion, status surfaces, and validation record through a serial integrator."
      maxProofSteps := 20
      repoLocalStatus := "unchecked_public_integration_gate"
      completionGate := "public docs remain open until machine anchor, validation, and leaf ledgers agree" } ]

/-- Boolean audit: every leaf row is budgeted at or below the M0387 limit. -/
def allFinalLeafBudgetsWithinM0387Limit : Bool :=
  finalTheoremTreeLeafLedgers.all (fun row => row.maxProofSteps ≤ 100)

/-- Checked audit: the current final theorem tree has exactly twenty-nine leaf rows. -/
theorem finalTheoremTreeLeafLedger_count :
    finalTheoremTreeLeafLedgers.length = 29 := by
  native_decide

/-- Checked audit: every current leaf row is budgeted at or below one hundred steps. -/
theorem allFinalLeafBudgetsWithinM0387Limit_eq_true :
    allFinalLeafBudgetsWithinM0387Limit = true := by
  native_decide

end ProofBudgetLeafLedgers

namespace HumanReadableProofFlow

/--
One reader-facing proof-flow row for the public Bezout backfill surface.

These rows are static integration data for the serial public-doc merge.  They
translate the checked statement/anchor/process surface into prose-ready proof
flow, while preserving the rule that unchecked terminal Bezout leaves stay
open until concrete curve, intersection, length, and degree APIs compile.
-/
structure ProofFlowRow where
  packageId : String
  readerFacingRole : String
  upstreamInputs : String
  downstreamInterface : String
  publicStatus : String

/--
Integration-ready human-readable proof-flow expansion for `S1-M-029-H`.

This table is intentionally package-level.  It gives the public integrator
stable text to merge into the designated public surface without creating a
second canonical theorem tree or claiming completion beyond the checked local
anchors in this module.
-/
def proofFlowExpansionRows : List ProofFlowRow :=
  [ { packageId := "BZ-P0.checked_statement_boundary"
      readerFacingRole :=
        "Freeze the public theorem target as the projective-plane intersection-length form of Bezout."
      upstreamInputs :=
        "Stage1 statement-normalization choice and homogeneous ternary polynomial notation."
      downstreamInterface :=
        "Provides PlaneCurveIntersectionData, BezoutHypotheses, BezoutConclusion, and StatementShape."
      publicStatus :=
        "checked local statement shape; not a terminal Bezout proof" },
    { packageId := "BZ-P1.statement_normalization"
      readerFacingRole :=
        "Keep geometric-point and affine variants subordinate to the length theorem, and isolate no-common-component choices."
      upstreamInputs :=
        "Selected statement variant plus the abstract noCommonComponent field."
      downstreamInterface :=
        "Feeds the curve model and finite-intersection branches once a concrete predicate is selected."
      publicStatus :=
        "partly checked for variant selection; no-common-component equivalences remain unchecked formalization_debt" },
    { packageId := "BZ-P2.mathlib_object_model"
      readerFacingRole :=
        "Record the imported mathlib substrate: schemes, Proj, closed immersions, homogeneous ideals, finite length, Hilbert polynomials, and ideal-sheaf intersections."
      upstreamInputs :=
        "Pinned mathlib dependency available through the local Lake project."
      downstreamInterface :=
        "Supplies checked anchors for later curve, intersection, and length wrappers."
      publicStatus :=
        "checked local anchors; no specialized projective-plane Bezout theorem found" },
    { packageId := "BZ-P3.projective_curve_model"
      readerFacingRole :=
        "Replace the current abstract curve fields with concrete projective-plane curves cut out by homogeneous ternary forms."
      upstreamInputs :=
        "Proj/projective-space API, homogeneous polynomial API, and selected degree convention."
      downstreamInterface :=
        "Must produce concrete curve objects, degree payloads, and zero-locus maps for the intersection package."
      publicStatus :=
        "unchecked formalization_debt" },
    { packageId := "BZ-P4.intersection_scheme_and_length"
      readerFacingRole :=
        "Construct the scheme-theoretic intersection and prove that its support and length have the required finiteness properties."
      upstreamInputs :=
        "Concrete curve objects, closed-immersion or ideal-sheaf representation, and no-common-component hypothesis."
      downstreamInterface :=
        "Feeds local multiplicity definitions and the global length decomposition."
      publicStatus :=
        "generic ideal-sheaf intersection anchors checked; specialized finiteness and length proof unchecked" },
    { packageId := "BZ-P5.local_intersection_multiplicity"
      readerFacingRole :=
        "Define local intersection multiplicity and relate the finite global intersection length to the sum of local lengths."
      upstreamInputs :=
        "Concrete intersection scheme, finite support, local quotient rings/modules, and finite-length APIs."
      downstreamInterface :=
        "Provides totalIntersectionMultiplicity as an actual finite local-length sum."
      publicStatus :=
        "unchecked formalization_debt" },
    { packageId := "BZ-P6.degree_and_hilbert_bridge"
      readerFacingRole :=
        "Prove the product-of-degrees formula using a Hilbert-polynomial, divisor-degree, or pinned terminal theorem route."
      upstreamInputs :=
        "Degree payloads for curves, graded exact sequence or divisor-degree machinery, and the length/multiplicity bridge."
      downstreamInterface :=
        "Must produce totalIntersectionMultiplicity = degreeF * degreeG."
      publicStatus :=
        "Hilbert-polynomial anchors checked; terminal product formula unchecked" },
    { packageId := "BZ-P7.special_cases_and_bounds"
      readerFacingRole :=
        "Expose safe corollary targets such as the multiplicity-counted bound and line-vs-curve arithmetic bridge."
      upstreamInputs :=
        "The normalized length conclusion, plus degree-one hypotheses for the line special case."
      downstreamInterface :=
        "Provides checked arithmetic bridge lemmas, pending reconnection to concrete line and curve objects."
      publicStatus :=
        "checked local arithmetic bridges; geometric object bridge unchecked" },
    { packageId := "BZ-P8.external_or_terminal_closure"
      readerFacingRole :=
        "Prevent anchor-only completion by requiring a local proof body, a checked mathlib wrapper, or a pinned external proof before any completed status."
      upstreamInputs :=
        "External audit rows for Hilbert polynomial, Bezout-name collision, intersection multiplicity, and Groebner projects."
      downstreamInterface :=
        "Blocks completed status unless terminal proof closure is imported and validated."
      publicStatus :=
        "no terminal external Lean 4 Bezout proof found; no repo_local_integration_debt completion claim" },
    { packageId := "BZ-P9.public_merge_gate"
      readerFacingRole :=
        "Serially merge the proof-flow text, status surfaces, validation record, and theorem-tree ledger into public docs."
      upstreamInputs :=
        "Checked Lean artifact, proof-budget ledger, external-audit verdict, and child ledger."
      downstreamInterface :=
        "Integrator updates blueprint/todo/README/meta only after all gates agree."
      publicStatus :=
        "open public integration gate for this child" } ]

/-- Public-merge gate for the human-readable expansion child. -/
def publicProofFlowMergeGate : String :=
  "serial public-doc integration required; worker provides checked proof-flow data only"

/-- Checked audit: the proof-flow expansion currently covers all ten package rows. -/
theorem proofFlowExpansionRows_count :
    proofFlowExpansionRows.length = 10 := by
  native_decide

end HumanReadableProofFlow

/-- Local audit marker: full theorem is not repo-local closed by this statement-shape artifact. -/
def machineProofDebtClassification : String :=
  "formalization_debt"

/-- Local audit marker for the no-anchor-only completion rule. -/
def repoLocalIntegrationDebtGate : String :=
    "not completed; no external Lean 4 terminal proof is imported into this Lake closure"

/-- Local audit marker listing the imported substrate used by this file. -/
def mathlibAnchorModules : List String :=
  [ "Mathlib.AlgebraicGeometry.Scheme",
    "Mathlib.AlgebraicGeometry.IdealSheaf.Functorial",
    "Mathlib.AlgebraicGeometry.Morphisms.ClosedImmersion",
    "Mathlib.AlgebraicGeometry.ProjectiveSpectrum.Basic",
    "Mathlib.AlgebraicGeometry.ProjectiveSpectrum.Scheme",
    "Mathlib.AlgebraicGeometry.Pullbacks",
    "Mathlib.RingTheory.FiniteLength",
    "Mathlib.RingTheory.GradedAlgebra.Homogeneous.Ideal",
    "Mathlib.RingTheory.MvPolynomial.Homogeneous",
    "Mathlib.RingTheory.Polynomial.HilbertPoly" ]

#check HomogeneousPlanePolynomial
#check BezoutStatementVariant
#check selectedStatementVariant
#check PlaneCurveIntersectionData
#check BezoutHypotheses
#check BezoutConclusion
#check BezoutMultiplicityBoundConclusion
#check StatementShape
#check lengthConclusion_implies_multiplicityBound
#check LineCurveBridgeConclusion
#check LineCurveBridgeStatementShape
#check LineLeftCurveBridgeData
#check LineRightCurveBridgeData
#check LineLeftCurveBridgeHypotheses
#check LineRightCurveBridgeHypotheses
#check LineLeftCurveBridgeConclusion
#check LineRightCurveBridgeConclusion
#check LineLeftCurveBridgeStatementShape
#check LineRightCurveBridgeStatementShape
#check lengthConclusion_lineLeft_equals_curveDegree
#check lengthConclusion_lineRight_equals_curveDegree
#check lengthConclusion_implies_lineLeftCurveBridgeTarget
#check lengthConclusion_implies_lineRightCurveBridgeTarget
#check lengthConclusion_implies_lineCurveBridge
#check statementShape_implies_lineCurveBridgeStatement
#check statementShape_implies_lineLeftCurveBridgeStatement
#check statementShape_implies_lineRightCurveBridgeStatement
#check MvPolynomial.IsHomogeneous
#check MvPolynomial.totalDegree
#check Scheme
#check Proj
#check ProjectiveSpectrum
#check ProjectiveSpectrum.basicOpen
#check AlgebraicGeometry.Proj.basicOpen
#check AlgebraicGeometry.Proj.basicOpenIsoSpec
#check IsClosedImmersion
#check IsClosedImmersion.isClosedEmbedding
#check IsClosedImmersion.iff_isPreimmersion
#check HomogeneousIdeal
#check HomogeneousIdeal.irrelevant
#check IsFiniteLength
#check isFiniteLength_iff_isNoetherian_isArtinian
#check isFiniteLength_iff_exists_compositionSeries
#check MvPolynomial.homogeneousSubmodule
#check MvPolynomial.mem_homogeneousSubmodule
#check MvPolynomial.homogeneousSubmodule_mul
#check Polynomial.preHilbertPoly
#check Polynomial.hilbertPoly
#check Polynomial.natDegree_preHilbertPoly
#check Polynomial.hilbertPoly_X_pow_succ
#check Polynomial.coeff_mul_invOneSubPow_eq_hilbertPoly_eval
#check Polynomial.existsUnique_hilbertPoly
#check MathlibAnchors.hilbertPolynomialAnchor
#check MathlibAnchors.preHilbertPolynomialAnchor
#check MathlibAnchors.preHilbertPolynomialNatDegreeAnchor
#check MathlibAnchors.hilbertPolynomialXPowSuccAnchor
#check MathlibAnchors.hilbertPolynomialExistsUniqueAnchor
#check ExternalLeanAudit.ExternalAnchorRow
#check ExternalLeanAudit.externalAnchorAuditTable
#check ExternalLeanAudit.externalAuditClosureGate
#check ExternalLeanAudit.externalAuditCompletionBlocker
#check ClosedSubschemeIntersectionAudit.closedSubschemeIntersectionApiVerdict
#check ClosedSubschemeIntersectionAudit.idealSheafDataAnchor
#check ClosedSubschemeIntersectionAudit.idealSheafSubschemeAnchor
#check ClosedSubschemeIntersectionAudit.idealSheafSubschemeInclusionAnchor
#check ClosedSubschemeIntersectionAudit.idealSheafSubschemeInclusionClosed
#check ClosedSubschemeIntersectionAudit.closedSubschemeIntersectionByIdealSum
#check ClosedSubschemeIntersectionAudit.closedSubschemeIntersectionInclusionClosed
#check ClosedSubschemeIntersectionAudit.idealSheafSupportSupAnchor
#check ClosedSubschemeIntersectionAudit.idealSheafIdealSupAnchor
#check ClosedSubschemeIntersectionAudit.idealSheafComapAnchor
#check ClosedSubschemeIntersectionAudit.idealSheafComapIsoAnchor
#check ClosedSubschemeIntersectionAudit.idealSheafComapIsoHomFstAnchor
#check ClosedSubschemeIntersectionAudit.schemePullbackAnchor
#check ClosedSubschemeIntersectionAudit.closedImmersionPullbackFstAnchor
#check Scheme.IdealSheafData.subscheme
#check Scheme.IdealSheafData.subschemeι
#check Scheme.IdealSheafData.support_sup
#check Scheme.IdealSheafData.comap
#check Scheme.IdealSheafData.comapIso
#check pullback
#check pullback.fst
#check ProofBudgetLeafLedgers.LeafLedgerRow
#check ProofBudgetLeafLedgers.finalTheoremTreePackages
#check ProofBudgetLeafLedgers.finalTheoremTreeLeafLedgers
#check ProofBudgetLeafLedgers.allFinalLeafBudgetsWithinM0387Limit
#check ProofBudgetLeafLedgers.finalTheoremTreeLeafLedger_count
#check ProofBudgetLeafLedgers.allFinalLeafBudgetsWithinM0387Limit_eq_true
#check HumanReadableProofFlow.ProofFlowRow
#check HumanReadableProofFlow.proofFlowExpansionRows
#check HumanReadableProofFlow.publicProofFlowMergeGate
#check HumanReadableProofFlow.proofFlowExpansionRows_count

end AwesomeTheorems.Stage1.S1_M_029
