import Mathlib.Algebra.Homology.SpectralSequence.Basic
import Mathlib.Algebra.Homology.SpectralObject.SpectralSequence
import Mathlib.AlgebraicTopology.SingularHomology.HomotopyInvarianceTopCat

/-!
# S1-M-106 / THM-M-0554: Atiyah-Hirzebruch spectral sequence

This Stage1 file records a conservative Lean statement-shape boundary for the
Atiyah-Hirzebruch spectral sequence.  The pinned mathlib snapshot contains a
general category-theoretic `SpectralSequence` API, first-quadrant/cohomological
specializations, `TopCat`, singular homology, and homotopy invariance of singular
homology.  It does not provide a terminal generalized cohomology theory API with
cellular filtrations and AHSS convergence.

The declarations below therefore avoid proof placeholders and false completion
claims.  They define the data a future proof or pinned dependency must supply,
plus small wrappers around existing mathlib spectral-sequence and singular
homology facts.
-/

noncomputable section

universe uC vC uι vι w

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_106

open CategoryTheory AlgebraicTopology

/-- The generic mathlib spectral-sequence object anchored for this slot. -/
abbrev MathlibSpectralSequence
    (C : Type uC) [Category.{vC} C] [Abelian C]
    {κ : Type uι} (c : ℤ → ComplexShape κ) (r₀ : ℤ) :=
  CategoryTheory.SpectralSequence C c r₀

/-- The cohomological `E₂` spectral-sequence object currently available in mathlib. -/
abbrev MathlibE2CohomologicalSpectralSequence
    (C : Type uC) [Category.{vC} C] [Abelian C] :
    Type (max uC vC) :=
  CategoryTheory.E₂CohomologicalSpectralSequence C

/-- The object at bidegree `(p, q)` on the `E₂` page of a mathlib cohomological spectral sequence. -/
abbrev E2PageObject
    {C : Type uC} [Category.{vC} C] [Abelian C]
    (S : MathlibE2CohomologicalSpectralSequence C) (p q : ℤ) : C :=
  (S.page 2).X (p, q)

/-- The `E₂` page object wrapper is definitionally the object on page `2`. -/
theorem e2PageObject_def
    {C : Type uC} [Category.{vC} C] [Abelian C]
    (S : MathlibE2CohomologicalSpectralSequence C) (p q : ℤ) :
    E2PageObject S p q = (S.page 2).X (p, q) :=
  rfl

/-- The abelian-category spectral-object API available in mathlib. -/
abbrev MathlibSpectralObject
    (C : Type uC) [Category.{vC} C] [Abelian C]
    (ι : Type uι) [Category.{vι} ι] :=
  CategoryTheory.Abelian.SpectralObject C ι

/--
Local exactness package for one three-term segment of a generalized-cohomology
long exact sequence.

The field `exactAtMiddle` is intentionally proposition-valued: this Stage1
artifact records the typed boundary a future proof must fill, without inventing
an AHSS-specific exactness API that mathlib does not yet provide.
-/
structure CohomologyExactnessWitness
    (C : Type uC) [Category.{vC} C] [Abelian C] : Type (max uC vC) where
  left : C
  middle : C
  right : C
  leftToMiddle : left ⟶ middle
  middleToRight : middle ⟶ right
  complexCondition : leftToMiddle ≫ middleToRight = 0
  exactAtMiddle : Prop

/--
Minimal interface for a generalized cohomology theory valued in an abelian
category.  This is not a complete Eilenberg-Steenrod formalization; it is a
typed placeholder for the contravariant functors, coefficient objects,
suspension shift, homotopy invariance, and exactness data that an AHSS proof
must later instantiate or import.
-/
structure GeneralizedCohomologyTheorySkeleton
    (C : Type uC) [Category.{vC} C] [Abelian C] : Type (max uC vC (w + 1)) where
  cohomology : ℤ → TopCat.{w}ᵒᵖ ⥤ C
  coefficient : ℤ → C
  coefficientSpace : TopCat.{w}
  coefficientSpaceIsPoint : Prop
  coefficientIso :
    ∀ n : ℤ, coefficient n ≅ (cohomology n).obj (Opposite.op coefficientSpace)
  suspension : TopCat.{w} → TopCat.{w}
  suspensionShiftIso :
    ∀ (n : ℤ) (X : TopCat.{w}),
      (cohomology (n + 1)).obj (Opposite.op (suspension X)) ≅
        (cohomology n).obj (Opposite.op X)
  homotopyInvariant :
    ∀ (n : ℤ) {X Y : TopCat.{w}} {f g : X ⟶ Y},
      TopCat.Homotopy f g →
        (cohomology n).map f.op = (cohomology n).map g.op
  exactness :
    ∀ (_ : ℤ) {A X : TopCat.{w}} (_ : A ⟶ X),
      CohomologyExactnessWitness C
  wedgeAxiomOrRepresentability : Prop

/-- Coefficient objects are identified with cohomology of the chosen coefficient space. -/
def GeneralizedCohomologyTheorySkeleton.coefficientAsCohomology
    {C : Type uC} [Category.{vC} C] [Abelian C]
    (E : GeneralizedCohomologyTheorySkeleton.{uC, vC, w} C) (n : ℤ) :
    E.coefficient n ≅ (E.cohomology n).obj (Opposite.op E.coefficientSpace) :=
  E.coefficientIso n

/-- The suspension shift isomorphism carried by the local generalized-cohomology interface. -/
def GeneralizedCohomologyTheorySkeleton.suspensionShift
    {C : Type uC} [Category.{vC} C] [Abelian C]
    (E : GeneralizedCohomologyTheorySkeleton.{uC, vC, w} C) (n : ℤ) (X : TopCat.{w}) :
    (E.cohomology (n + 1)).obj (Opposite.op (E.suspension X)) ≅
      (E.cohomology n).obj (Opposite.op X) :=
  E.suspensionShiftIso n X

/-- Homotopic maps induce equal generalized-cohomology maps in this interface. -/
theorem GeneralizedCohomologyTheorySkeleton.map_eq_of_homotopy
    {C : Type uC} [Category.{vC} C] [Abelian C]
    (E : GeneralizedCohomologyTheorySkeleton.{uC, vC, w} C)
    (n : ℤ) {X Y : TopCat.{w}} {f g : X ⟶ Y}
    (H : TopCat.Homotopy f g) :
    (E.cohomology n).map f.op = (E.cohomology n).map g.op :=
  E.homotopyInvariant n H

/-- The exactness witness carried by the local generalized-cohomology interface. -/
def GeneralizedCohomologyTheorySkeleton.exactnessWitness
    {C : Type uC} [Category.{vC} C] [Abelian C]
    (E : GeneralizedCohomologyTheorySkeleton.{uC, vC, w} C)
    (n : ℤ) {A X : TopCat.{w}} (i : A ⟶ X) :
    CohomologyExactnessWitness C :=
  E.exactness n i

/-- Each exactness witness carries the expected complex condition. -/
theorem CohomologyExactnessWitness.leftToMiddle_comp_middleToRight
    {C : Type uC} [Category.{vC} C] [Abelian C]
    (W : CohomologyExactnessWitness C) :
    W.leftToMiddle ≫ W.middleToRight = 0 :=
  W.complexCondition

/-- The exactness witness supplied by a generalized-cohomology skeleton is a complex. -/
theorem GeneralizedCohomologyTheorySkeleton.exactnessWitness_complex
    {C : Type uC} [Category.{vC} C] [Abelian C]
    (E : GeneralizedCohomologyTheorySkeleton.{uC, vC, w} C)
    (n : ℤ) {A X : TopCat.{w}} (i : A ⟶ X) :
    (E.exactnessWitness n i).leftToMiddle ≫
        (E.exactnessWitness n i).middleToRight = 0 :=
  (E.exactnessWitness n i).complexCondition

/-- Completion gate for the P3 generalized-cohomology interface selection. -/
structure GeneralizedCohomologyTheoryInterfaceGate where
  contravariantFunctorTyped : Bool
  coefficientObjectsTyped : Bool
  suspensionShiftTyped : Bool
  homotopyInvarianceTyped : Bool
  exactnessWitnessTyped : Bool
  concreteExternalTheoryImported : Bool
  terminalAHSSConstructionClosed : Bool
  completedStateRetainsRepoLocalIntegrationDebt : Bool
  parentCompletionAllowed : Bool
  debtClass : String
  validationCommand : String

