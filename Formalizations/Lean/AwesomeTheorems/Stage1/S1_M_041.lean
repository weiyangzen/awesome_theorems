import Mathlib.AlgebraicGeometry.Morphisms.Proper
import Mathlib.AlgebraicGeometry.Morphisms.Smooth
import Mathlib.AlgebraicGeometry.Geometrically.Integral
import Mathlib.CategoryTheory.Comma.Over.Basic
import Mathlib.NumberTheory.NumberField.Basic

/-!
# S1-M-041 / THM-M-0122: Faltings' theorem, Stage1 statement shape

This file deliberately does not claim a proof of Faltings' theorem.  It records
the Lean 4 boundary for Mordell's conjecture in terms of mathlib objects that
are currently available locally: number fields, schemes, K-rational points,
smooth morphisms, proper morphisms, and finite sets.

The predicate carrying "is a curve" is pinned to the strongest local mathlib
interface found in this repository: smooth of relative dimension one, proper,
and geometrically integral.  The local pin does not yet expose a selected
projective morphism predicate, geometrically connected curve predicate, or
geometric genus API for smooth projective curves, so genus is represented by a
checked Stage1 numeric slot rather than by the final imported invariant.

The rational-point interface is checked in two compatible forms: the concrete
section structure `KRationalPoint`, and the slice-category morphism
`OverSpecKRationalPoint`.  A small bridge interface also records the exact
conversion laws any later functor-of-points API must supply before it can
replace the section model without changing the finiteness statement.
-/

noncomputable section

open CategoryTheory AlgebraicGeometry

universe u

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_041

/-- A `K`-rational point of a scheme `X` over `Spec K`, written as a section of
the structure morphism. -/
structure KRationalPoint (K : Type u) [Field K]
    (X : Scheme.{u}) (structureMap : X ⟶ Spec (CommRingCat.of K)) where
  toSpecMap : Spec (CommRingCat.of K) ⟶ X
  over_base : toSpecMap ≫ structureMap = 𝟙 (Spec (CommRingCat.of K))

/-- The slice-category encoding of a `K`-rational point of `X` over
`Spec K`: a morphism over `Spec K` from the identity object to the structure
morphism. -/
abbrev OverSpecKRationalPoint (K : Type u) [Field K]
    (X : Scheme.{u}) (structureMap : X ⟶ Spec (CommRingCat.of K)) : Type u :=
  Over.mk (𝟙 (Spec (CommRingCat.of K))) ⟶ Over.mk structureMap

namespace KRationalPoint

/-- Projection lemma for the section equation carried by `KRationalPoint`. -/
theorem comp_structureMap {K : Type u} [Field K] {X : Scheme.{u}}
    {structureMap : X ⟶ Spec (CommRingCat.of K)}
    (p : KRationalPoint K X structureMap) :
    p.toSpecMap ≫ structureMap = 𝟙 (Spec (CommRingCat.of K)) :=
  p.over_base

/-- Equivalence between the local section model and the slice-category model of
`K`-rational points over `Spec K`. -/
def equivOverSpecKRationalPoint {K : Type u} [Field K] {X : Scheme.{u}}
    {structureMap : X ⟶ Spec (CommRingCat.of K)} :
    KRationalPoint K X structureMap ≃ OverSpecKRationalPoint K X structureMap where
  toFun p := Over.homMk p.toSpecMap p.over_base
  invFun p := ⟨p.left, by simpa using Over.w p⟩
  left_inv p := by
    cases p
    rfl
  right_inv p := by
    ext
    rfl

@[simp]
theorem equivOverSpecKRationalPoint_apply_left {K : Type u} [Field K] {X : Scheme.{u}}
    {structureMap : X ⟶ Spec (CommRingCat.of K)}
    (p : KRationalPoint K X structureMap) :
    (equivOverSpecKRationalPoint (structureMap := structureMap) p).left = p.toSpecMap :=
  rfl

