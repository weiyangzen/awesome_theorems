import Mathlib.CategoryTheory.Monoidal.Tor
import Mathlib.Algebra.Homology.HomologySequence
import Mathlib.Algebra.Homology.HomologySequenceLemmas
import Mathlib.Algebra.Homology.ShortComplex.ShortExact

/-!
# S1-M-101 / THM-M-0008: Tor functor properties

This Stage1 file records the repo-local Lean boundary for the general properties
of Tor functors.  The pinned mathlib snapshot defines `CategoryTheory.Tor` and
`CategoryTheory.Tor'` as left-derived tensor-product functors and proves the
basic vanishing of higher Tor against projective objects.  It does not yet expose
a terminal packaged theorem giving the full balanced comparison, naturality of
connecting morphisms, and long exact Tor sequences.

The declarations below therefore provide checked aliases and wrappers for the
available mathlib facts, plus a precise statement-shape package for the missing
terminal theorem family.  No proof placeholder is introduced.
-/

noncomputable section

open CategoryTheory CategoryTheory.Limits CategoryTheory.MonoidalCategory

universe u v w

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_101

variable (C : Type u) [Category.{v} C] [MonoidalCategory C]
  [Abelian C] [MonoidalPreadditive C] [HasProjectiveResolutions C]

/-- Mathlib's Tor functor, derived in the second tensor variable. -/
abbrev TorFunctor (n : ℕ) : C ⥤ C ⥤ C :=
  CategoryTheory.Tor C n

/-- Mathlib's alternate Tor functor, derived in the first tensor variable. -/
abbrev TorPrimeFunctor (n : ℕ) : C ⥤ C ⥤ C :=
  CategoryTheory.Tor' C n

/-- The local alias for Tor unfolds definitionally to mathlib's `CategoryTheory.Tor`. -/
theorem torFunctor_eq_mathlib (n : ℕ) :
    TorFunctor C n = CategoryTheory.Tor C n :=
  rfl

/-- The local alias for the alternate Tor unfolds definitionally to mathlib's `CategoryTheory.Tor'`. -/
theorem torPrimeFunctor_eq_mathlib (n : ℕ) :
    TorPrimeFunctor C n = CategoryTheory.Tor' C n :=
  rfl

/-- Audit witness: `Tor` is left-derived tensoring in the second variable. -/
theorem torFunctor_obj_eq_leftDerived (n : ℕ) (X : C) :
    (TorFunctor C n).obj X =
      CategoryTheory.Functor.leftDerived ((tensoringLeft C).obj X) n :=
  rfl

/-- Audit witness: maps of `Tor` are left-derived maps of left tensoring. -/
theorem torFunctor_map_eq_leftDerived (n : ℕ) {X Y : C} (f : X ⟶ Y) :
    (TorFunctor C n).map f =
      CategoryTheory.NatTrans.leftDerived ((tensoringLeft C).map f) n :=
  rfl

/-- Audit witness: `Tor'` is left-derived tensoring in the first variable, then flipped. -/
theorem torPrimeFunctor_obj_obj_eq_leftDerived (n : ℕ) (X Y : C) :
    ((TorPrimeFunctor C n).obj X).obj Y =
      (CategoryTheory.Functor.leftDerived ((tensoringRight C).obj Y) n).obj X :=
  rfl

/--
Checked mathlib wrapper: higher Tor vanishes when the second input is projective.

This is a genuine local proof, but it is not the full Tor long-exact-sequence
theorem.
-/
theorem tor_succ_isZero_of_projective (X Y : C) [Projective Y] (n : ℕ) :
    IsZero (((TorFunctor C (n + 1)).obj X).obj Y) := by
  exact CategoryTheory.isZero_Tor_succ_of_projective C X Y n

/--
Checked mathlib wrapper: the alternate higher Tor vanishes when the first input
is projective.
-/
theorem torPrime_succ_isZero_of_projective (X Y : C) [Projective X] (n : ℕ) :
    IsZero (((TorPrimeFunctor C (n + 1)).obj X).obj Y) := by
  exact CategoryTheory.isZero_Tor'_succ_of_projective C X Y n