/--
P3 gate: the generalized-cohomology interface is a checked repo-local skeleton,
not an imported terminal AHSS or generalized-cohomology formalization.
-/
def generalizedCohomologyTheoryInterfaceGate :
    GeneralizedCohomologyTheoryInterfaceGate where
  contravariantFunctorTyped := true
  coefficientObjectsTyped := true
  suspensionShiftTyped := true
  homotopyInvarianceTyped := true
  exactnessWitnessTyped := true
  concreteExternalTheoryImported := false
  terminalAHSSConstructionClosed := false
  completedStateRetainsRepoLocalIntegrationDebt := false
  parentCompletionAllowed := false
  debtClass := "formalization_debt"
  validationCommand := "cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_106.lean"

/-- P3 gate: the contravariant `TopCatᵒᵖ` cohomology functor family is typed. -/
theorem generalizedCohomologyTheoryInterfaceGate_contravariantFunctorTyped :
    generalizedCohomologyTheoryInterfaceGate.contravariantFunctorTyped = true :=
  rfl

/-- P3 gate: coefficient objects and their comparison isomorphisms are typed. -/
theorem generalizedCohomologyTheoryInterfaceGate_coefficientObjectsTyped :
    generalizedCohomologyTheoryInterfaceGate.coefficientObjectsTyped = true :=
  rfl

/-- P3 gate: suspension-shift isomorphisms are typed. -/
theorem generalizedCohomologyTheoryInterfaceGate_suspensionShiftTyped :
    generalizedCohomologyTheoryInterfaceGate.suspensionShiftTyped = true :=
  rfl

/-- P3 gate: homotopy invariance is part of the checked interface. -/
theorem generalizedCohomologyTheoryInterfaceGate_homotopyInvarianceTyped :
    generalizedCohomologyTheoryInterfaceGate.homotopyInvarianceTyped = true :=
  rfl

/-- P3 gate: exactness witnesses are part of the checked interface. -/
theorem generalizedCohomologyTheoryInterfaceGate_exactnessWitnessTyped :
    generalizedCohomologyTheoryInterfaceGate.exactnessWitnessTyped = true :=
  rfl

/-- P3 gate: no completed state retains repo-local integration debt. -/
theorem generalizedCohomologyTheoryInterfaceGate_no_repoLocalIntegrationDebt :
    generalizedCohomologyTheoryInterfaceGate.completedStateRetainsRepoLocalIntegrationDebt = false :=
  rfl

/-- P3 gate: selecting the interface does not complete the AHSS parent theorem. -/
theorem generalizedCohomologyTheoryInterfaceGate_no_parent_completion :
    generalizedCohomologyTheoryInterfaceGate.parentCompletionAllowed = false :=
  rfl

/--
Current repo-local status of the ordinary cohomology API needed for the AHSS
`E₂` page.

The third constructor is the active status for this file: mathlib supplies
singular simplicial sets, singular chains, and singular homology, but this
snapshot does not expose a selected ordinary singular cohomology functor with
coefficient objects suitable for the AHSS formula.
-/
inductive OrdinaryCohomologyApiStatus where
  | abstractModelOnly
  | singularHomologyAndSimplicialAnchorsOnly
  | nativeSingularCohomologyApiMissing
  deriving DecidableEq, Repr

/--
Ordinary cohomology coefficient model for the AHSS `E₂` page.

Mathematically this is the assignment
`E₂^{p,q} = H^p(X; E^q(pt))`.  The fields keep the coefficient object
`E^q(pt)` tied to the local generalized-cohomology skeleton while leaving the
ordinary cohomology functor abstract until a singular/simplicial cohomology API
is imported or built.
-/
structure OrdinaryCohomologyCoefficientModel
    (C : Type uC) [Category.{vC} C] [Abelian C]
    (E : GeneralizedCohomologyTheorySkeleton.{uC, vC, w} C)
    (X : TopCat.{w}) : Type (max uC vC (w + 1)) where
  coefficientObject : ℤ → C
  coefficientObjectIso :
    ∀ q : ℤ, coefficientObject q ≅ E.coefficient q
  ordinaryCohomologyWithCoefficient : ℤ → ℤ → C
  e₂TermModel : ℤ → ℤ → C
  e₂TermModel_eq :
    ∀ p q : ℤ, e₂TermModel p q = ordinaryCohomologyWithCoefficient p q
  formulaConvention : String
  degreeConvention : String
  coefficientConvention : String
  apiStatus : OrdinaryCohomologyApiStatus
  singularSimplicialAnchor : String
  singularHomologyAnchor : String
  missingApiBlocker : String

/-- Coefficients in the local ordinary-cohomology model are the generalized coefficients. -/
def OrdinaryCohomologyCoefficientModel.coefficientAsGeneralizedCoefficient
    {C : Type uC} [Category.{vC} C] [Abelian C]
    {E : GeneralizedCohomologyTheorySkeleton.{uC, vC, w} C}
    {X : TopCat.{w}}
    (M : OrdinaryCohomologyCoefficientModel C E X) (q : ℤ) :
    M.coefficientObject q ≅ E.coefficient q :=
  M.coefficientObjectIso q

/-- The local model's `E₂` term is definitionally the selected ordinary cohomology object. -/
theorem OrdinaryCohomologyCoefficientModel.e₂TermModel_eq_ordinaryCohomology
    {C : Type uC} [Category.{vC} C] [Abelian C]
    {E : GeneralizedCohomologyTheorySkeleton.{uC, vC, w} C}
    {X : TopCat.{w}}
    (M : OrdinaryCohomologyCoefficientModel C E X) (p q : ℤ) :
    M.e₂TermModel p q = M.ordinaryCohomologyWithCoefficient p q :=
  M.e₂TermModel_eq p q

/-- Human-readable AHSS `E₂` page convention fixed by this child task. -/
def ordinaryCohomologyE₂FormulaConvention : String :=
  "E₂^{p,q} = H^p(X; E^q(pt))"

/-- Current blocker for replacing the abstract model by a concrete mathlib cohomology functor. -/
def ordinaryCohomologyCoefficientModelBlocker : String :=
  "formalization_debt: pinned mathlib exposes TopCat.toSSet, singularChainComplexFunctor, " ++
    "and singularHomologyFunctor, but no selected ordinary singular cohomology functor " ++
    "with coefficient objects E^q(pt) and AHSS-compatible degree conventions is available."

/-- Search terms used for the ordinary-cohomology side of the AHSS `E₂` audit. -/
def ordinaryCohomologyApiSearchTerms : List String := [
  "singularCohomology",
  "SingularCohomology",
  "ordinary cohomology",
  "cochainComplex",
  "cohomologyFunctor",
  "H^p(X; A)",
  "TopCat.toSSet",
  "singularChainComplexFunctor",
  "singularHomologyFunctor"
]

/-- Current repo-local status of the ordinary-cohomology API needed by P4. -/
def ordinaryCohomologyCurrentApiStatus : OrdinaryCohomologyApiStatus :=
  OrdinaryCohomologyApiStatus.nativeSingularCohomologyApiMissing

/-- P4 audit result: the native singular-cohomology API is currently missing. -/
theorem ordinaryCohomologyCurrentApiStatus_eq_missing :
    ordinaryCohomologyCurrentApiStatus =
      OrdinaryCohomologyApiStatus.nativeSingularCohomologyApiMissing :=
  rfl

/-- Completion gate for the P4 ordinary-cohomology coefficient model. -/
structure OrdinaryCohomologyCoefficientModelGate where
  e₂FormulaSpecified : Bool
  coefficientTiedToGeneralizedTheory : Bool
  abstractOrdinaryCohomologyModelTyped : Bool
  singularSimplicialAnchorTyped : Bool
  singularHomologyAnchorTyped : Bool
  nativeSingularCohomologyApiAvailable : Bool
  ahssE₂PageConcrete : Bool
  completedStateRetainsRepoLocalIntegrationDebt : Bool
  parentCompletionAllowed : Bool
  apiStatus : OrdinaryCohomologyApiStatus
  debtClass : String
  blocker : String
  validationCommand : String