@[simp]
theorem equivOverSpecKRationalPoint_symm_toSpecMap {K : Type u} [Field K] {X : Scheme.{u}}
    {structureMap : X ⟶ Spec (CommRingCat.of K)}
    (p : OverSpecKRationalPoint K X structureMap) :
    ((equivOverSpecKRationalPoint (structureMap := structureMap)).symm p).toSpecMap = p.left :=
  rfl

end KRationalPoint

/-- Minimal conversion contract for any later rational-point API, including a
functor-of-points representation, to be interchangeable with the section model
used by this Stage1 artifact. -/
structure RationalPointAPIBridge (K : Type u) [Field K]
    (X : Scheme.{u}) (structureMap : X ⟶ Spec (CommRingCat.of K)) where
  pointType : Type u
  toSection : pointType → KRationalPoint K X structureMap
  ofSection : KRationalPoint K X structureMap → pointType
  toSection_ofSection : ∀ p, toSection (ofSection p) = p
  ofSection_toSection : ∀ q, ofSection (toSection q) = q

namespace RationalPointAPIBridge

/-- The exact equivalence certified by a rational-point API bridge. -/
def sectionEquiv {K : Type u} [Field K] {X : Scheme.{u}}
    {structureMap : X ⟶ Spec (CommRingCat.of K)}
    (B : RationalPointAPIBridge K X structureMap) :
    KRationalPoint K X structureMap ≃ B.pointType where
  toFun := B.ofSection
  invFun := B.toSection
  left_inv := B.toSection_ofSection
  right_inv := B.ofSection_toSection

/-- Finiteness of rational points is invariant under a certified API bridge. -/
theorem section_univ_finite_iff_pointType_univ_finite {K : Type u} [Field K]
    {X : Scheme.{u}} {structureMap : X ⟶ Spec (CommRingCat.of K)}
    (B : RationalPointAPIBridge K X structureMap) :
    (Set.univ : Set (KRationalPoint K X structureMap)).Finite ↔
      (Set.univ : Set B.pointType).Finite := by
  constructor
  · intro h
    have himage :
        ((sectionEquiv B) '' (Set.univ : Set (KRationalPoint K X structureMap))).Finite :=
      h.image (sectionEquiv B)
    simpa using himage
  · intro h
    have himage :
        (((sectionEquiv B).symm) '' (Set.univ : Set B.pointType)).Finite :=
      h.image (sectionEquiv B).symm
    simpa using himage

end RationalPointAPIBridge

/-- The checked slice-category rational-point API is a certified bridge for the
section-based `KRationalPoint` model. -/
def overSpecKRationalPointAPIBridge (K : Type u) [Field K]
    (X : Scheme.{u}) (structureMap : X ⟶ Spec (CommRingCat.of K)) :
    RationalPointAPIBridge K X structureMap where
  pointType := OverSpecKRationalPoint K X structureMap
  toSection := (KRationalPoint.equivOverSpecKRationalPoint (structureMap := structureMap)).symm
  ofSection := KRationalPoint.equivOverSpecKRationalPoint (structureMap := structureMap)
  toSection_ofSection := by
    intro p
    simp
  ofSection_toSection := by
    intro p
    simp

/-- Concrete Stage1 replacement for the former opaque `curve_condition` slot.

This is intentionally named as a Stage1 predicate rather than as a final
definition of "smooth projective geometrically connected curve": this local
mathlib pin supplies `SmoothOfRelativeDimension 1`, `IsProper`, and
`GeometricallyIntegral`, but no selected scheme-morphism API for projectivity or
geometric connectedness. -/
def Stage1CurveCondition {K : Type u} [Field K]
    {X : Scheme.{u}} (structureMap : X ⟶ Spec (CommRingCat.of K)) : Prop :=
  SmoothOfRelativeDimension 1 structureMap ∧
    IsProper structureMap ∧
    GeometricallyIntegral structureMap