/-- A basic functoriality smoke test for naturality in the first variable. -/
theorem tor_map_id_app (n : ℕ) (X Y : C) :
    ((TorFunctor C n).map (𝟙 X)).app Y =
      𝟙 (((TorFunctor C n).obj X).obj Y) := by
  simp [TorFunctor]

/-- A basic composition smoke test for functoriality in the first variable. -/
theorem tor_map_comp_app (n : ℕ) {X Y Z : C} (f : X ⟶ Y) (g : Y ⟶ Z) (W : C) :
    ((TorFunctor C n).map (f ≫ g)).app W =
      ((TorFunctor C n).map f).app W ≫ ((TorFunctor C n).map g).app W := by
  simp [TorFunctor]

/-- A basic functoriality smoke test for naturality in the second variable. -/
theorem tor_obj_map_id (n : ℕ) (X Y : C) :
    ((TorFunctor C n).obj X).map (𝟙 Y) =
      𝟙 (((TorFunctor C n).obj X).obj Y) := by
  simp [TorFunctor]

/-- A basic composition smoke test for functoriality in the second variable. -/
theorem tor_obj_map_comp (n : ℕ) (X : C) {Y Z W : C} (f : Y ⟶ Z) (g : Z ⟶ W) :
    ((TorFunctor C n).obj X).map (f ≫ g) =
      ((TorFunctor C n).obj X).map f ≫ ((TorFunctor C n).obj X).map g := by
  simp [TorFunctor]

/--
Stage1 hypothesis boundary for the future balanced comparison
`Tor C n ≅ Tor' C n`.

The surrounding variables are the exact Lean typeclass envelope currently needed
to even state mathlib's two functors: `Category`, `MonoidalCategory`, `Abelian`,
`MonoidalPreadditive`, and `HasProjectiveResolutions`.  The fields below are the
additional proof obligations that are not supplied by
`Mathlib.CategoryTheory.Monoidal.Tor`: a common delta-functor framework, the
degree-zero tensor-product comparison, uniqueness for the two effaceable
derived-functor constructions, and the resulting natural comparison in both
variables.  This is statement-boundary data only; it does not prove the
comparison.
-/
structure BalancedComparisonHypothesisPackage : Type (max u v) where
  torDeltaFunctorStructure : Prop
  torPrimeDeltaFunctorStructure : Prop
  torDeltaStructure_holds : torDeltaFunctorStructure
  torPrimeDeltaStructure_holds : torPrimeDeltaFunctorStructure
  torEffaceableInSecondVariable : Prop
  torPrimeEffaceableInFirstVariable : Prop
  torEffaceability_holds : torEffaceableInSecondVariable
  torPrimeEffaceability_holds : torPrimeEffaceableInFirstVariable
  degreeZeroTensorComparison : TorFunctor C 0 ≅ TorPrimeFunctor C 0
  deltaFunctorUniquenessApplies : Prop
  deltaFunctorUniqueness_holds : deltaFunctorUniquenessApplies
  balancedComparison : ∀ n : ℕ, TorFunctor C n ≅ TorPrimeFunctor C n
  naturalInFirstVariable : Prop
  naturalInSecondVariable : Prop
  naturalInFirstVariable_holds : naturalInFirstVariable
  naturalInSecondVariable_holds : naturalInSecondVariable

/--
The isolated Stage1 target for deciding the exact hypotheses of a future
balanced Tor comparison.  This remains unproved until the delta-functor and
degree-zero comparison fields above are supplied locally or by a pinned import.
-/
def BalancedComparisonStatementShape : Prop :=
  Nonempty (BalancedComparisonHypothesisPackage C)

/-- The balanced-comparison target is exactly nonemptiness of the package above. -/
theorem balancedComparisonStatementShape_iff_nonempty :
    BalancedComparisonStatementShape C ↔
      Nonempty (BalancedComparisonHypothesisPackage C) :=
  Iff.rfl

/-- Projection from a future package to the comparison at a fixed degree. -/
def balancedComparison_of_package
    (P : BalancedComparisonHypothesisPackage C) (n : ℕ) :
    TorFunctor C n ≅ TorPrimeFunctor C n :=
  P.balancedComparison n

section HomologySequenceBridge

open HomologicalComplex