/--
P4 gate: the `E₂^{p,q} = H^p(X; E^q(pt))` coefficient convention is typed,
and singular/simplicial support is anchored, but the concrete ordinary
singular-cohomology functor is still missing in the pinned repo-local API.
-/
def ordinaryCohomologyCoefficientModelGate :
    OrdinaryCohomologyCoefficientModelGate where
  e₂FormulaSpecified := true
  coefficientTiedToGeneralizedTheory := true
  abstractOrdinaryCohomologyModelTyped := true
  singularSimplicialAnchorTyped := true
  singularHomologyAnchorTyped := true
  nativeSingularCohomologyApiAvailable := false
  ahssE₂PageConcrete := false
  completedStateRetainsRepoLocalIntegrationDebt := false
  parentCompletionAllowed := false
  apiStatus := ordinaryCohomologyCurrentApiStatus
  debtClass := "formalization_debt"
  blocker := ordinaryCohomologyCoefficientModelBlocker
  validationCommand := "cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_106.lean"

/-- P4 gate: the AHSS `E₂` formula convention is recorded. -/
theorem ordinaryCohomologyCoefficientModelGate_formulaSpecified :
    ordinaryCohomologyCoefficientModelGate.e₂FormulaSpecified = true :=
  rfl

/-- P4 gate: coefficient objects are tied to the generalized cohomology coefficients. -/
theorem ordinaryCohomologyCoefficientModelGate_coefficientsTied :
    ordinaryCohomologyCoefficientModelGate.coefficientTiedToGeneralizedTheory = true :=
  rfl

/-- P4 gate: the ordinary-cohomology model is typed only abstractly. -/
theorem ordinaryCohomologyCoefficientModelGate_abstractModelTyped :
    ordinaryCohomologyCoefficientModelGate.abstractOrdinaryCohomologyModelTyped = true :=
  rfl

/-- P4 gate: singular/simplicial anchors are present, but native cohomology is not. -/
theorem ordinaryCohomologyCoefficientModelGate_nativeApiMissing :
    ordinaryCohomologyCoefficientModelGate.nativeSingularCohomologyApiAvailable = false :=
  rfl

/-- P4 gate: the current API status is the missing native singular-cohomology blocker. -/
theorem ordinaryCohomologyCoefficientModelGate_status :
    ordinaryCohomologyCoefficientModelGate.apiStatus =
      OrdinaryCohomologyApiStatus.nativeSingularCohomologyApiMissing :=
  rfl

/-- P4 gate: no completed state retains repo-local integration debt. -/
theorem ordinaryCohomologyCoefficientModelGate_no_repoLocalIntegrationDebt :
    ordinaryCohomologyCoefficientModelGate.completedStateRetainsRepoLocalIntegrationDebt = false :=
  rfl

/-- P4 gate: the abstract coefficient model does not complete the AHSS parent theorem. -/
theorem ordinaryCohomologyCoefficientModelGate_no_parent_completion :
    ordinaryCohomologyCoefficientModelGate.parentCompletionAllowed = false :=
  rfl

/--
Repo-local `TopCat` model selected for the AHSS filtration input.

The intended specialization is the skeletal filtration
`X⁰ -> X¹ -> ... -> X` of a finite or CW complex.  The current mathlib snapshot
does not provide a terminal bundled CW-complex/skeleton API for `TopCat`, so this
record keeps the object-level data and the exact hypotheses a future AHSS
construction must discharge.
-/
structure FilteredTopCatSkeleton : Type (w + 1) where
  total : TopCat.{w}
  stage : ℕ → TopCat.{w}
  stageToStage : (m n : ℕ) → (m ≤ n) → (stage m ⟶ stage n)
  stageToTotal : ∀ n : ℕ, (stage n ⟶ total)
  stage_id : ∀ n : ℕ, stageToStage n n (le_refl n) = 𝟙 (stage n)
  stage_comp :
    ∀ {l m n : ℕ} (hlm : l ≤ m) (hmn : m ≤ n),
      stageToStage l n (le_trans hlm hmn) =
        stageToStage l m hlm ≫ stageToStage m n hmn
  compatible_to_total :
    ∀ {m n : ℕ} (hmn : m ≤ n),
      stageToStage m n hmn ≫ stageToTotal n = stageToTotal m
  finiteOrCWHypotheses : Prop
  exhaustive : Prop
  closedCofibrationOrCellAttachmentHypotheses : Prop

/--
The selected P2 route: a natural-number-indexed `TopCat` filtration carrying
explicit CW/finite/exhaustiveness hypotheses.
-/
def selectedFilteredSpaceModelName : String :=
  "Nat-indexed TopCat skeleton with explicit finite/CW and cell-attachment hypotheses"

/--
Trivial filtration wrapper.  This is useful for later low-dimensional or
trivial-filtration sanity checks, but it is not an AHSS completion claim.
-/
def trivialFilteredTopCatSkeleton (X : TopCat.{w}) : FilteredTopCatSkeleton.{w} where
  total := X
  stage := fun _ => X
  stageToStage := fun _ _ _ => 𝟙 X
  stageToTotal := fun _ => 𝟙 X
  stage_id := by
    intro n
    rfl
  stage_comp := by
    intro l m n hlm hmn
    simp
  compatible_to_total := by
    intro m n hmn
    simp
  finiteOrCWHypotheses := True
  exhaustive := True
  closedCofibrationOrCellAttachmentHypotheses := True

/-- The trivial filtered skeleton has the requested total space. -/
theorem trivialFilteredTopCatSkeleton_total (X : TopCat.{w}) :
    (trivialFilteredTopCatSkeleton X).total = X :=
  rfl

/-- Every stage of the trivial filtered skeleton is definitionally the total space. -/
theorem trivialFilteredTopCatSkeleton_stage (X : TopCat.{w}) (n : ℕ) :
    (trivialFilteredTopCatSkeleton X).stage n = X :=
  rfl