/-- Stage1 fallback carrier for the geometric genus until a native smooth
proper curve genus API is selected and imported. -/
abbrev GeometricGenusSlot : Type :=
  ℕ

/-- Stage1 spelling of the Faltings genus hypothesis as `g > 1`. -/
def GenusGreaterThanOne (g : GeometricGenusSlot) : Prop :=
  1 < g

/-- Equivalent Stage1 spelling of the Faltings genus hypothesis as `g >= 2`. -/
def GenusAtLeastTwo (g : GeometricGenusSlot) : Prop :=
  2 ≤ g

/-- The numeric genus normalization used by the local Faltings statement shape:
for natural-valued genus data, `g > 1` and `g >= 2` are definitionally the same
boundary. -/
lemma genusGreaterThanOne_iff_genusAtLeastTwo (g : GeometricGenusSlot) :
    GenusGreaterThanOne g ↔ GenusAtLeastTwo g := by
  rfl

/-- Boundary data for the class of curves appearing in Faltings' theorem.

The `curve_condition` field is a concrete Stage1 predicate, not an opaque
placeholder.  The `geometricGenus` field is a numeric Stage1 fallback slot:
it records the intended geometric genus value only after the smooth/proper curve
genus API is selected. -/
structure FaltingsCurveData (K : Type u) [Field K] [NumberField K] where
  X : Scheme.{u}
  structureMap : X ⟶ Spec (CommRingCat.of K)
  curve_condition : Stage1CurveCondition structureMap
  geometricGenus : GeometricGenusSlot
  genus_gt_one : GenusGreaterThanOne geometricGenus

/-- Smoothness follows from the concrete Stage1 curve predicate. -/
lemma FaltingsCurveData.smooth {K : Type u} [Field K] [NumberField K]
    (C : FaltingsCurveData K) : Smooth C.structureMap := by
  letI : SmoothOfRelativeDimension 1 C.structureMap := C.curve_condition.1
  exact SmoothOfRelativeDimension.smooth 1 C.structureMap

/-- Properness is one component of the concrete Stage1 curve predicate. -/
lemma FaltingsCurveData.proper {K : Type u} [Field K] [NumberField K]
    (C : FaltingsCurveData K) : IsProper C.structureMap :=
  C.curve_condition.2.1

/-- Geometric integrality is the available local substitute for the intended
geometric connectedness/non-singular curve irreducibility package. -/
lemma FaltingsCurveData.geometricallyIntegral {K : Type u} [Field K] [NumberField K]
    (C : FaltingsCurveData K) : GeometricallyIntegral C.structureMap :=
  C.curve_condition.2.2

/-- The stored Stage1 genus hypothesis in its `g > 1` spelling. -/
lemma FaltingsCurveData.genusGreaterThanOne {K : Type u} [Field K] [NumberField K]
    (C : FaltingsCurveData K) : GenusGreaterThanOne C.geometricGenus :=
  C.genus_gt_one

/-- The stored Stage1 genus hypothesis normalized to the `g >= 2` spelling. -/
lemma FaltingsCurveData.genusAtLeastTwo {K : Type u} [Field K] [NumberField K]
    (C : FaltingsCurveData K) : GenusAtLeastTwo C.geometricGenus :=
  (genusGreaterThanOne_iff_genusAtLeastTwo C.geometricGenus).mp C.genus_gt_one

/-- The set of `K`-rational points of a Stage1 Faltings curve datum. -/
def RationalPoints {K : Type u} [Field K] [NumberField K]
    (C : FaltingsCurveData K) : Set (KRationalPoint K C.X C.structureMap) :=
  Set.univ

/-- Stage1 normalized statement shape for Faltings' theorem / Mordell's
conjecture: a smooth proper curve of genus at least two over a number field has
finitely many rational points.

This is a statement-shape artifact only.  The proof body is not present in
mathlib at the pinned revision audited by the worker ledger. -/
def StatementShape : Prop :=
  ∀ (K : Type u) [Field K] [NumberField K] (C : FaltingsCurveData K),
    (RationalPoints C).Finite