variable {A : Type u} [Category.{v} A] [Abelian A]
variable {ι : Type w} {c : ComplexShape ι}
variable {S : ShortComplex (HomologicalComplex A c)}
variable (hS : S.ShortExact) (i j : ι) (hij : c.Rel i j)

/--
Checked local name for the connecting morphism supplied by
`ShortComplex.ShortExact.δ` in the homology sequence of a short exact sequence
of complexes.
-/
abbrev HomologySequenceConnectingMorphism :
    S.X₃.homology i ⟶ S.X₁.homology j :=
  hS.δ i j hij

/-- The local connecting-morphism alias is definitionally mathlib's `hS.δ`. -/
theorem homologySequenceConnectingMorphism_eq_shortExact_delta :
    HomologySequenceConnectingMorphism hS i j hij = hS.δ i j hij :=
  rfl

/--
Checked wrapper for exactness at `S.X₁.homology j` in the homology sequence:
`S.X₃.homology i ⟶ S.X₁.homology j ⟶ S.X₂.homology j`.
-/
theorem homologySequence_exact₁ :
    (ShortComplex.mk _ _ (ShortComplex.ShortExact.δ_comp hS i j hij)).Exact :=
  hS.homology_exact₁ i j hij

/--
Checked wrapper for exactness at `S.X₂.homology i` in the homology sequence:
`S.X₁.homology i ⟶ S.X₂.homology i ⟶ S.X₃.homology i`.
-/
theorem homologySequence_exact₂ (hS : S.ShortExact) :
    (ShortComplex.mk (homologyMap S.f i) (homologyMap S.g i)
      (by rw [← homologyMap_comp, S.zero, homologyMap_zero])).Exact :=
  hS.homology_exact₂ i

/--
Checked wrapper for exactness at `S.X₃.homology i` in the homology sequence:
`S.X₂.homology i ⟶ S.X₃.homology i ⟶ S.X₁.homology j`.
-/
theorem homologySequence_exact₃ :
    (ShortComplex.mk _ _ (ShortComplex.ShortExact.comp_δ hS i j hij)).Exact :=
  hS.homology_exact₃ i j hij

/--
Checked wrapper for the six-term exact sequence built from
`homology_exact₂`, `homology_exact₃`, `homology_exact₁`, and
`homology_exact₂` in the next degree.
-/
theorem homologySequence_composableArrows₅_exact :
    (HomologySequence.composableArrows₅ hS i j hij).Exact :=
  HomologySequence.composableArrows₅_exact hS i j hij

end HomologySequenceBridge

/--
Statement-shape package for the missing bridge from mathlib's homology-sequence
machinery to a Tor-specific long exact sequence.

The checked wrappers above identify the available local ingredients:
`ShortComplex.ShortExact.δ`, `homology_exact₁/₂/₃`, and
`HomologySequence.composableArrows₅_exact`.  A future Tor proof still has to
construct the appropriate short exact sequence of projective-resolution
complexes, identify its homology objects with `Tor`, identify the resulting
connecting morphism with the Tor boundary map, and then transport the
six-term/window exactness statement through those identifications.
-/
structure TorLongExactBridgePackage (C : Type u) [Category.{v} C] [MonoidalCategory C]
    [Abelian C] [MonoidalPreadditive C] [HasProjectiveResolutions C] :
    Type (max u v) where
  projectiveResolutionShortExactLift : Prop
  torHomologyIdentifications : Prop
  connectingMorphismIsShortExactDelta : Prop
  torLongExactSecondVariable : Prop
  torLongExactFirstVariable : Prop
  naturalityFromHomologySequence : Prop
  projectiveResolutionShortExactLift_holds : projectiveResolutionShortExactLift
  torHomologyIdentifications_holds : torHomologyIdentifications
  connectingMorphismIsShortExactDelta_holds : connectingMorphismIsShortExactDelta
  torLongExactSecondVariable_holds : torLongExactSecondVariable
  torLongExactFirstVariable_holds : torLongExactFirstVariable
  naturalityFromHomologySequence_holds : naturalityFromHomologySequence

/--
The isolated Stage1 target for the child task bridging
`ShortComplex.ShortExact.δ` and `HomologySequence` exactness lemmas to a
Tor-specific long exact sequence statement.
-/
def TorLongExactBridgeStatementShape : Prop :=
  Nonempty (TorLongExactBridgePackage C)