/--
The AHSS construction input selected by P2: a filtered `TopCat` skeleton whose
total object is the space in the statement.
-/
def FilteredSpaceModelFor (X : TopCat.{w}) : Type (w + 1) :=
  {F : FilteredTopCatSkeleton.{w} // F.total = X}

/-- Any `TopCat` object has the trivial filtered-space model selected by P2. -/
def trivialFilteredSpaceModelFor (X : TopCat.{w}) : FilteredSpaceModelFor X :=
  ⟨trivialFilteredTopCatSkeleton X, rfl⟩

/-- Completion gate for the P2 filtered-space model selection. -/
structure FilteredSpaceModelSelectionGate where
  localModelSelected : Bool
  totalSpaceSubtypeSelected : Bool
  concreteCWApiImported : Bool
  terminalAHSSConstructionClosed : Bool
  completedStateRetainsRepoLocalIntegrationDebt : Bool
  parentCompletionAllowed : Bool
  debtClass : String
  selectedModel : String
  validationCommand : String

/--
P2 gate: the repo-local `TopCat` filtration skeleton is selected and checked,
but the absence of a concrete bundled CW-skeleton API remains formalization debt.
-/
def filteredSpaceModelSelectionGate : FilteredSpaceModelSelectionGate where
  localModelSelected := true
  totalSpaceSubtypeSelected := true
  concreteCWApiImported := false
  terminalAHSSConstructionClosed := false
  completedStateRetainsRepoLocalIntegrationDebt := false
  parentCompletionAllowed := false
  debtClass := "formalization_debt"
  selectedModel := selectedFilteredSpaceModelName
  validationCommand := "cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_106.lean"

/-- P2 gate: the selected model is repo-local and checked. -/
theorem filteredSpaceModelSelectionGate_model_selected :
    filteredSpaceModelSelectionGate.localModelSelected = true :=
  rfl

/-- P2 gate: no completed state retains repo-local integration debt. -/
theorem filteredSpaceModelSelectionGate_no_repoLocalIntegrationDebt :
    filteredSpaceModelSelectionGate.completedStateRetainsRepoLocalIntegrationDebt = false :=
  rfl

/-- P2 gate: selecting the filtered-space model does not complete the AHSS parent theorem. -/
theorem filteredSpaceModelSelectionGate_no_parent_completion :
    filteredSpaceModelSelectionGate.parentCompletionAllowed = false :=
  rfl

/--
The cohomological `r`-page complex shape used by mathlib spectral sequences.

For the AHSS convention this records that the page differential has vector
`(r, 1 - r)`.
-/
def CohomologicalPageComplexShape (r : ℤ) : ComplexShape (ℤ × ℤ) :=
  ComplexShape.up' (⟨r, 1 - r⟩ : ℤ × ℤ)

/-- Target bidegree of a cohomological `r`-page differential. -/
def cohomologicalPageDifferentialTarget (r : ℤ) (pq : ℤ × ℤ) : ℤ × ℤ :=
  (pq.1 + r, pq.2 + (1 - r))

/-- The mathlib cohomological page relation is exactly the `(r, 1-r)` bidegree shift. -/
theorem cohomologicalPageRel_iff (r p q p' q' : ℤ) :
    (CohomologicalPageComplexShape r).Rel (p, q) (p', q') ↔
      p + r = p' ∧ q + (1 - r) = q' := by
  constructor
  · intro h
    constructor
    · exact congrArg Prod.fst h
    · exact congrArg Prod.snd h
  · rintro ⟨hp, hq⟩
    exact Prod.ext hp hq

/-- The target selected by `cohomologicalPageDifferentialTarget` is related to the source. -/
theorem cohomologicalPageDifferentialTarget_rel (r : ℤ) (pq : ℤ × ℤ) :
    (CohomologicalPageComplexShape r).Rel pq (cohomologicalPageDifferentialTarget r pq) := by
  rcases pq with ⟨p, q⟩
  rw [cohomologicalPageRel_iff]
  exact ⟨rfl, rfl⟩

/-- First coordinate of the cohomological `r`-page differential target. -/
theorem cohomologicalPageDifferentialTarget_fst (r p q : ℤ) :
    (cohomologicalPageDifferentialTarget r (p, q)).1 = p + r :=
  rfl

/-- Second coordinate of the cohomological `r`-page differential target. -/
theorem cohomologicalPageDifferentialTarget_snd (r p q : ℤ) :
    (cohomologicalPageDifferentialTarget r (p, q)).2 = q + (1 - r) :=
  rfl

/-- The cohomological page differential raises total degree by one. -/
theorem cohomologicalPageDifferentialTarget_totalDegree (r p q : ℤ) :
    (cohomologicalPageDifferentialTarget r (p, q)).1 +
        (cohomologicalPageDifferentialTarget r (p, q)).2 = p + q + 1 := by
  unfold cohomologicalPageDifferentialTarget
  ring_nf

/--
Prototype spectral-object output attached to a filtered `TopCat` skeleton.

This is deliberately weaker than an AHSS theorem: it packages page complexes
with the cohomological page shape and records the exact-couple/spectral-object
and filtration-compatibility obligations as explicit propositions that a later
construction must prove.
-/
structure FilteredSpectralObjectPrototype
    (C : Type uC) [Category.{vC} C] [Abelian C] : Type (max uC vC (w + 1)) where
  filtration : FilteredTopCatSkeleton.{w}
  pageComplex : ∀ r : ℤ, HomologicalComplex C (CohomologicalPageComplexShape r)
  exactCoupleOrSpectralObjectConstruction : Prop
  filtrationCompatibility : Prop
  cohomologicalPageConvention : Prop

namespace FilteredSpectralObjectPrototype

/-- The page differential selected by the cohomological bidegree convention. -/
def pageDifferential
    {C : Type uC} [Category.{vC} C] [Abelian C]
    (P : FilteredSpectralObjectPrototype.{uC, vC, w} C) (r : ℤ) (pq : ℤ × ℤ) :
    (P.pageComplex r).X pq ⟶
      (P.pageComplex r).X (cohomologicalPageDifferentialTarget r pq) :=
  (P.pageComplex r).d pq (cohomologicalPageDifferentialTarget r pq)

/-- The prototype page differential has bidegree `(r, 1-r)`. -/
theorem pageDifferential_bidegree
    {C : Type uC} [Category.{vC} C] [Abelian C]
    (r p q : ℤ) :
    (CohomologicalPageComplexShape r).Rel (p, q)
      (cohomologicalPageDifferentialTarget r (p, q)) := by
  exact cohomologicalPageDifferentialTarget_rel r (p, q)

/-- The prototype page differentials square to zero, as supplied by `HomologicalComplex`. -/
theorem pageDifferential_comp_pageDifferential
    {C : Type uC} [Category.{vC} C] [Abelian C]
    (P : FilteredSpectralObjectPrototype.{uC, vC, w} C) (r : ℤ) (pq : ℤ × ℤ) :
    pageDifferential P r pq ≫
        pageDifferential P r (cohomologicalPageDifferentialTarget r pq) = 0 := by
  exact HomologicalComplex.d_comp_d (P.pageComplex r) pq
    (cohomologicalPageDifferentialTarget r pq)
    (cohomologicalPageDifferentialTarget r (cohomologicalPageDifferentialTarget r pq))

end FilteredSpectralObjectPrototype

/-- Current blocker for upgrading the P5 prototype to a concrete AHSS exact couple. -/
def filteredSpectralObjectPrototypeBlocker : String :=
  "formalization_debt: the repo-local artifact proves the cohomological page " ++
    "bidegree convention for abstract page complexes, but no concrete exact couple " ++
    "or spectral object has yet been constructed from filtered generalized cohomology."

/-- Completion gate for the P5 exact-couple/spectral-object prototype. -/
structure FilteredSpectralObjectPrototypeGate where
  filteredPrototypeTyped : Bool
  pageComplexShapeTyped : Bool
  bidegreeConventionProved : Bool
  totalDegreeShiftProved : Bool
  pageDifferentialsSquareZero : Bool
  concreteExactCoupleConstructed : Bool
  concreteSpectralObjectConstructed : Bool
  filtrationInstantiatedFromCohomology : Bool
  completedStateRetainsRepoLocalIntegrationDebt : Bool
  parentCompletionAllowed : Bool
  debtClass : String
  blocker : String
  validationCommand : String

/--
P5 gate: the filtered spectral-object prototype and page bidegree convention are
checked, while the concrete exact-couple/spectral-object construction remains
future formalization work.
-/
def filteredSpectralObjectPrototypeGate : FilteredSpectralObjectPrototypeGate where
  filteredPrototypeTyped := true
  pageComplexShapeTyped := true
  bidegreeConventionProved := true
  totalDegreeShiftProved := true
  pageDifferentialsSquareZero := true
  concreteExactCoupleConstructed := false
  concreteSpectralObjectConstructed := false
  filtrationInstantiatedFromCohomology := false
  completedStateRetainsRepoLocalIntegrationDebt := false
  parentCompletionAllowed := false
  debtClass := "formalization_debt"
  blocker := filteredSpectralObjectPrototypeBlocker
  validationCommand := "cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_106.lean"

/-- P5 gate: the filtered spectral-object prototype is typed. -/
theorem filteredSpectralObjectPrototypeGate_prototypeTyped :
    filteredSpectralObjectPrototypeGate.filteredPrototypeTyped = true :=
  rfl

/-- P5 gate: the cohomological page complex shape is typed. -/
theorem filteredSpectralObjectPrototypeGate_pageShapeTyped :
    filteredSpectralObjectPrototypeGate.pageComplexShapeTyped = true :=
  rfl

/-- P5 gate: the bidegree convention has a checked local proof. -/
theorem filteredSpectralObjectPrototypeGate_bidegreeProved :
    filteredSpectralObjectPrototypeGate.bidegreeConventionProved = true :=
  rfl

/-- P5 gate: the total-degree shift has a checked local proof. -/
theorem filteredSpectralObjectPrototypeGate_totalDegreeShiftProved :
    filteredSpectralObjectPrototypeGate.totalDegreeShiftProved = true :=
  rfl

/-- P5 gate: the prototype page differentials square to zero. -/
theorem filteredSpectralObjectPrototypeGate_squareZero :
    filteredSpectralObjectPrototypeGate.pageDifferentialsSquareZero = true :=
  rfl

/-- P5 gate: no completed state retains repo-local integration debt. -/
theorem filteredSpectralObjectPrototypeGate_no_repoLocalIntegrationDebt :
    filteredSpectralObjectPrototypeGate.completedStateRetainsRepoLocalIntegrationDebt = false :=
  rfl

/-- P5 gate: the prototype does not complete the AHSS parent theorem. -/
theorem filteredSpectralObjectPrototypeGate_no_parent_completion :
    filteredSpectralObjectPrototypeGate.parentCompletionAllowed = false :=
  rfl

/--
Data package for a future formal Atiyah-Hirzebruch spectral sequence over a
space `X` and a generalized cohomology theory `E`.

The fields record the expected mathematical interface:

* a cohomological `E₂` spectral sequence from mathlib,
* identification of its `E₂` page with ordinary cohomology of `X` with
  coefficients in the generalized coefficient objects,
* an associated graded target for the generalized cohomology of `X`,
* convergence and naturality hypotheses/conclusions.

No field asserts that mathlib already proves the AHSS; the structure is the
boundary a later local proof or pinned upstream theorem must fill.
-/
structure AtiyahHirzebruchSpectralSequenceData
    (C : Type uC) [Category.{vC} C] [Abelian C]
    (E : GeneralizedCohomologyTheorySkeleton.{uC, vC, w} C)
    (X : TopCat.{w}) : Type (max uC vC (w + 1)) where
  filteredSpace : FilteredSpaceModelFor X
  spectralSequence : MathlibE2CohomologicalSpectralSequence C
  ordinaryCohomologyCoefficientModel : OrdinaryCohomologyCoefficientModel C E X
  ordinaryCohomologyWithCoefficients : ℤ → ℤ → C
  e₂PageIso :
    ∀ p q : ℤ, E2PageObject spectralSequence p q ≅ ordinaryCohomologyWithCoefficients p q
  abutmentFiltrationQuotient : ℤ → ℤ → C
  abutmentIso :
    ∀ p q : ℤ, abutmentFiltrationQuotient p q ≅
      (E.cohomology (p + q)).obj (Opposite.op X)
  cellularOrFiniteFiltrationHypotheses : Prop
  convergenceToAssociatedGraded : Prop
  naturalityInSpace : Prop

/--
Hypotheses under which the Atiyah-Hirzebruch spectral sequence is expected to
converge to the associated graded object of generalized cohomology.

The first three fields reuse the selected filtered `TopCat` model.  The
remaining fields record the usual boundedness/completeness/separatedness
requirements without pretending that mathlib already has the corresponding
filtered-object API for generalized cohomology.
-/
structure AHSSConvergenceHypothesisBundle
    {X : TopCat.{w}} (F : FilteredSpaceModelFor X) : Type (w + 1) where
  finiteOrCW : F.1.finiteOrCWHypotheses
  exhaustive : F.1.exhaustive
  cellAttachmentOrCofibration : F.1.closedCofibrationOrCellAttachmentHypotheses
  boundedBelowInEachTotalDegree : Prop
  finiteLengthInEachTotalDegree : Prop
  completeForFiltrationTopology : Prop
  separatedForFiltrationTopology : Prop

/-- The non-`TopCat` convergence hypotheses as a single proposition. -/
def AHSSConvergenceHypothesisBundle.extraHypotheses
    {X : TopCat.{w}} {F : FilteredSpaceModelFor X}
    (H : AHSSConvergenceHypothesisBundle F) : Prop :=
  H.boundedBelowInEachTotalDegree ∧
    H.finiteLengthInEachTotalDegree ∧
    H.completeForFiltrationTopology ∧
    H.separatedForFiltrationTopology

/--
Associated-graded target for the AHSS abutment.

For total degree `n`, `targetCohomology n` is identified with `E^n(X)`.
The object `associatedGradedPiece p n` is the abstract local stand-in for
`F^p E^n(X) / F^{p+1} E^n(X)`.
-/
structure AssociatedGradedGeneralizedCohomologyTarget
    (C : Type uC) [Category.{vC} C] [Abelian C]
    (E : GeneralizedCohomologyTheorySkeleton.{uC, vC, w} C)
    (X : TopCat.{w}) : Type (max uC vC (w + 1)) where
  targetCohomology : ℤ → C
  targetCohomologyIso :
    ∀ n : ℤ, targetCohomology n ≅ (E.cohomology n).obj (Opposite.op X)
  filtrationStage : ℤ → ℤ → C
  filtrationMapToTarget : ∀ p n : ℤ, filtrationStage p n ⟶ targetCohomology n
  associatedGradedPiece : ℤ → ℤ → C
  associatedGradedPieceConvention : ℤ → ℤ → Prop
  exhaustiveCompleteSeparatedConvention : Prop
  finiteLengthConvention : Prop

/-- Total-degree convention for the cohomological AHSS bidegree `(p, q)`. -/
def ahssTotalDegree (p q : ℤ) : ℤ :=
  p + q

/--
P6 convergence data: the eventual/stable page is identified with the associated
graded pieces of generalized cohomology under finite/CW/completeness hypotheses.

This is still a statement-shape package, not a proof that mathlib constructs the
AHSS.  The `stablePageObject` field deliberately avoids naming an `E∞` API that
does not yet exist in the pinned mathlib snapshot.
-/
structure AtiyahHirzebruchConvergenceData
    (C : Type uC) [Category.{vC} C] [Abelian C]
    (E : GeneralizedCohomologyTheorySkeleton.{uC, vC, w} C)
    (X : TopCat.{w}) : Type (max uC vC (w + 1)) where
  ahssData : AtiyahHirzebruchSpectralSequenceData C E X
  convergenceHypotheses : AHSSConvergenceHypothesisBundle ahssData.filteredSpace
  extraHypothesesSatisfied : convergenceHypotheses.extraHypotheses
  associatedGradedTarget : AssociatedGradedGeneralizedCohomologyTarget C E X
  stablePageObject : ℤ → ℤ → C
  stablePageConvention : String
  pageStabilizationWitness : Prop
  convergesToAssociatedGraded :
    ∀ p q : ℤ,
      stablePageObject p q ≅
        associatedGradedTarget.associatedGradedPiece p (ahssTotalDegree p q)
  strongConvergenceConclusion : Prop
  extensionProblemsRecordedNotSolved : Prop

/--
The P6 theorem statement shape.

Given AHSS data and the finite/CW/completeness hypotheses, the stable page
converges to the associated graded of `E^(p+q)(X)`.
-/
def ConvergenceStatementShape
    (C : Type uC) [Category.{vC} C] [Abelian C]
    (E : GeneralizedCohomologyTheorySkeleton.{uC, vC, w} C)
    (X : TopCat.{w}) : Prop :=
  Nonempty (AtiyahHirzebruchConvergenceData C E X)

/-- The P6 convergence statement unfolds to nonemptiness of the convergence data package. -/
theorem convergenceStatementShape_iff_nonempty
    (C : Type uC) [Category.{vC} C] [Abelian C]
    (E : GeneralizedCohomologyTheorySkeleton.{uC, vC, w} C)
    (X : TopCat.{w}) :
    ConvergenceStatementShape C E X ↔
      Nonempty (AtiyahHirzebruchConvergenceData C E X) :=
  Iff.rfl

/-- Human-readable convention fixed by P6 for the AHSS convergence target. -/
def ahssConvergenceTargetConvention : String :=
  "E_infty^{p,q} is the associated graded piece F^p E^(p+q)(X) / F^(p+1) E^(p+q)(X)"

/-- Current blocker for upgrading the P6 statement shape into a proved AHSS convergence theorem. -/
def ahssConvergenceBlocker : String :=
  "formalization_debt: the repo has a typed convergence target, but no local or pinned Lean 4 " ++
    "construction of the AHSS stable page, filtered generalized cohomology abutment, " ++
    "or completeness/separatedness theorem for the filtration."

/-- Completion gate for the P6 convergence statement. -/
structure AHSSConvergenceStatementGate where
  convergenceStatementTyped : Bool
  finiteOrCWHypothesesRecorded : Bool
  boundednessHypothesesRecorded : Bool
  completenessSeparatednessHypothesesRecorded : Bool
  associatedGradedTargetTyped : Bool
  totalDegreeConventionTyped : Bool
  stablePageConventionRecorded : Bool
  terminalConvergenceProofImported : Bool
  terminalAHSSClosed : Bool
  completedStateRetainsRepoLocalIntegrationDebt : Bool
  parentCompletionAllowed : Bool
  debtClass : String
  blocker : String
  validationCommand : String

/--
P6 gate: the convergence theorem is stated as a checked data package under the
finite/CW, boundedness, completeness, and separatedness hypotheses, but no
terminal AHSS convergence proof is imported or locally constructed.
-/
def ahssConvergenceStatementGate : AHSSConvergenceStatementGate where
  convergenceStatementTyped := true
  finiteOrCWHypothesesRecorded := true
  boundednessHypothesesRecorded := true
  completenessSeparatednessHypothesesRecorded := true
  associatedGradedTargetTyped := true
  totalDegreeConventionTyped := true
  stablePageConventionRecorded := true
  terminalConvergenceProofImported := false
  terminalAHSSClosed := false
  completedStateRetainsRepoLocalIntegrationDebt := false
  parentCompletionAllowed := false
  debtClass := "formalization_debt"
  blocker := ahssConvergenceBlocker
  validationCommand := "cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_106.lean"

/-- P6 gate: the convergence statement shape is typed. -/
theorem ahssConvergenceStatementGate_statementTyped :
    ahssConvergenceStatementGate.convergenceStatementTyped = true :=
  rfl

/-- P6 gate: finite/CW input hypotheses are recorded in the checked bundle. -/
theorem ahssConvergenceStatementGate_finiteOrCW :
    ahssConvergenceStatementGate.finiteOrCWHypothesesRecorded = true :=
  rfl

/-- P6 gate: boundedness hypotheses are recorded in the checked bundle. -/
theorem ahssConvergenceStatementGate_boundedness :
    ahssConvergenceStatementGate.boundednessHypothesesRecorded = true :=
  rfl

/-- P6 gate: completeness and separatedness hypotheses are recorded. -/
theorem ahssConvergenceStatementGate_completenessSeparatedness :
    ahssConvergenceStatementGate.completenessSeparatednessHypothesesRecorded = true :=
  rfl

/-- P6 gate: the associated-graded target is typed. -/
theorem ahssConvergenceStatementGate_associatedGradedTarget :
    ahssConvergenceStatementGate.associatedGradedTargetTyped = true :=
  rfl

/-- P6 gate: the total-degree convention is typed. -/
theorem ahssConvergenceStatementGate_totalDegreeConvention :
    ahssConvergenceStatementGate.totalDegreeConventionTyped = true :=
  rfl

/-- P6 gate: no completed state retains repo-local integration debt. -/
theorem ahssConvergenceStatementGate_no_repoLocalIntegrationDebt :
    ahssConvergenceStatementGate.completedStateRetainsRepoLocalIntegrationDebt = false :=
  rfl

/-- P6 gate: the statement-shape package does not complete the AHSS parent theorem. -/
theorem ahssConvergenceStatementGate_no_parent_completion :
    ahssConvergenceStatementGate.parentCompletionAllowed = false :=
  rfl

/--
Checked P7 special-case wrapper for the trivial filtration.

This package verifies the low-dimensional sanity input that every `TopCat`
object admits the constant filtration `X = X = ...`, with all filtration-side
hypotheses discharged by `True`.  It deliberately does not construct the AHSS
pages, identify the `E₂` page, or prove convergence.
-/
structure TrivialFiltrationSpecialCaseWrapper (X : TopCat.{w}) : Type (w + 1) where
  filteredSpace : FilteredSpaceModelFor X
  filteredSpace_eq_trivial :
    filteredSpace.1 = trivialFilteredTopCatSkeleton X
  finiteOrCW : filteredSpace.1.finiteOrCWHypotheses
  exhaustive : filteredSpace.1.exhaustive
  cellAttachmentOrCofibration :
    filteredSpace.1.closedCofibrationOrCellAttachmentHypotheses
  pageShape : ℤ → ComplexShape (ℤ × ℤ)
  pageShape_eq : ∀ r : ℤ, pageShape r = CohomologicalPageComplexShape r
  totalDegree : ℤ × ℤ → ℤ
  totalDegree_eq : ∀ pq : ℤ × ℤ, totalDegree pq = pq.1 + pq.2
  terminalAHSSProof : Bool
  blocker : String

/-- The checked trivial-filtration special case used by `S1-M-106 / M0554.P7`. -/
def trivialFiltrationSpecialCaseWrapper (X : TopCat.{w}) :
    TrivialFiltrationSpecialCaseWrapper X where
  filteredSpace := trivialFilteredSpaceModelFor X
  filteredSpace_eq_trivial := rfl
  finiteOrCW := True.intro
  exhaustive := True.intro
  cellAttachmentOrCofibration := True.intro
  pageShape := CohomologicalPageComplexShape
  pageShape_eq := fun _ => rfl
  totalDegree := fun pq => pq.1 + pq.2
  totalDegree_eq := fun _ => rfl
  terminalAHSSProof := false
  blocker :=
    "formalization_debt: this checked P7 wrapper closes only the trivial-filtration " ++
      "input sanity case. It does not construct AHSS pages, the E₂ identification, " ++
      "or convergence to generalized cohomology."

/-- The P7 wrapper uses the constant filtration on every stage. -/
theorem trivialFiltrationSpecialCaseWrapper_stage (X : TopCat.{w}) (n : ℕ) :
    (trivialFiltrationSpecialCaseWrapper X).filteredSpace.1.stage n = X :=
  rfl

/-- The P7 wrapper keeps the standard cohomological page-shape convention. -/
theorem trivialFiltrationSpecialCaseWrapper_pageShape (X : TopCat.{w}) (r : ℤ) :
    (trivialFiltrationSpecialCaseWrapper X).pageShape r =
      CohomologicalPageComplexShape r :=
  rfl

/-- The P7 wrapper records the usual AHSS total-degree convention. -/
theorem trivialFiltrationSpecialCaseWrapper_totalDegree
    (X : TopCat.{w}) (p q : ℤ) :
    (trivialFiltrationSpecialCaseWrapper X).totalDegree (p, q) = p + q :=
  rfl

/-- The checked P7 wrapper is explicitly not a terminal AHSS proof. -/
theorem trivialFiltrationSpecialCaseWrapper_not_terminal (X : TopCat.{w}) :
    (trivialFiltrationSpecialCaseWrapper X).terminalAHSSProof = false :=
  rfl

/-- Statement shape closed by P7: the checked trivial-filtration wrapper exists. -/
def TrivialFiltrationSpecialCaseStatement (X : TopCat.{w}) : Prop :=
  Nonempty (TrivialFiltrationSpecialCaseWrapper X)

/-- Every `TopCat` object has the checked P7 trivial-filtration wrapper. -/
theorem trivialFiltrationSpecialCaseStatement (X : TopCat.{w}) :
    TrivialFiltrationSpecialCaseStatement X :=
  ⟨trivialFiltrationSpecialCaseWrapper X⟩

/-- Completion gate for the P7 special-case wrapper. -/
structure TrivialFiltrationSpecialCaseGate where
  localWrapperChecked : Bool
  terminalAHSSClosed : Bool
  externalProofImported : Bool
  completedStateRetainsRepoLocalIntegrationDebt : Bool
  completionClaimAllowedForParent : Bool
  debtClass : String
  validationCommand : String

/-- P7 gate: checked local wrapper, no parent AHSS completion claim. -/
def trivialFiltrationSpecialCaseGate : TrivialFiltrationSpecialCaseGate where
  localWrapperChecked := true
  terminalAHSSClosed := false
  externalProofImported := false
  completedStateRetainsRepoLocalIntegrationDebt := false
  completionClaimAllowedForParent := false
  debtClass := "formalization_debt"
  validationCommand := "cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_106.lean"

/-- The P7 gate records that the repo-local trivial-filtration wrapper is checked. -/
theorem trivialFiltrationSpecialCaseGate_localWrapperChecked :
    trivialFiltrationSpecialCaseGate.localWrapperChecked = true :=
  rfl

/-- The P7 gate is local wrapper work, not an imported external AHSS proof. -/
theorem trivialFiltrationSpecialCaseGate_no_externalProofImported :
    trivialFiltrationSpecialCaseGate.externalProofImported = false :=
  rfl

/-- No completed state in the P7 gate retains repo-local integration debt. -/
theorem trivialFiltrationSpecialCaseGate_no_repoLocalIntegrationDebt :
    trivialFiltrationSpecialCaseGate.completedStateRetainsRepoLocalIntegrationDebt = false :=
  rfl

/-- The P7 gate does not permit a parent AHSS completion claim. -/
theorem trivialFiltrationSpecialCaseGate_no_parent_completion :
    trivialFiltrationSpecialCaseGate.completionClaimAllowedForParent = false :=
  rfl

/--
Stage1 statement-shape candidate for the Atiyah-Hirzebruch spectral sequence.

For a fixed abelian target category, generalized cohomology skeleton, and space,
the formal target is the existence of the AHSS data package above.  This is a
statement shape only, not a terminal proof of the AHSS.
-/
def StatementShape
    (C : Type uC) [Category.{vC} C] [Abelian C]
    (E : GeneralizedCohomologyTheorySkeleton.{uC, vC, w} C)
    (X : TopCat.{w}) : Prop :=
  Nonempty (AtiyahHirzebruchSpectralSequenceData C E X)

/-- The statement-shape definition unfolds to nonemptiness of the AHSS data package. -/
theorem statementShape_iff_nonempty
    (C : Type uC) [Category.{vC} C] [Abelian C]
    (E : GeneralizedCohomologyTheorySkeleton.{uC, vC, w} C)
    (X : TopCat.{w}) :
    StatementShape C E X ↔
      Nonempty (AtiyahHirzebruchSpectralSequenceData C E X) :=
  Iff.rfl

/-- Wrapper for the category of mathlib `E₂` cohomological spectral sequences. -/
def mathlibE2CohomologicalSpectralSequenceType
    (C : Type uC) [Category.{vC} C] [Abelian C] :
    Type (max uC vC) :=
  MathlibE2CohomologicalSpectralSequence C

/-- The singular simplicial-set object currently available in mathlib. -/
abbrev MathlibSingularSimplicialSet (X : TopCat.{w}) : SSet.{w} :=
  TopCat.toSSet.obj X

/-- The local singular-simplicial-set wrapper is definitionally `TopCat.toSSet.obj X`. -/
theorem mathlibSingularSimplicialSet_def (X : TopCat.{w}) :
    MathlibSingularSimplicialSet X = TopCat.toSSet.obj X :=
  rfl

/-- Existing mathlib singular-chain complex with coefficient object `R`. -/
abbrev MathlibSingularChainComplexWithCoefficients
    (C : Type uC) [Category.{vC} C] [Limits.HasCoproducts.{w} C]
    [Preadditive C] [CategoryWithHomology C]
    (R : C) (X : TopCat.{w}) : ChainComplex C ℕ :=
  ((singularChainComplexFunctor C).obj R).obj X

/-- Existing mathlib singular-homology object with coefficient object `R`. -/
abbrev MathlibSingularHomologyWithCoefficients
    (C : Type uC) [Category.{vC} C] [Limits.HasCoproducts.{w} C]
    [Preadditive C] [CategoryWithHomology C]
    (R : C) (n : ℕ) (X : TopCat.{w}) : C :=
  (((singularHomologyFunctor C n).obj R).obj X)

/-- The local singular-chain wrapper is definitionally mathlib's singular-chain complex. -/
theorem mathlibSingularChainComplexWithCoefficients_def
    (C : Type uC) [Category.{vC} C] [Limits.HasCoproducts.{w} C]
    [Preadditive C] [CategoryWithHomology C]
    (R : C) (X : TopCat.{w}) :
    MathlibSingularChainComplexWithCoefficients C R X =
      ((singularChainComplexFunctor C).obj R).obj X :=
  rfl

/-- The local singular-homology wrapper is definitionally mathlib's singular-homology functor. -/
theorem mathlibSingularHomologyWithCoefficients_def
    (C : Type uC) [Category.{vC} C] [Limits.HasCoproducts.{w} C]
    [Preadditive C] [CategoryWithHomology C]
    (R : C) (n : ℕ) (X : TopCat.{w}) :
    MathlibSingularHomologyWithCoefficients C R n X =
      (((singularHomologyFunctor C n).obj R).obj X) :=
  rfl

/-- Checked wrapper around mathlib homotopy invariance of singular homology. -/
theorem singularHomology_homotopy_invariant
    {C : Type uC} [Category.{vC} C] [Preadditive C] [Limits.HasCoproducts C]
    [CategoryWithHomology C]
    {X Y : TopCat.{w}} {f g : X ⟶ Y}
    (H : TopCat.Homotopy f g) (R : C) (n : ℕ) :
    HomologicalComplex.homologyMap (((singularChainComplexFunctor C).obj R).map f) n =
      HomologicalComplex.homologyMap (((singularChainComplexFunctor C).obj R).map g) n := by
  exact TopCat.Homotopy.congr_homologyMap_singularChainComplexFunctor H R n

/-- One row in the local audit table for mathlib anchors relevant to the AHSS slot. -/
structure MathlibAnchorAuditRow where
  moduleName : String
  declarationName : String
  sourceLocation : String
  repoLocalStatus : String
  ahssRole : String
  blocker : String

/-- mathlib revision used for the public anchor audit requested by `S1-M-106 / M0554.P1`. -/
def mathlibAnchorAuditRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Algebra.Homology.SpectralSequence.Basic",
  "Mathlib.Algebra.Homology.SpectralSequence.ComplexShape",
  "Mathlib.Algebra.Homology.SpectralObject.SpectralSequence",
  "Mathlib.Algebra.Homology.SpectralObject.HasSpectralSequence",
  "Mathlib.Algebra.Homology.HomotopyCategory.SpectralObject",
  "Mathlib.AlgebraicTopology.SingularHomology.Basic",
  "Mathlib.AlgebraicTopology.SingularHomology.HomotopyInvarianceTopCat",
  "Mathlib.AlgebraicTopology.SimplicialSet.Basic",
  "Mathlib.AlgebraicTopology.DoldKan.Equivalence",
  "Mathlib.Topology.Category.TopCat.Basic"
]

