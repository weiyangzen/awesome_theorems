import Mathlib.RingTheory.NoetherNormalization
import Mathlib.AlgebraicGeometry.AffineSpace
import Mathlib.AlgebraicGeometry.Morphisms.Finite

/-!
# S1-M-030 / THM-M-0106: Noether normalization lemma

This Stage1 artifact records a repo-local Lean boundary for the affine
Noether normalization theorem.  The checked theorems below split the
commutative-algebra package into the integral normalization theorem, the finite
module upgrade, and the corresponding finite morphism between affine schemes.
-/

noncomputable section

open CategoryTheory
open AlgebraicGeometry

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_030

universe u

/-- Proof-package labels for the Stage1 Noether-normalization split. -/
inductive CommutativeAlgebraPackage where
  | polynomialAlgebraSource
  | integralEmbedding
  | finiteModuleUpgrade
  | affineSpecFiniteMorphism
  | publicStatementBridge
  deriving DecidableEq, Repr

/-- Ordered package split for the commutative-algebra part of THM-M-0106. -/
def commutativeAlgebraPackageSplit : List CommutativeAlgebraPackage := [
  CommutativeAlgebraPackage.polynomialAlgebraSource,
  CommutativeAlgebraPackage.integralEmbedding,
  CommutativeAlgebraPackage.finiteModuleUpgrade,
  CommutativeAlgebraPackage.affineSpecFiniteMorphism,
  CommutativeAlgebraPackage.publicStatementBridge
]

/--
Integral statement shape: the first mathlib package supplies an injective
polynomial-algebra map over which the target algebra is integral.
-/
def IntegralStatementShape : Prop :=
  ∀ (k R : Type u) [Field k] [CommRing R] [Nontrivial R] [Algebra k R]
    [Algebra.FiniteType k R],
    ∃ s, ∃ g : MvPolynomial (Fin s) k →ₐ[k] R,
      Function.Injective g ∧ g.IsIntegral

/--
Algebraic statement shape: a finitely generated nonzero algebra over a field is
finite over an injectively embedded polynomial algebra in finitely many
variables.
-/
def AlgebraicStatementShape : Prop :=
  ∀ (k R : Type u) [Field k] [CommRing R] [Nontrivial R] [Algebra k R]
    [Algebra.FiniteType k R],
    ∃ s, ∃ g : MvPolynomial (Fin s) k →ₐ[k] R,
      Function.Injective g ∧ g.Finite

/--
Geometric affine statement shape: for an affine `k`-scheme represented as
`Spec R`, the mathlib normalization map gives a finite morphism to affine space
`Spec k[X_0, ..., X_(s-1)]`.
-/
def AffineSchemeStatementShape : Prop :=
  ∀ (k R : Type u) [Field k] [CommRing R] [Nontrivial R] [Algebra k R]
    [Algebra.FiniteType k R],
    ∃ s, ∃ g : MvPolynomial (Fin s) k →ₐ[k] R,
      Function.Injective g ∧ g.Finite ∧
        IsFinite (Spec.map (CommRingCat.ofHom g.toRingHom))

/--
The explicit affine-space morphism induced by a finite algebra map
`k[X_0, ..., X_(s-1)] →ₐ[k] R`.
-/
def affineSpaceMorphismOfAlgHom {k R : Type u} [Field k] [CommRing R] [Algebra k R]
    {s : ℕ} (g : MvPolynomial (Fin s) k →ₐ[k] R) :
    Spec (CommRingCat.of R) ⟶
      AlgebraicGeometry.AffineSpace (Fin s) (Spec (CommRingCat.of k)) :=
  Spec.map (CommRingCat.ofHom g.toRingHom) ≫
    (AlgebraicGeometry.AffineSpace.SpecIso (Fin s) (CommRingCat.of k)).inv