/-- The Tor long-exact bridge target unfolds to nonemptiness of the package above. -/
theorem torLongExactBridgeStatementShape_iff_nonempty :
    TorLongExactBridgeStatementShape C ↔
      Nonempty (TorLongExactBridgePackage C) :=
  Iff.rfl

/--
A repo-local planning leaf for splitting the still-unproved Tor naturality and
long-exact-sequence branches.

The fields are textual because the pinned mathlib Tor API does not yet expose
the terminal balanced-comparison or Tor long-exact-sequence theorems needed to
promote these nodes into proof statements.  The list below is nevertheless
checked as a concrete M0387 `<= 100` local-budget inventory.
-/
structure TorExpandedProofLeaf where
  id : String
  parentLeaf : String
  package : String
  obligation : String
  upstreamInputs : String
  downstreamOutput : String
  localBudgetSteps : Nat
  status : String

/--
M0387-level split of `M0008-L017` through `M0008-L021`.

This is a proof-leaf ledger, not a proof of the terminal Tor theorem family.
Each entry is intended to become a separate `<= 100` step proof unit after the
missing Tor comparison, boundary-map, and exactness-transport APIs are supplied
locally or by a pinned upstream Lean dependency.
-/
def torExpandedProofLeaves : List TorExpandedProofLeaf :=
  [ { id := "M0008-L017-A",
      parentLeaf := "M0008-L017",
      package := "functoriality_and_naturality",
      obligation := "state the bifunctorial square for Tor maps induced by f : X1 -> X2 and g : Y1 -> Y2",
      upstreamInputs := "TorFunctor, functoriality in each variable, tensoringLeft/tensoringRight map conventions",
      downstreamOutput := "canonical naturality-square statement for TorFunctor C n",
      localBudgetSteps := 35,
      status := "unchecked_formalization_debt_statement_shape" },
    { id := "M0008-L017-B",
      parentLeaf := "M0008-L017",
      package := "functoriality_and_naturality",
      obligation := "prove the first-variable identity edge of the Tor bifunctorial square",
      upstreamInputs := "tor_map_id_app and category identity simplification",
      downstreamOutput := "identity naturality square in the first variable",
      localBudgetSteps := 25,
      status := "checked_support_exists_terminal_square_unchecked" },
    { id := "M0008-L017-C",
      parentLeaf := "M0008-L017",
      package := "functoriality_and_naturality",
      obligation := "prove the second-variable identity edge of the Tor bifunctorial square",
      upstreamInputs := "tor_obj_map_id and category identity simplification",
      downstreamOutput := "identity naturality square in the second variable",
      localBudgetSteps := 25,
      status := "checked_support_exists_terminal_square_unchecked" },
    { id := "M0008-L017-D",
      parentLeaf := "M0008-L017",
      package := "functoriality_and_naturality",
      obligation := "prove first-variable composition compatibility for the Tor bifunctorial square",
      upstreamInputs := "tor_map_comp_app and functor composition laws",
      downstreamOutput := "composition naturality in the first variable",
      localBudgetSteps := 35,
      status := "checked_support_exists_terminal_square_unchecked" },
    { id := "M0008-L017-E",
      parentLeaf := "M0008-L017",
      package := "functoriality_and_naturality",
      obligation := "prove second-variable composition compatibility for the Tor bifunctorial square",
      upstreamInputs := "tor_obj_map_comp and functor composition laws",
      downstreamOutput := "composition naturality in the second variable",
      localBudgetSteps := 35,
      status := "checked_support_exists_terminal_square_unchecked" },
    { id := "M0008-L018-A",
      parentLeaf := "M0008-L018",
      package := "connecting_morphism_naturality",
      obligation := "state maps of short exact sequences of complexes in the form needed by the homology-sequence boundary map",
      upstreamInputs := "ShortComplex.ShortExact, HomologicalComplex maps, HomologySequence lemmas",
      downstreamOutput := "map-of-short-exact-sequences input package",
      localBudgetSteps := 55,
      status := "unchecked_formalization_debt_statement_shape" },
    { id := "M0008-L018-B",
      parentLeaf := "M0008-L018",
      package := "connecting_morphism_naturality",
      obligation := "identify the generic connecting morphism in the source and target homology sequences as ShortComplex.ShortExact.delta",
      upstreamInputs := "HomologySequenceConnectingMorphism and homologySequenceConnectingMorphism_eq_shortExact_delta",
      downstreamOutput := "source/target boundary-map identifications",
      localBudgetSteps := 45,
      status := "checked_support_exists_terminal_naturality_unchecked" },
    { id := "M0008-L018-C",
      parentLeaf := "M0008-L018",
      package := "connecting_morphism_naturality",
      obligation := "prove the homology-sequence delta naturality square for maps of short exact sequences",
      upstreamInputs := "Mathlib.Algebra.Homology.HomologySequenceLemmas and the map-of-short-exact input package",
      downstreamOutput := "generic connecting-morphism naturality square",
      localBudgetSteps := 90,
      status := "unchecked_formalization_debt_generic_naturality" },
    { id := "M0008-L018-D",
      parentLeaf := "M0008-L018",
      package := "connecting_morphism_naturality",
      obligation := "transport generic delta naturality through the future Tor homology identifications",
      upstreamInputs := "generic delta naturality, torHomologyIdentifications, connectingMorphismIsShortExactDelta",
      downstreamOutput := "Tor connecting-morphism naturality statement",
      localBudgetSteps := 95,
      status := "unchecked_formalization_debt_tor_transport" },
    { id := "M0008-L019-A",
      parentLeaf := "M0008-L019",
      package := "short_exact_to_long_exact",
      obligation := "choose the second-variable short exact sequence convention and freeze the object order",
      upstreamInputs := "TorFunctor, ShortComplex.ShortExact, tensoringLeft convention",
      downstreamOutput := "second-variable Tor short-exact input convention",
      localBudgetSteps := 40,
      status := "unchecked_formalization_debt_statement_shape" },
    { id := "M0008-L019-B",
      parentLeaf := "M0008-L019",
      package := "short_exact_to_long_exact",
      obligation := "fix the homological index shift relating Tor degree n+1, the boundary morphism, and Tor degree n",
      upstreamInputs := "Functor.leftDerived indexing and HomologySequence c.Rel indices",
      downstreamOutput := "second-variable Tor long-exact index convention",
      localBudgetSteps := 60,
      status := "unchecked_formalization_debt_indexing" },
    { id := "M0008-L019-C",
      parentLeaf := "M0008-L019",
      package := "short_exact_to_long_exact",
      obligation := "state the displayed window of the second-variable Tor long exact sequence at a fixed degree",
      upstreamInputs := "index convention, TorFunctor object maps, future Tor boundary map",
      downstreamOutput := "second-variable long-exact window statement",
      localBudgetSteps := 70,
      status := "unchecked_formalization_debt_statement_shape" },
    { id := "M0008-L020-A",
      parentLeaf := "M0008-L020",
      package := "short_exact_to_long_exact",
      obligation := "construct or import the short exact sequence of projective-resolution complexes feeding the homology sequence",
      upstreamInputs := "projective resolutions, short exact input sequence, tensoringLeft exactness requirements",
      downstreamOutput := "projectiveResolutionShortExactLift field for TorLongExactBridgePackage",
      localBudgetSteps := 100,
      status := "unchecked_formalization_debt_resolution_lift" },
    { id := "M0008-L020-B",
      parentLeaf := "M0008-L020",
      package := "short_exact_to_long_exact",
      obligation := "identify homology objects of the lifted complexes with the displayed Tor objects",
      upstreamInputs := "Functor.leftDerived definitions, TorFunctor object audit, projective-resolution lift",
      downstreamOutput := "torHomologyIdentifications field for TorLongExactBridgePackage",
      localBudgetSteps := 100,
      status := "unchecked_formalization_debt_homology_identification" },
    { id := "M0008-L020-C",
      parentLeaf := "M0008-L020",
      package := "short_exact_to_long_exact",
      obligation := "transport homologySequence_exact1, exact2, exact3, and composableArrows5 exactness to each displayed Tor object",
      upstreamInputs := "homologySequence_exact1/exact2/exact3 wrappers and Tor homology identifications",
      downstreamOutput := "exactness at every object in the second-variable Tor long-exact window",
      localBudgetSteps := 100,
      status := "unchecked_formalization_debt_exactness_transport" },
    { id := "M0008-L020-D",
      parentLeaf := "M0008-L020",
      package := "short_exact_to_long_exact",
      obligation := "package the transported exactness windows into the second-variable long exact Tor statement",
      upstreamInputs := "displayed Tor windows and exactness-at-object transport lemmas",
      downstreamOutput := "torLongExactSecondVariable field for TorLongExactBridgePackage",
      localBudgetSteps := 75,
      status := "unchecked_formalization_debt_terminal_packaging" },
    { id := "M0008-L021-A",
      parentLeaf := "M0008-L021",
      package := "balanced_first_variable_long_exact",
      obligation := "decide whether the first-variable long exact sequence is proved directly with TorPrimeFunctor or transported through balanced comparison",
      upstreamInputs := "BalancedComparisonHypothesisPackage, TorPrimeFunctor, second-variable long-exact package",
      downstreamOutput := "selected first-variable proof route",
      localBudgetSteps := 45,
      status := "unchecked_formalization_debt_route_selection" },
    { id := "M0008-L021-B",
      parentLeaf := "M0008-L021",
      package := "balanced_first_variable_long_exact",
      obligation := "if using TorPrimeFunctor directly, mirror the projective-resolution lift and homology identification in the first variable",
      upstreamInputs := "TorPrimeFunctor object audit, tensoringRight convention, homology-sequence bridge wrappers",
      downstreamOutput := "first-variable direct long-exact construction",
      localBudgetSteps := 100,
      status := "unchecked_formalization_debt_direct_route" },
    { id := "M0008-L021-C",
      parentLeaf := "M0008-L021",
      package := "balanced_first_variable_long_exact",
      obligation := "if transporting, prove exactness is preserved across the balanced comparison isomorphisms degree-by-degree",
      upstreamInputs := "balancedComparison, second-variable exactness windows, isomorphism transport lemmas",
      downstreamOutput := "first-variable exactness via balanced comparison",
      localBudgetSteps := 95,
      status := "unchecked_formalization_debt_balanced_transport" },
    { id := "M0008-L021-D",
      parentLeaf := "M0008-L021",
      package := "balanced_first_variable_long_exact",
      obligation := "package the selected first-variable route into the terminal Tor property package without claiming completion prematurely",
      upstreamInputs := "first-variable direct or transported exactness and naturality data",
      downstreamOutput := "torLongExactFirstVariable field for TorLongExactBridgePackage and TorPropertyPackage",
      localBudgetSteps := 70,
      status := "unchecked_formalization_debt_terminal_packaging" } ]