/-- Public-backfill-ready audit rows for the checked mathlib anchors in this Stage1 slot. -/
def mathlibAnchorAuditTable : List MathlibAnchorAuditRow := [
  {
    moduleName := "Mathlib.Algebra.Homology.SpectralSequence.Basic",
    declarationName := "CategoryTheory.SpectralSequence",
    sourceLocation := "Mathlib/Algebra/Homology/SpectralSequence/Basic.lean:37",
    repoLocalStatus := "local_wrapper_upstream_mathlib",
    ahssRole := "Generic pages plus page-to-next-page homology isomorphisms in an abelian category.",
    blocker := "Not specialized to filtered spaces, ordinary cohomology, or AHSS convergence."
  },
  {
    moduleName := "Mathlib.Algebra.Homology.SpectralSequence.Basic",
    declarationName := "CategoryTheory.E₂CohomologicalSpectralSequence",
    sourceLocation := "Mathlib/Algebra/Homology/SpectralSequence/Basic.lean:114",
    repoLocalStatus := "local_wrapper_upstream_mathlib",
    ahssRole := "Cohomological E₂-page convention used by the local statement-shape wrapper.",
    blocker := "No identification with H^p(X; E^q(pt)) or generalized-cohomology target."
  },
  {
    moduleName := "Mathlib.Algebra.Homology.SpectralObject.Basic",
    declarationName := "CategoryTheory.Abelian.SpectralObject",
    sourceLocation := "Mathlib/Algebra/Homology/SpectralObject/Basic.lean:41",
    repoLocalStatus := "local_wrapper_upstream_mathlib",
    ahssRole := "Abelian-category spectral-object data with exact long-sequence structure.",
    blocker := "No filtered TopCat/CW input selected for AHSS construction."
  },
  {
    moduleName := "Mathlib.Algebra.Homology.SpectralObject.HasSpectralSequence",
    declarationName := "CategoryTheory.Abelian.SpectralObject.HasSpectralSequence",
    sourceLocation := "Mathlib/Algebra/Homology/SpectralObject/HasSpectralSequence.lean:277",
    repoLocalStatus := "upstream_anchor_checked",
    ahssRole := "Typeclass bridge from a spectral object to page data, including E₂ cohomological cores.",
    blocker := "Bridge is generic; it does not instantiate the AHSS filtration/cohomology package."
  },
  {
    moduleName := "Mathlib.Algebra.Homology.SpectralObject.SpectralSequence",
    declarationName := "CategoryTheory.Abelian.SpectralObject.SpectralSequence.page",
    sourceLocation := "Mathlib/Algebra/Homology/SpectralObject/SpectralSequence.lean:167",
    repoLocalStatus := "upstream_anchor_checked",
    ahssRole := "Constructs spectral-sequence pages from a spectral object under the required hypotheses.",
    blocker := "Requires AHSS-specific spectral object and convergence data not present in mathlib."
  },
  {
    moduleName := "Mathlib.AlgebraicTopology.SingularHomology.Basic",
    declarationName := "AlgebraicTopology.singularChainComplexFunctor",
    sourceLocation := "Mathlib/AlgebraicTopology/SingularHomology/Basic.lean:42",
    repoLocalStatus := "upstream_anchor_checked",
    ahssRole := "TopCat singular chains with coefficients in an abelian target category.",
    blocker := "Homology API is present; ordinary cohomology with generalized coefficient objects is not selected."
  },
  {
    moduleName := "Mathlib.AlgebraicTopology.SingularHomology.Basic",
    declarationName := "AlgebraicTopology.singularHomologyFunctor",
    sourceLocation := "Mathlib/AlgebraicTopology/SingularHomology/Basic.lean:47",
    repoLocalStatus := "upstream_anchor_checked",
    ahssRole := "Singular homology functor for TopCat spaces.",
    blocker := "AHSS E₂ page needs ordinary cohomology, not only this singular homology functor."
  },
  {
    moduleName := "Mathlib.AlgebraicTopology.SingularHomology.HomotopyInvarianceTopCat",
    declarationName := "TopCat.Homotopy.congr_homologyMap_singularChainComplexFunctor",
    sourceLocation := "Mathlib/AlgebraicTopology/SingularHomology/HomotopyInvarianceTopCat.lean:57",
    repoLocalStatus := "local_wrapper_upstream_mathlib",
    ahssRole := "Checked homotopy-invariance wrapper for singular homology maps in TopCat.",
    blocker := "Does not provide generalized cohomology axioms or AHSS convergence."
  },
  {
    moduleName := "Mathlib.AlgebraicTopology.SingularSet",
    declarationName := "TopCat.toSSet",
    sourceLocation := "Mathlib/AlgebraicTopology/SingularSet.lean:54",
    repoLocalStatus := "upstream_anchor_checked",
    ahssRole := "Singular simplicial set bridge used by the singular-chain construction.",
    blocker := "Bridge infrastructure only; no filtered-space AHSS construction."
  },
  {
    moduleName := "Mathlib.Topology.Category.TopCat.Basic",
    declarationName := "TopCat",
    sourceLocation := "Mathlib/Topology/Category/TopCat/Basic.lean:30",
    repoLocalStatus := "upstream_anchor_checked",
    ahssRole := "Bundled category of topological spaces for the local AHSS statement shape.",
    blocker := "TopCat alone does not encode CW filtrations or generalized cohomology."
  }
]