/-- The mathlib revision requested for this Stage1 anchor audit. -/
def auditedMathlibRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- Structured public-backfill row for audited mathlib anchors. -/
structure MathlibAnchorRow where
  requested : String
  moduleName : String
  checkedDeclaration : String
  repoLocalStatus : String
  note : String

/--
Mathlib anchor table prepared for the public `S1-M-041 / THM-M-0122` backfill.

The rows are metadata for the public blueprint/todo surface.  The declarations
listed in `checkedDeclaration` are also probed below with `#check` in this
repository's pinned mathlib closure.
-/
def mathlibAnchorTable : List MathlibAnchorRow := [
  {
    requested := "NumberField"
    moduleName := "Mathlib.NumberTheory.NumberField.Basic"
    checkedDeclaration := "NumberField"
    repoLocalStatus := "checked"
    note := "Number-field typeclass used to quantify over the base field `K`."
  },
  {
    requested := "Scheme"
    moduleName := "Mathlib.AlgebraicGeometry.Scheme"
    checkedDeclaration := "AlgebraicGeometry.Scheme"
    repoLocalStatus := "checked"
    note := "Core scheme object used for the curve datum `X`."
  },
  {
    requested := "Spec"
    moduleName := "Mathlib.AlgebraicGeometry.Scheme"
    checkedDeclaration := "AlgebraicGeometry.Scheme.Spec"
    repoLocalStatus := "checked"
    note := "Affine scheme constructor used for the base `Spec K`."
  },
  {
    requested := "Over category rational-point encoding"
    moduleName := "Mathlib.CategoryTheory.Comma.Over.Basic"
    checkedDeclaration := "CategoryTheory.Over"
    repoLocalStatus := "checked"
    note := "`OverSpecKRationalPoint` and `KRationalPoint.equivOverSpecKRationalPoint` identify section-based rational points with morphisms in the slice category over `Spec K`."
  },
  {
    requested := "SmoothOfRelativeDimension 1"
    moduleName := "Mathlib.AlgebraicGeometry.Morphisms.Smooth"
    checkedDeclaration := "AlgebraicGeometry.SmoothOfRelativeDimension"
    repoLocalStatus := "checked"
    note := "Concrete relative-dimension-one smoothness predicate used by `Stage1CurveCondition`."
  },
  {
    requested := "Smooth"
    moduleName := "Mathlib.AlgebraicGeometry.Morphisms.Smooth"
    checkedDeclaration := "AlgebraicGeometry.Smooth"
    repoLocalStatus := "checked"
    note := "Smoothness follows from the relative-dimension-one component of `Stage1CurveCondition`."
  },
  {
    requested := "IsProper"
    moduleName := "Mathlib.AlgebraicGeometry.Morphisms.Proper"
    checkedDeclaration := "AlgebraicGeometry.IsProper"
    repoLocalStatus := "checked"
    note := "Properness predicate used on the structure morphism."
  },
  {
    requested := "Set.Finite"
    moduleName := "Mathlib.Data.Set.Finite.Basic"
    checkedDeclaration := "Set.Finite"
    repoLocalStatus := "checked"
    note := "Finite-set predicate used for the set of `K`-rational points."
  },
  {
    requested := "GeometricallyIntegral"
    moduleName := "Mathlib.AlgebraicGeometry.Geometrically.Integral"
    checkedDeclaration := "AlgebraicGeometry.GeometricallyIntegral"
    repoLocalStatus := "checked"
    note := "Available local geometrically integral predicate used by `Stage1CurveCondition`; geometric connectedness remains unselected locally."
  },
  {
    requested := "Projective morphism predicate"
    moduleName := "not selected"
    checkedDeclaration := "none"
    repoLocalStatus := "integration_blocker"
    note := "No scheme-morphism `IsProjective`/projective predicate was found in the local mathlib surface during this child pass."
  },
  {
    requested := "Geometric genus for smooth proper curves"
    moduleName := "not selected"
    checkedDeclaration := "none"
    repoLocalStatus := "integration_blocker"
    note := "No native smooth proper curve geometric genus API was found in the local mathlib surface during this child pass; `GeometricGenusSlot` is only a checked Stage1 numeric fallback."
  }
]