/-- Every expanded Tor proof leaf is explicitly budgeted at `<= 100` steps. -/
theorem torExpandedProofLeaves_all_budget_le_100 :
    torExpandedProofLeaves.all (fun leaf => leaf.localBudgetSteps <= 100) = true := by
  native_decide

/-- The expansion preserves the five requested parent leaves `M0008-L017` through `M0008-L021`. -/
theorem torExpandedProofLeaves_parent_count :
    torExpandedProofLeaves.length = 20 := by
  native_decide

/-- This split is complete as a ledger, while the terminal Tor proof remains open. -/
def torExpandedProofLeavesSplitStatus : String :=
  "split_complete_terminal_tor_proof_open_formalization_debt"

/--
Repo-local integration gate for a possible external Lean 4 proof of Tor long
exact sequences.

This is intentionally a gate, not evidence of a theorem proof.  At the current
repo boundary no external Lean 4 proof of the Tor long exact sequence has been
pinned as a Lake dependency, imported into this file, or checked by a local
wrapper.  URL-only evidence is therefore rejected as a completion signal.
-/
structure ExternalTorLongExactIntegrationGate where
  externalLean4ProofLocated : Bool
  pinnedDependencyInLakeClosure : Bool
  importedByLocalWrapper : Bool
  localWrapperChecked : Bool
  concreteIntegrationBlockerRecorded : Bool
  urlOnlyEvidenceAcceptedAsCompletion : Bool
  completionClaimAllowed : Bool