/-- Search terms that did not locate a terminal AHSS theorem in the pinned mathlib sources. -/
def absentTerminalSearchTerms : List String := [
  "Atiyah",
  "Hirzebruch",
  "AtiyahHirzebruch",
  "AHSS",
  "generalized cohomology",
  "CohomologyTheory",
  "FilteredComplex",
  "ExactCouple"
]

/--
One row in the P8 external-proof audit.

The row records a source/query rather than completion evidence.  In particular,
`terminalProofLocated = false` means there is no pin-ready proof artifact from
that source, while `requiresPinImportCheck = true` records the M0387 gate that
would apply if a future audit finds one.
-/
structure ExternalAHSSProofAuditRow where
  source : String
  query : String
  terminalProofLocated : Bool
  candidateModuleOrTheorem : String
  lakePinStatus : String
  integrationBlocker : String
  requiresPinImportCheck : Bool

/-- Audit date for the P8 external AHSS proof pass recorded by this Stage1 artifact. -/
def externalAHSSProofAuditDate : String := "2026-05-01"

/-- P8 audit rows for external Lean 4 AHSS proof search in this child pass. -/
def externalAHSSProofAuditRows : List ExternalAHSSProofAuditRow := [
  {
    source := "local repository and pinned mathlib dependency closure",
    query := "rg Atiyah|Hirzebruch|AtiyahHirzebruch|AHSS|generalized cohomology|ExactCouple",
    terminalProofLocated := false,
    candidateModuleOrTheorem := "",
    lakePinStatus := "not_applicable_no_candidate",
    integrationBlocker :=
      "No terminal AHSS Lean 4 theorem or importable external dependency was located in the local repo or pinned mathlib snapshot.",
    requiresPinImportCheck := true
  },
  {
    source := "GitHub repository search API",
    query := "AtiyahHirzebruch Lean; \"Atiyah-Hirzebruch\" Lean; AHSS Lean SpectralSequence",
    terminalProofLocated := false,
    candidateModuleOrTheorem := "",
    lakePinStatus := "not_applicable_no_candidate",
    integrationBlocker :=
      "Repository search returned no pin-ready Lean 4 AHSS proof repository for the audited query set.",
    requiresPinImportCheck := true
  },
  {
    source := "GitHub code search API (unauthenticated)",
    query := "AtiyahHirzebruch language:Lean; \"Atiyah-Hirzebruch\" language:Lean; AHSS language:Lean",
    terminalProofLocated := false,
    candidateModuleOrTheorem := "",
    lakePinStatus := "blocked_requires_authenticated_code_search",
    integrationBlocker :=
      "Unauthenticated GitHub code search returned 401 Requires authentication; any future completion-state change requires authenticated primary-source code search or equivalent.",
    requiresPinImportCheck := true
  },
  {
    source := "Reservoir package registry page",
    query := "Atiyah Hirzebruch; AHSS",
    terminalProofLocated := false,
    candidateModuleOrTheorem := "",
    lakePinStatus := "not_applicable_no_candidate",
    integrationBlocker :=
      "No visible package candidate was identified for a terminal AHSS proof; API search endpoints used in this pass returned unavailable-path responses.",
    requiresPinImportCheck := true
  }
]