/-- Public search terms reserved for the external Lean 4 source audit. -/
def externalLeanSearchTerms : List String := [
  "Faltings",
  "Mordell",
  "MordellConjecture",
  "FaltingsTheorem",
  "genus at least two",
  "rational points NumberField"
]

/-- Date of the child external-source audit, using an absolute date for traceability. -/
def externalLeanSourceAuditDate : String :=
  "2026-05-01"

/--
Authenticated GitHub code-search status for the external Lean 4 source audit.

The local `gh` client had no authenticated GitHub host and no API token was
available in the environment.  GitHub REST code search also returned HTTP 401
for an unauthenticated `Faltings language:Lean` probe, so this child cannot
certify that authenticated code search was completed.
-/
def githubAuthenticatedCodeSearchStatus : String :=
  "blocked: gh auth status reports no login; GitHub code search API returned HTTP 401 Requires authentication"

/-- Fallback public GitHub/API and local-source probes run after authentication was blocked. -/
def externalLeanFallbackAuditResults : List String := [
  "leanprover-community/mathlib4@8a178386ffc0f5fef0b77738bb5449d50efeea95: local rg found docs/1000.yaml titles for Faltings's theorem, Mordell-Weil theorem, and Chowla-Mordell theorem, plus Mathlib.GroupTheory.Descent comments about Mordell-Weil; no terminal Faltings/Mordell theorem or module was found",
  "GitHub repository API query \"Faltings theorem\" Lean: total_count=0 incomplete_results=false",
  "GitHub repository API query \"Mordell conjecture\" Lean: total_count=0 incomplete_results=false",
  "GitHub repository API query Faltings Lean: total_count=0 incomplete_results=false",
  "GitHub repository API query FaltingsTheorem Lean: total_count=0 incomplete_results=false",
  "GitHub repository API query MordellConjecture Lean: total_count=0 incomplete_results=false",
  "GitHub repository API query \"genus at least two\" Lean: total_count=0 incomplete_results=false",
  "GitHub repository API query \"rational points\" NumberField Lean: total_count=0 incomplete_results=false",
  "GitHub repository API query Mordell Lean4: found AEjonanonymous/Non-existence-of-Perfect-Cuboids@36fdfb8c662467a5c97413899a60ee675ba90f36, module No Perfect Cuboids.lean, theorem names parity_wall_consistency/perfection_locus_empty/no_perfect_cuboid_final; this is not a Mordell-conjecture or Faltings terminal proof",
  "General web search for Lean 4 Faltings theorem formalization / Lean 4 Mordell conjecture formalization did not identify a public Lean 4 terminal proof source"
]

/-- Exact external Lean 4 terminal proof anchors found by this child audit. -/
def externalLeanTerminalProofAnchors : List String := []

/--
Whether this child found a public external Lean 4 terminal proof of Faltings'
theorem / the Mordell conjecture.
-/
def externalLeanTerminalProofFound : Bool :=
  false

theorem externalLeanTerminalProofFound_eq_false :
    externalLeanTerminalProofFound = false :=
  rfl

/-- Repo-local machine-proof closure states allowed by the M0387-level gate. -/
inductive RepoLocalClosureGate where
  | localProofBody
  | localWrapperUpstreamMathlib
  | externalUpstreamPinned
  | notRepoLocalClosed
  deriving DecidableEq, Repr

/--
Current closure gate for `THM-M-0122`.

This value is intentionally `notRepoLocalClosed`: the file contains a checked
statement shape, anchor metadata, and interface bridges, but no local proof
body, mathlib theorem wrapper, or pinned external dependency proving Faltings'
theorem through Lake.
-/
def currentRepoLocalClosureGate : RepoLocalClosureGate :=
  RepoLocalClosureGate.notRepoLocalClosed