/--
Current child-task gate value for external Tor long-exact-sequence proofs.

If a later audit locates an external Lean 4 proof, this value must not be flipped
to completion until the proof is either pinned/imported/checked locally or a
concrete integration blocker is recorded outside any completed state.
-/
def torLongExactExternalIntegrationGate : ExternalTorLongExactIntegrationGate where
  externalLean4ProofLocated := false
  pinnedDependencyInLakeClosure := false
  importedByLocalWrapper := false
  localWrapperChecked := false
  concreteIntegrationBlockerRecorded := false
  urlOnlyEvidenceAcceptedAsCompletion := false
  completionClaimAllowed := false

/-- The current repo-local gate does not accept URL-only evidence as completion. -/
theorem torLongExactExternalIntegrationGate_rejects_url_only_completion :
    torLongExactExternalIntegrationGate.urlOnlyEvidenceAcceptedAsCompletion = false :=
  rfl

/-- The current repo-local gate permits no terminal Tor long-exact completion claim. -/
theorem torLongExactExternalIntegrationGate_no_completion_claim :
    torLongExactExternalIntegrationGate.completionClaimAllowed = false :=
  rfl

/--
No external Tor long-exact proof is currently inside the repo-local validation
closure: it is not pinned, imported by a local wrapper, or checked here.
-/
theorem torLongExactExternalIntegrationGate_not_repo_local_closed :
    torLongExactExternalIntegrationGate.pinnedDependencyInLakeClosure = false ∧
      torLongExactExternalIntegrationGate.importedByLocalWrapper = false ∧
      torLongExactExternalIntegrationGate.localWrapperChecked = false := by
  exact ⟨rfl, rfl, rfl⟩