/--
P8 integration gate for external AHSS proofs.

This gate is deliberately not a completion claim.  It states the invariant that
anchor-only external evidence cannot close the AHSS slot: any future external
Lean 4 proof must be pinned/imported/checked in this Lake closure, or else the
public status must record a concrete blocker and remain open.
-/
structure ExternalAHSSProofIntegrationGate where
  terminalExternalProofLocated : Bool
  externalProofPinnedImportedChecked : Bool
  anchorOnlyCompletionClaimed : Bool
  completedStateRetainsRepoLocalIntegrationDebt : Bool
  parentCompletionAllowed : Bool
  currentDebtClass : String
  requiredFutureAction : String

/-- Current P8 result: no external proof candidate is integrated or used as completion evidence. -/
def externalAHSSProofIntegrationGate : ExternalAHSSProofIntegrationGate where
  terminalExternalProofLocated := false
  externalProofPinnedImportedChecked := false
  anchorOnlyCompletionClaimed := false
  completedStateRetainsRepoLocalIntegrationDebt := false
  parentCompletionAllowed := false
  currentDebtClass := "formalization_debt"
  requiredFutureAction :=
    "If a terminal external Lean 4 AHSS proof is later found, pin/import/check it " ++
      "inside Formalizations/Lean or record a concrete toolchain/license/API blocker; " ++
      "do not mark the AHSS slot completed from anchor-only evidence."