theorem currentRepoLocalClosureGate_eq_notRepoLocalClosed :
    currentRepoLocalClosureGate = RepoLocalClosureGate.notRepoLocalClosed :=
  rfl

end S1_M_041
end Stage1
end AwesomeTheorems

-- Audit probes for the local mathlib interfaces used above.
#check NumberField
#check Scheme
#check Spec
#check CategoryTheory.Over
#check CategoryTheory.Over.mk
#check CategoryTheory.Over.homMk
#check AlgebraicGeometry.Smooth
#check AlgebraicGeometry.SmoothOfRelativeDimension
#check AlgebraicGeometry.IsProper
#check AlgebraicGeometry.GeometricallyIntegral
#check Set.Finite
#check AwesomeTheorems.Stage1.S1_M_041.KRationalPoint
#check AwesomeTheorems.Stage1.S1_M_041.OverSpecKRationalPoint
#check AwesomeTheorems.Stage1.S1_M_041.KRationalPoint.comp_structureMap
#check AwesomeTheorems.Stage1.S1_M_041.KRationalPoint.equivOverSpecKRationalPoint
#check AwesomeTheorems.Stage1.S1_M_041.KRationalPoint.equivOverSpecKRationalPoint_apply_left
#check AwesomeTheorems.Stage1.S1_M_041.KRationalPoint.equivOverSpecKRationalPoint_symm_toSpecMap
#check AwesomeTheorems.Stage1.S1_M_041.RationalPointAPIBridge
#check AwesomeTheorems.Stage1.S1_M_041.RationalPointAPIBridge.sectionEquiv
#check AwesomeTheorems.Stage1.S1_M_041.RationalPointAPIBridge.section_univ_finite_iff_pointType_univ_finite
#check AwesomeTheorems.Stage1.S1_M_041.overSpecKRationalPointAPIBridge
#check AwesomeTheorems.Stage1.S1_M_041.Stage1CurveCondition
#check AwesomeTheorems.Stage1.S1_M_041.GeometricGenusSlot
#check AwesomeTheorems.Stage1.S1_M_041.GenusGreaterThanOne
#check AwesomeTheorems.Stage1.S1_M_041.GenusAtLeastTwo
#check AwesomeTheorems.Stage1.S1_M_041.genusGreaterThanOne_iff_genusAtLeastTwo
#check AwesomeTheorems.Stage1.S1_M_041.FaltingsCurveData.genusGreaterThanOne
#check AwesomeTheorems.Stage1.S1_M_041.FaltingsCurveData.genusAtLeastTwo
#check AwesomeTheorems.Stage1.S1_M_041.auditedMathlibRevision
#check AwesomeTheorems.Stage1.S1_M_041.mathlibAnchorTable
#check AwesomeTheorems.Stage1.S1_M_041.externalLeanSearchTerms
#check AwesomeTheorems.Stage1.S1_M_041.externalLeanSourceAuditDate
#check AwesomeTheorems.Stage1.S1_M_041.githubAuthenticatedCodeSearchStatus
#check AwesomeTheorems.Stage1.S1_M_041.externalLeanFallbackAuditResults
#check AwesomeTheorems.Stage1.S1_M_041.externalLeanTerminalProofAnchors
#check AwesomeTheorems.Stage1.S1_M_041.externalLeanTerminalProofFound
#check AwesomeTheorems.Stage1.S1_M_041.externalLeanTerminalProofFound_eq_false
#check AwesomeTheorems.Stage1.S1_M_041.RepoLocalClosureGate
#check AwesomeTheorems.Stage1.S1_M_041.currentRepoLocalClosureGate
#check AwesomeTheorems.Stage1.S1_M_041.currentRepoLocalClosureGate_eq_notRepoLocalClosed
#check AwesomeTheorems.Stage1.S1_M_041.StatementShape