/--
Statement-shape package for the terminal family of Tor functor properties.

The fields are proof obligations, not assumptions used to prove a theorem here.
They isolate the missing closure target: a later integrator must either prove
these fields in the repo, import them from mathlib, or pin an external Lean 4
dependency that supplies them.
-/
structure TorPropertyPackage : Type (max u v) where
  balancedComparison : ∀ n : ℕ, TorFunctor C n ≅ TorPrimeFunctor C n
  naturalityOfConnectingMorphisms : Prop
  longExactFromShortExactFirstVariable : Prop
  longExactFromShortExactSecondVariable : Prop
  compatibilityWithHomologySequence : Prop
  naturality_holds : naturalityOfConnectingMorphisms
  longExact_first_holds : longExactFromShortExactFirstVariable
  longExact_second_holds : longExactFromShortExactSecondVariable
  homologySequence_compatibility_holds : compatibilityWithHomologySequence
  higherTorSecondProjectiveVanishes :
    ∀ (X Y : C) [Projective Y] (n : ℕ),
      IsZero (((TorFunctor C (n + 1)).obj X).obj Y)
  higherTorFirstProjectiveVanishes :
    ∀ (X Y : C) [Projective X] (n : ℕ),
      IsZero (((TorPrimeFunctor C (n + 1)).obj X).obj Y)

/--
Stage1 normalized statement candidate for THM-M-0008.

It asserts the existence of a terminal package bundling balanced Tor, naturality,
long exact sequence, homology-sequence compatibility, and projective-vanishing
properties in a monoidal abelian category with projective resolutions.
-/
def StatementShape : Prop :=
  Nonempty (TorPropertyPackage C)

/-- The statement-shape definition unfolds to nonemptiness of the terminal package. -/
theorem statementShape_iff_nonempty :
    StatementShape C ↔ Nonempty (TorPropertyPackage C) :=
  Iff.rfl

/-! ## Audit probes -/

#check CategoryTheory.Tor
#check CategoryTheory.Tor'
#check CategoryTheory.isZero_Tor_succ_of_projective
#check CategoryTheory.isZero_Tor'_succ_of_projective
#check CategoryTheory.Functor.leftDerived
#check CategoryTheory.NatTrans.leftDerived
#check CategoryTheory.ShortComplex.ShortExact.δ
#check ShortComplex.ShortExact
#check BalancedComparisonHypothesisPackage
#check BalancedComparisonStatementShape
#check balancedComparison_of_package

end S1_M_101
end Stage1
end AwesomeTheorems