/-- P8 gate: this audit has not located a terminal external AHSS proof candidate. -/
theorem externalAHSSProofIntegrationGate_no_terminalExternalProofLocated :
    externalAHSSProofIntegrationGate.terminalExternalProofLocated = false :=
  rfl

/-- P8 gate: no external AHSS proof is currently pinned, imported, and checked here. -/
theorem externalAHSSProofIntegrationGate_no_externalProofPinnedImportedChecked :
    externalAHSSProofIntegrationGate.externalProofPinnedImportedChecked = false :=
  rfl

/-- P8 gate: no anchor-only external evidence is treated as completion. -/
theorem externalAHSSProofIntegrationGate_no_anchorOnlyCompletion :
    externalAHSSProofIntegrationGate.anchorOnlyCompletionClaimed = false :=
  rfl

/-- P8 gate: no completed state retains repo-local integration debt. -/
theorem externalAHSSProofIntegrationGate_no_repoLocalIntegrationDebt :
    externalAHSSProofIntegrationGate.completedStateRetainsRepoLocalIntegrationDebt = false :=
  rfl

/-- P8 gate: parent AHSS completion is not allowed by the current external-proof audit. -/
theorem externalAHSSProofIntegrationGate_no_parent_completion :
    externalAHSSProofIntegrationGate.parentCompletionAllowed = false :=
  rfl

end S1_M_106
end Stage1
end AwesomeTheorems