/--
A06 prototype audit: after identifying affine space over `Spec k` with
`Spec k[X_0, ..., X_(s-1)]`, the morphism is exactly the affine-Spec map of the
coordinate-ring algebra map.
-/
theorem affineSpaceMorphismOfAlgHom_comp_SpecIso_hom {k R : Type u}
    [Field k] [CommRing R] [Algebra k R] {s : ℕ}
    (g : MvPolynomial (Fin s) k →ₐ[k] R) :
    affineSpaceMorphismOfAlgHom g ≫
        (AlgebraicGeometry.AffineSpace.SpecIso (Fin s) (CommRingCat.of k)).hom =
      Spec.map (CommRingCat.ofHom g.toRingHom) := by
  simp [affineSpaceMorphismOfAlgHom]

/--
A07 transport theorem: the affine-space morphism attached to a finite
coordinate-ring algebra map is finite.  The `Spec.map` leg is finite by
`IsFinite.SpecMap_iff`, and the final affine-space isomorphism preserves the
finite-morphism property.
-/
theorem finite_affineSpaceMorphismOfAlgHom {k R : Type u}
    [Field k] [CommRing R] [Algebra k R] {s : ℕ}
    (g : MvPolynomial (Fin s) k →ₐ[k] R) (hg : g.Finite) :
    IsFinite (affineSpaceMorphismOfAlgHom g) := by
  have hSpec : IsFinite (Spec.map (CommRingCat.ofHom g.toRingHom)) := by
    rw [AlgebraicGeometry.IsFinite.SpecMap_iff]
    exact hg
  dsimp [affineSpaceMorphismOfAlgHom]
  exact MorphismProperty.RespectsIso.postcomp (P := @IsFinite)
    (AlgebraicGeometry.AffineSpace.SpecIso (Fin s) (CommRingCat.of k)).inv
    (Spec.map (CommRingCat.ofHom g.toRingHom)) hSpec

/--
A06 checked existential shape: every finite algebra map supplied in the
Noether-normalization package gives a concrete morphism from `Spec R` to the
standard affine space over `Spec k`.
-/
def AffineSpaceMorphismStatementShape : Prop :=
  ∀ (k R : Type u) [Field k] [CommRing R] [Algebra k R]
    (s : ℕ) (g : MvPolynomial (Fin s) k →ₐ[k] R), g.Finite →
      ∃ f : Spec (CommRingCat.of R) ⟶
          AlgebraicGeometry.AffineSpace (Fin s) (Spec (CommRingCat.of k)),
        f ≫ (AlgebraicGeometry.AffineSpace.SpecIso (Fin s) (CommRingCat.of k)).hom =
          Spec.map (CommRingCat.ofHom g.toRingHom)

/--
Child-task wrapper for `S1-M-030-A06`: construct the scheme morphism to affine
space from the finite algebra map.  Finiteness of the morphism itself is the
separate `S1-M-030-A07` transport step.
-/
theorem s1_m_030_a06_affineSpaceMorphism_from_finite_algHom :
    AffineSpaceMorphismStatementShape := by
  intro k R _ _ _ s g _hg
  exact ⟨affineSpaceMorphismOfAlgHom g, affineSpaceMorphismOfAlgHom_comp_SpecIso_hom g⟩

/--
A07 checked shape: the concrete affine-space morphism constructed in A06 is a
finite morphism whenever the coordinate-ring algebra map is finite.
-/
def AffineSpaceFiniteMorphismStatementShape : Prop :=
  ∀ (k R : Type u) [Field k] [CommRing R] [Algebra k R]
    (s : ℕ) (g : MvPolynomial (Fin s) k →ₐ[k] R), g.Finite →
      IsFinite (affineSpaceMorphismOfAlgHom g)

/--
Child-task wrapper for `S1-M-030-A07`: finiteness of the morphism to affine
space follows from `AlgebraicGeometry.IsFinite.SpecMap_iff` plus transport
across `AlgebraicGeometry.AffineSpace.SpecIso`.
-/
theorem s1_m_030_a07_affineSpaceMorphism_isFinite :
    AffineSpaceFiniteMorphismStatementShape := by
  intro k R _ _ _ s g hg
  exact finite_affineSpaceMorphismOfAlgHom g hg

/--
Checked mathlib wrapper for the integral Noether-normalization package.
-/
theorem noetherNormalization_integral_mathlib_wrapper :
    IntegralStatementShape := by
  intro k R _ _ _ _ _
  exact exists_integral_inj_algHom_of_fg k R

/--
Child-task wrapper for `S1-M-030-A02`: expose the integral coordinate-ring
Noether-normalization statement under a stable task-level name.
-/
theorem s1_m_030_a02_exists_integral_inj_algHom_of_fg_ring_wrapper :
    IntegralStatementShape :=
  noetherNormalization_integral_mathlib_wrapper

/--
Checked finite-module upgrade package: the integral normalization statement
implies the finite normalization statement for finitely generated algebras.
-/
theorem integralStatementShape_to_algebraicStatementShape :
    IntegralStatementShape.{u} → AlgebraicStatementShape.{u} := by
  intro h k R _ _ _ _ _
  obtain ⟨s, g, hg_inj, hg_integral⟩ := h k R
  refine ⟨s, g, hg_inj, ?_⟩
  have hcomp :
      algebraMap k R = g.toRingHom.comp (algebraMap k (MvPolynomial (Fin s) k)) := by
    algebraize [g.toRingHom]
    rw [IsScalarTower.algebraMap_eq k (MvPolynomial (Fin s) k),
      RingHom.algebraMap_toAlgebra']
  exact hg_integral.to_finite
    (hcomp ▸
      RingHom.finiteType_algebraMap.mpr
        (inferInstance : Algebra.FiniteType k R)).of_comp_finiteType

/--
Checked mathlib wrapper for the finite algebraic Noether-normalization theorem.
-/
theorem noetherNormalization_algebraic_mathlib_wrapper :
    AlgebraicStatementShape := by
  intro k R _ _ _ _ _
  exact exists_finite_inj_algHom_of_fg k R

/--
Child-task wrapper for `S1-M-030-A03`: expose the finite coordinate-ring
Noether-normalization statement under a stable task-level name.
-/
theorem s1_m_030_a03_exists_finite_inj_algHom_of_fg_ring_wrapper :
    AlgebraicStatementShape :=
  noetherNormalization_algebraic_mathlib_wrapper

/--
Checked affine-Spec package: a finite algebra map induces a finite morphism on
affine spectra.
-/
theorem algebraicStatementShape_to_affineSchemeStatementShape :
    AlgebraicStatementShape.{u} → AffineSchemeStatementShape.{u} := by
  intro h k R _ _ _ _ _
  obtain ⟨s, g, hg_inj, hg_finite⟩ := h k R
  refine ⟨s, g, hg_inj, hg_finite, ?_⟩
  rw [AlgebraicGeometry.IsFinite.SpecMap_iff]
  exact hg_finite

/--
Checked affine-scheme wrapper: the finite algebra map supplied by mathlib
induces a finite morphism from `Spec R` to affine space.
-/
theorem noetherNormalization_affineScheme_mathlib_wrapper :
    AffineSchemeStatementShape := by
  intro k R _ _ _ _ _
  obtain ⟨s, g, hg_inj, hg_finite⟩ := exists_finite_inj_algHom_of_fg k R
  refine ⟨s, g, hg_inj, hg_finite, ?_⟩
  rw [AlgebraicGeometry.IsFinite.SpecMap_iff]
  exact hg_finite

/--
Optional affine-variety specialization shape for `S1-M-030-A08`.

Mathlib's currently imported algebraic-geometry surface does not provide a
separate general-purpose `AffineVariety` category here, so the repo-local
specialization uses the standard coordinate-ring boundary: a reduced finite
type affine `k`-algebra represented by `Spec R`.  The conclusion is the checked
finite morphism from that affine scheme to affine space.
-/
def AffineVarietyCoordinateRingStatementShape : Prop :=
  ∀ (k R : Type u) [Field k] [CommRing R] [Nontrivial R] [Algebra k R]
    [Algebra.FiniteType k R] [IsReduced R],
    ∃ s, ∃ g : MvPolynomial (Fin s) k →ₐ[k] R,
      Function.Injective g ∧ g.Finite ∧
        ∃ f : Spec (CommRingCat.of R) ⟶
            AlgebraicGeometry.AffineSpace (Fin s) (Spec (CommRingCat.of k)),
          IsFinite f ∧
            f ≫ (AlgebraicGeometry.AffineSpace.SpecIso (Fin s) (CommRingCat.of k)).hom =
              Spec.map (CommRingCat.ofHom g.toRingHom)

/--
A08 specialization bridge: after the affine-scheme finite-morphism wrapper is
checked, reduced finite type coordinate rings inherit the same finite morphism
to affine space.  This is the repo-local affine-variety boundary until a
dedicated variety API is imported and checked.
-/
theorem affineSchemeStatementShape_to_affineVarietyCoordinateRingStatementShape :
    AffineSchemeStatementShape.{u} → AffineVarietyCoordinateRingStatementShape.{u} := by
  intro h k R _ _ _ _ _ _
  obtain ⟨s, g, hg_inj, hg_finite, _hSpec⟩ := h k R
  refine ⟨s, g, hg_inj, hg_finite, affineSpaceMorphismOfAlgHom g, ?_, ?_⟩
  · exact finite_affineSpaceMorphismOfAlgHom g hg_finite
  · exact affineSpaceMorphismOfAlgHom_comp_SpecIso_hom g

/--
Child-task wrapper for `S1-M-030-A08`: optional affine-variety wording is
checked only in the coordinate-ring sense supported by the current imports.
-/
theorem s1_m_030_a08_affineVariety_coordinateRing_specialization :
    AffineVarietyCoordinateRingStatementShape :=
  affineSchemeStatementShape_to_affineVarietyCoordinateRingStatementShape
    noetherNormalization_affineScheme_mathlib_wrapper

/-- Root Stage1 statement shape for this theorem slot. -/
def StatementShape : Prop :=
  AffineSchemeStatementShape.{u}

/-- Checked identity for audit tooling. -/
theorem statementShape_iff_affineSchemeStatementShape :
    StatementShape.{u} ↔ AffineSchemeStatementShape.{u} :=
  by
    change AffineSchemeStatementShape.{u} ↔ AffineSchemeStatementShape.{u}
    exact Iff.rfl

/--
Child-task decision for `S1-M-030-A05`: public Stage1 completion should use
the checked affine-Spec finite-morphism wrapper as the root boundary.  The
coordinate-ring wrappers are checked child nodes, not the terminal public
statement for this theorem slot.
-/
def s1_m_030_a05_publicCompletionDecision : List String := [
  "decision: public Stage1 completion requires the checked affine-Spec finite-morphism boundary",
  "first checked child: the coordinate-ring integral and finite wrappers are child nodes, not the terminal public statement",
  "A08 bridge: the coordinate-ring affine-variety specialization is checked locally; public affine-variety wording still needs serial integration"
]

/--
A05 checked boundary identity: the repo-local root statement is exactly the
affine-scheme finite-morphism statement shape.
-/
theorem s1_m_030_a05_completionBoundary_is_affineSchemeStatementShape :
    StatementShape.{u} ↔ AffineSchemeStatementShape.{u} :=
  statementShape_iff_affineSchemeStatementShape

/-- Human-readable package names for public backfill. -/
def commutativeAlgebraPackageAudit : List (String × String) := [
  ("S1-M-030-P01-polynomial-source",
    "Choose the source polynomial algebra MvPolynomial (Fin s) k."),
  ("S1-M-030-P02-integral-embedding",
    "Wrap exists_integral_inj_algHom_of_fg: injective map and integral target algebra."),
  ("S1-M-030-P03-finite-upgrade",
    "Use finite type over k to upgrade integral-over-polynomial to finite-over-polynomial."),
  ("S1-M-030-P04-affine-Spec",
    "Use IsFinite.SpecMap_iff to convert the finite algebra map to a finite morphism of affine schemes."),
  ("S1-M-030-P05-public-bridge",
    "Keep the classical affine-variety wording as a public statement bridge until integrator normalization.")
]

/-- Machine proof debt classification for this Stage1 slot. -/
def machineProofDebtClassification : List String := [
  "local_wrapper_upstream_mathlib: integral and finite affine algebraic Noether normalization are wrapped from Mathlib.RingTheory.NoetherNormalization",
  "local_proof_body: the finite-upgrade, affine-Spec package edge, and affine-space isomorphism transport are checked in this file",
  "formalization_debt: the source-language affine-variety-to-affine-space presentation still needs public statement normalization and proof-tree backfill",
  "not completed as a Stage1 theorem until public surface, external audit, and <=100 child-leaf ledgers are merged by the integrator"
]

/-- Public-documentation boundary for `S1-M-030-A09`. -/
def s1_m_030_a09_publicDocumentationBoundary : List String := [
  "mathlib proves the coordinate-ring Noether-normalization theorems exists_integral_inj_algHom_of_fg and exists_finite_inj_algHom_of_fg",
  "the repo-local wrapper proves only the statement shapes imported and checked in this Lean file",
  "the checked local geometric boundary is the affine-Spec finite-morphism wrapper plus the affine-space isomorphism transport",
  "classical affine-variety wording is represented only by the checked coordinate-ring specialization until a public integrator normalizes the statement",
  "public completion must wait for serial documentation backfill, validation evidence, external-audit handling, and the no anchor-only integration-debt gate"
]

/-- Public status-synchronization gate for `S1-M-030-A10`. -/
def s1_m_030_a10_statusSynchronizationGate : List String := [
  "A10 is public-doc integration work, not a new proof obligation",
  "the wrapper build validation is repo-local and must be cited before any public checklist update",
  "the public merge target is the authoritative Stage1 blueprint or todo surface, not a private child ledger",
  "this child cannot mark the public checklist completed because shared public docs are outside its write scope",
  "parent completion remains blocked until A11 external-audit handling and A12 no-residual-integration-debt synchronization are explicit"
]

/-- External-audit result for `S1-M-030-A11` in this worker environment. -/
def s1_m_030_a11_externalSearchAudit : List String := [
  "2026-05-01: gh auth status reports no logged-in GitHub hosts, so authenticated GitHub code search was not available in this worker",
  "unauthenticated GitHub REST code search for exists_finite_inj_algHom_of_fg and NoetherNormalization returned 401 Requires authentication",
  "unauthenticated GitHub repository search for Lean NoetherNormalization and Noether-normalization Lean-4 phrases returned total_count 0",
  "repo-local dependency grep found the NoetherNormalization theorem family only in the pinned mathlib package",
  "the current Lake closure pins mathlib and flt-regular, and contains no non-mathlib Lean 4 algebraic-geometry Noether-normalization dependency",
  "A11 consequence: no stronger non-mathlib scheme wrapper was integrated or left as completed anchor-only evidence in this pass"
]

/--
Integration blocker for `S1-M-030-A11`: the required authenticated external code
search could not be completed from this worker because no GitHub credentials are
available.  Any later positive result must be pinned/imported/checked or kept as
a concrete blocker before public completion.
-/
def s1_m_030_a11_externalWrapperIntegrationBlocker : List String := [
  "blocker: authenticated GitHub code search is unavailable until gh auth login or an equivalent token-backed search is configured",
  "follow-up search terms: NoetherNormalization, Noether normalization, exists_integral_inj_algHom_of_fg, exists_finite_inj_algHom_of_fg, AffineSpace.SpecIso, IsFinite.SpecMap_iff",
  "required positive-result handling: record repository URL, commit, module path, theorem names, Lean/Lake versions, license, and mathlib compatibility",
  "required integration handling: pin as a Lake dependency or vendor the proof body, add a repo-local wrapper theorem, and run lake env lean on the wrapper",
  "if dependency, license, or API incompatibility prevents integration, keep the Stage1 slot open with that concrete blocker; do not mark anchor-only evidence completed"
]

/-- Repo-local integration-debt gate for this Stage1 slot. -/
def repoLocalIntegrationDebtGate : List String := [
  "no anchor-only completed state is used",
  "the relevant Lean proof is in the pinned mathlib dependency and is checked through this local wrapper",
  "A11 has no completed external-anchor claim; authenticated external search remains blocked by missing GitHub authentication in this worker",
  "any later external Lean proof claim must be pin/import/check or recorded as an explicit integration blocker before completion"
]

/-- Child-task gate for `S1-M-030-A12`. -/
def s1_m_030_a12_publicCompletionNoIntegrationDebtGate : List String := [
  "A12 is a completion-surface gate, not a new mathematical proof leaf",
  "public completion must not cite external_upstream_anchor_only evidence as completed",
  "the current repo-local closed machine content is local_wrapper_upstream_mathlib plus local_proof_body bridge code",
  "the classical affine-variety wording and any unmerged public statement normalization remain formalization_debt",
  "because authenticated external search is still blocked in A11, the parent Stage1 item must remain open until that blocker is resolved or accepted as an explicit integration blocker",
  "a completed public state is allowed only after the blueprint/todo text says that no repo_local_integration_debt remains"
]

/-- mathlib modules and theorem names used by this local wrapper. -/
def mathlibAnchorAudit : List String := [
  "Mathlib.RingTheory.NoetherNormalization.exists_integral_inj_algHom_of_fg",
  "Mathlib.RingTheory.NoetherNormalization.exists_finite_inj_algHom_of_fg",
  "Mathlib.AlgebraicGeometry.Morphisms.Finite.AlgebraicGeometry.IsFinite.SpecMap_iff",
  "Mathlib.CategoryTheory.MorphismProperty.RespectsIso.postcomp",
  "Mathlib.AlgebraicGeometry.Morphisms.Finite.AlgebraicGeometry.IsFinite"
]

/-! ## Audit probes -/

#check exists_integral_inj_algHom_of_fg
#check exists_finite_inj_algHom_of_fg
#check AlgebraicGeometry.IsFinite.SpecMap_iff
#check noetherNormalization_integral_mathlib_wrapper
#check s1_m_030_a02_exists_integral_inj_algHom_of_fg_ring_wrapper
#check integralStatementShape_to_algebraicStatementShape
#check noetherNormalization_algebraic_mathlib_wrapper
#check s1_m_030_a03_exists_finite_inj_algHom_of_fg_ring_wrapper
#check affineSpaceMorphismOfAlgHom
#check affineSpaceMorphismOfAlgHom_comp_SpecIso_hom
#check finite_affineSpaceMorphismOfAlgHom
#check s1_m_030_a06_affineSpaceMorphism_from_finite_algHom
#check AffineSpaceFiniteMorphismStatementShape
#check s1_m_030_a07_affineSpaceMorphism_isFinite
#check algebraicStatementShape_to_affineSchemeStatementShape
#check noetherNormalization_affineScheme_mathlib_wrapper
#check AffineVarietyCoordinateRingStatementShape
#check affineSchemeStatementShape_to_affineVarietyCoordinateRingStatementShape
#check s1_m_030_a08_affineVariety_coordinateRing_specialization
#check s1_m_030_a05_publicCompletionDecision
#check s1_m_030_a05_completionBoundary_is_affineSchemeStatementShape
#check s1_m_030_a09_publicDocumentationBoundary
#check s1_m_030_a10_statusSynchronizationGate
#check s1_m_030_a11_externalSearchAudit
#check s1_m_030_a11_externalWrapperIntegrationBlocker
#check s1_m_030_a12_publicCompletionNoIntegrationDebtGate

end S1_M_030
end Stage1
end AwesomeTheorems
