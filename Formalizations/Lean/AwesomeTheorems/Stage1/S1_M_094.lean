import Mathlib.CategoryTheory.Abelian.RightDerived
import Mathlib.Algebra.Homology.SpectralObject.SpectralSequence
import Mathlib.Algebra.Homology.HomologySequence

/-!
# S1-M-094 / THM-M-0007: Grothendieck spectral sequence theorem

This file records a conservative Lean 4 boundary for the Grothendieck spectral
sequence for a composite of derived functors.  The pinned mathlib snapshot has
right-derived functors of additive functors between abelian categories, long
exact homology-sequence infrastructure, and general spectral-sequence objects.
It does not expose a terminal theorem identifying an `E₂` page
`R^p G (R^q F X)` with an abutment `R^(p+q) (G ⋙ F) X`.

The declarations below therefore provide checked statement shapes and wrappers
around existing mathlib facts only.  They do not prove the target theorem.
-/

noncomputable section

open CategoryTheory CategoryTheory.Limits

set_option linter.unusedSectionVars false

universe uC vC uD vD uE vE

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_094

variable {C : Type uC} [Category.{vC} C] [Abelian C] [HasInjectiveResolutions C]
variable {D : Type uD} [Category.{vD} D] [Abelian D] [HasInjectiveResolutions D]
variable {E : Type uE} [Category.{vE} E] [Abelian E]

/-- The mathlib object `R^n F` for an additive functor between abelian categories. -/
abbrev RightDerivedFunctor (F : C ⥤ D) [F.Additive] (n : ℕ) : C ⥤ D :=
  F.rightDerived n

/-- The expected `E₂^{p,q}` object in the Grothendieck spectral sequence. -/
abbrev E₂Term (F : C ⥤ D) (G : D ⥤ E) [F.Additive] [G.Additive]
    (X : C) (p q : ℕ) : E :=
  (G.rightDerived p).obj ((F.rightDerived q).obj X)

/-- The expected abutment object `R^n (F ⋙ G)(X)`. -/
abbrev CompositeDerivedTarget (F : C ⥤ D) (G : D ⥤ E)
    [F.Additive] [G.Additive] (X : C) (n : ℕ) : E :=
  ((F ⋙ G).rightDerived n).obj X

/--
The usual acyclicity hypothesis for Grothendieck's spectral sequence:
`F` sends injective objects of `C` to objects that are acyclic for `G`.
-/
def GrothendieckAcyclicity (F : C ⥤ D) (G : D ⥤ E)
    [F.Additive] [G.Additive] : Prop :=
  ∀ (I : C), Injective I → ∀ n : ℕ, 0 < n → IsZero ((G.rightDerived n).obj (F.obj I))

/--
Data that a future local proof or pinned upstream theorem must construct.

The abstract `spectralSequence` field avoids claiming that the current file has
constructed the Grothendieck spectral sequence.  The two isomorphism families
freeze the intended `E₂` page and abutment in mathlib's existing right-derived
functor notation.
-/
structure GrothendieckSpectralSequenceBoundary
    (F : C ⥤ D) (G : D ⥤ E) [F.Additive] [G.Additive] (X : C) where
  spectralSequence : Type (max (max uE vE) 1)
  e₂Page : ℕ → ℕ → E
  abutment : ℕ → E
  e₂PageIso : ∀ p q : ℕ, e₂Page p q ≅ E₂Term F G X p q
  abutmentIso : ∀ n : ℕ, abutment n ≅ CompositeDerivedTarget F G X n
  naturalityInX : Prop
  convergenceToCompositeDerived : Prop

/--
Stage1 statement-shape candidate for the Grothendieck spectral sequence theorem.

For left-exact additive functors `F` and `G`, assuming the standard acyclicity
condition, a later proof should construct spectral-sequence data whose `E₂` page
is `R^p G (R^q F X)` and whose abutment is `R^(p+q) (F ⋙ G)(X)`.
-/
def StatementShape : Prop :=
  ∀ (F : C ⥤ D) (G : D ⥤ E) [F.Additive] [G.Additive],
    PreservesFiniteLimits F →
      PreservesFiniteLimits G →
        GrothendieckAcyclicity F G →
          ∀ X : C, Nonempty (GrothendieckSpectralSequenceBoundary F G X)

/-!
## External integration candidate

The Riou derived-categories project contains a Lean 4 anchor for the terminal
theorem family, but it is not in this repository's Lake closure.  The record
below is intentionally data only: importing the external theorem would require
a separate dependency decision because the candidate uses Lean `v4.21.0-rc3`
and a forked mathlib revision, while this repository currently targets
Lean `v4.29.0`.
-/

/-- Metadata for an external Lean project that may close this Stage1 slot once pinned. -/
structure UpstreamClosureCandidate where
  project : String
  projectRevision : String
  dependency : String
  dependencyRevision : String
  toolchain : String
  sourceModule : String
  theoremNames : List String
  repoLocalStatus : String
deriving Repr

/--
Integration candidate for a future pinned upstream closure of the Grothendieck
spectral sequence theorem.

This declaration does not assert that the theorem has been imported or checked
in this repository; `repoLocalStatus` records the current blocker explicitly.
-/
def riouGrothendieckSpectralSequenceCandidate : UpstreamClosureCandidate where
  project := "joelriou/lean-derived-categories"
  projectRevision := "c1d75ecdb3bbb9d85b161bade0aadfa1c2b7f6e4"
  dependency := "joelriou/mathlib4"
  dependencyRevision := "d886e33fd2f029f2304dfd20d9069d5fa7f3aa1a"
  toolchain := "leanprover/lean4:v4.21.0-rc3"
  sourceModule := "Mathlib.Algebra.Homology.SpectralSequence.Examples.Grothendieck"
  theoremNames :=
    [ "DerivedCategory.Plus.grothendieckSpectralSequence",
      "DerivedCategory.Plus.grothendieckSpectralSequence.page₂Iso",
      "DerivedCategory.Plus.grothendieckSpectralSequence.stronglyConvergesToInDegree'",
      "DerivedCategory.Plus.grothendieckSpectralSequence.stronglyConvergesTo" ]
  repoLocalStatus :=
    "external_upstream_anchor_only; blocked until pinned/imported/checked or ported locally"

/-!
## Route decision

The old-toolchain candidate is useful as a porting source, but not as a direct
Lake dependency for this repository: a normal Lean dependency must share the
current toolchain and mathlib API.  The current repo-local closure has no
compatible `Mathlib.Algebra.Homology.SpectralSequence.Examples.Grothendieck`
module, so the actionable route is a port to the repo's Lean `v4.29.0` stack,
or equivalently waiting for exactly that port to land in a compatible pinned
mathlib before adding a wrapper.
-/

/-- Audited route decision for closing this Stage1 theorem slot. -/
structure IntegrationRouteDecision where
  decisionDate : String
  selectedRoute : String
  rejectedRoutes : List String
  localToolchain : String
  localMathlibRevision : String
  upstreamMainProbe : String
  localPortBlockers : List String
  repoLocalStatus : String
deriving Repr

/--
Decision for the Grothendieck spectral-sequence integration route.

This is checked metadata only.  It records that the local theorem still needs a
port or a future compatible upstream mathlib import before any wrapper theorem
can be claimed.
-/
def grothendieckSpectralSequenceRouteDecision_20260501 : IntegrationRouteDecision where
  decisionDate := "2026-05-01"
  selectedRoute := "port_to_repo_lean_v4_29_snapshot"
  rejectedRoutes :=
    [ "do_not_pin_v4_21_0_rc3_project_as_direct_lake_dependency",
      "do_not_wait_without_a_compatible_mathlib_module_or_exact_import_probe" ]
  localToolchain := "leanprover/lean4:v4.29.0"
  localMathlibRevision := "8a178386ffc0f5fef0b77738bb5449d50efeea95"
  upstreamMainProbe :=
    "raw leanprover-community/mathlib4 master path for SpectralSequence/Examples/Grothendieck returned 404 on 2026-05-01"
  localPortBlockers :=
    [ "local mathlib lacks Mathlib.Algebra.Homology.SpectralSequence.Examples.Grothendieck",
      "local mathlib lacks DerivedCategory.Plus.grothendieckSpectralSequence",
      "local mathlib lacks the external RightDerivedFunctorPlus API names used by the candidate, including rightDerivedFunctorPlus, rightDerivedFunctorPlusUnit, and rightDerived'",
      "local mathlib lacks the external TStructure spectral-sequence helper names used by the candidate, including TStructure.spectralSequenceNat and Functor.VanishesOnGEOne" ]
  repoLocalStatus :=
    "not_repo_local_closed; port selected but terminal wrapper remains blocked"

/-!
## Terminal wrapper gate

Child task `S1-M-094-C003` asks for a local wrapper around
`DerivedCategory.Plus.grothendieckSpectralSequence` after the dependency-route
decision.  The decision above selects a port to this repository's Lean
`v4.29.0` stack, but the theorem and its prerequisite API are not yet present
in the local Lake closure.  The following checked metadata is therefore the
strongest safe local artifact for this child: it records the wrapper target and
the exact blocker without manufacturing an unimportable theorem declaration.
-/

/-- Checked record for a terminal wrapper that is blocked by missing local imports. -/
structure TerminalWrapperBlocker where
  requestedWrapper : String
  requestedAuxiliaryWrappers : List String
  attemptedImport : String
  blocker : String
  requiredBeforeCompletion : List String
  repoLocalStatus : String
deriving Repr

/--
Integration gate for the requested Grothendieck spectral-sequence wrapper.

No theorem wrapper is declared here because the target declaration is absent
from the current repository closure.  This preserves the M0387 rule that
anchor-only evidence cannot be marked completed.
-/
def grothendieckSpectralSequenceWrapperBlocker_20260501 :
    TerminalWrapperBlocker where
  requestedWrapper := "DerivedCategory.Plus.grothendieckSpectralSequence"
  requestedAuxiliaryWrappers :=
    [ "DerivedCategory.Plus.grothendieckSpectralSequence.page₂Iso",
      "DerivedCategory.Plus.grothendieckSpectralSequence.stronglyConvergesToInDegree'",
      "DerivedCategory.Plus.grothendieckSpectralSequence.stronglyConvergesTo" ]
  attemptedImport := "Mathlib.Algebra.Homology.SpectralSequence.Examples.Grothendieck"
  blocker :=
    "module and target declarations are absent from the repo-local Lean v4.29.0/mathlib closure"
  requiredBeforeCompletion :=
    [ "port or receive a compatible local Grothendieck spectral-sequence module",
      "make DerivedCategory.Plus.grothendieckSpectralSequence available in this Lake closure",
      "add a theorem/def wrapper that elaborates against the local declaration",
      "validate with cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_094.lean" ]
  repoLocalStatus :=
    "not_repo_local_closed; terminal wrapper cannot be declared until the target theorem imports"

/-!
## Public backfill gate

Child task `S1-M-094-C004` is a public theorem-tree backfill task.  Because the
terminal local wrapper is still blocked, this file can only record the checked
gate decision and the exact theorem names to backfill later; it must not mark
the public theorem tree as closed.
-/

/-- Checked record for the public theorem-tree backfill gate. -/
structure PublicBackfillGate where
  childTask : String
  requestedTheoremTreeNames : List String
  prerequisiteLocalWrapper : String
  localWrapperValidation : String
  publicBackfillDecision : String
  integrationBlocker : String
  repoLocalStatus : String
deriving Repr

/--
Gate for backfilling the public theorem tree with the Grothendieck
spectral-sequence theorem family.

The requested names are integration-ready, but the decision remains blocked
until a repo-local wrapper for the terminal theorem elaborates and validates.
-/
def grothendieckSpectralSequencePublicBackfillGate_20260501 :
    PublicBackfillGate where
  childTask := "S1-M-094-C004"
  requestedTheoremTreeNames :=
    [ "DerivedCategory.Plus.grothendieckSpectralSequence",
      "DerivedCategory.Plus.grothendieckSpectralSequence.page₂Iso",
      "DerivedCategory.Plus.grothendieckSpectralSequence.stronglyConvergesToInDegree'",
      "DerivedCategory.Plus.grothendieckSpectralSequence.stronglyConvergesTo" ]
  prerequisiteLocalWrapper := "DerivedCategory.Plus.grothendieckSpectralSequence"
  localWrapperValidation :=
    "not available; local wrapper cannot be declared against the current Lake closure"
  publicBackfillDecision :=
    "do_not_edit_public_theorem_tree_yet; provide an integrator-ready proposal only"
  integrationBlocker :=
    "the prerequisite local wrapper has not validated in this repository"
  repoLocalStatus :=
    "not_repo_local_closed; public backfill remains blocked by terminal-wrapper integration"

/-!
## Repo-local integration-debt gate

Child task `S1-M-094-C005` keeps the parent theorem open until the
repo-local integration-debt gate is closed.  This is not a proof task by
itself: it is a checked guard against upgrading anchor-only external evidence
to a completed theorem status.
-/

/-- Checked record for the final repo-local integration-debt gate. -/
structure RepoLocalIntegrationDebtGate where
  childTask : String
  externalAnchorStatus : String
  repoLocalWrapperStatus : String
  completionDecision : String
  blockedBy : List String
  closeOnlyAfter : List String
  repoLocalStatus : String
deriving Repr

/--
Gate that keeps `S1-M-094` open.

The external Riou theorem family is useful primary-source evidence, but this
repository has not imported or checked it.  Completion therefore remains
blocked until the theorem family is present in this Lake closure and a local
wrapper validates.
-/
def grothendieckSpectralSequenceRepoLocalIntegrationDebtGate_20260501 :
    RepoLocalIntegrationDebtGate where
  childTask := "S1-M-094-C005"
  externalAnchorStatus :=
    "anchor_only: joelriou/lean-derived-categories c1d75ecdb3bbb9d85b161bade0aadfa1c2b7f6e4 via joelriou/mathlib4 d886e33fd2f029f2304dfd20d9069d5fa7f3aa1a"
  repoLocalWrapperStatus :=
    "absent: DerivedCategory.Plus.grothendieckSpectralSequence is not available in the repo-local Lake closure"
  completionDecision :=
    "keep_open; do_not_mark_anchor_only_evidence_completed"
  blockedBy :=
    [ "external proof uses Lean v4.21.0-rc3 while this repo targets Lean v4.29.0",
      "external proof uses a joelriou/mathlib4 fork not pinned in this repository",
      "local mathlib lacks Mathlib.Algebra.Homology.SpectralSequence.Examples.Grothendieck",
      "no local wrapper for DerivedCategory.Plus.grothendieckSpectralSequence validates yet" ]
  closeOnlyAfter :=
    [ "pin/import/check the external theorem family in this repository, or port it locally",
      "add a repo-local wrapper for DerivedCategory.Plus.grothendieckSpectralSequence",
      "validate with cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_094.lean",
      "then backfill public blueprint/todo status serially" ]
  repoLocalStatus :=
    "repo_local_integration_debt_open; not completed"

/-- Checked wrapper: mathlib's right-derived functor notation for this slot. -/
theorem rightDerivedFunctor_eq (F : C ⥤ D) [F.Additive] (n : ℕ) :
    RightDerivedFunctor F n = F.rightDerived n :=
  rfl

/-- Checked wrapper: injective objects have vanishing higher right-derived functors. -/
theorem isZero_rightDerived_obj_injective_succ
    (F : C ⥤ D) [F.Additive] (n : ℕ) (X : C) [Injective X] :
    IsZero ((F.rightDerived (n + 1)).obj X) := by
  exact Functor.isZero_rightDerived_obj_injective_succ F n X

/-- Checked wrapper: a left-exact additive functor is isomorphic to its zeroth right-derived functor. -/
def rightDerivedZeroIsoSelf (F : C ⥤ D) [F.Additive] [PreservesFiniteLimits F] :
    F.rightDerived 0 ≅ F :=
  F.rightDerivedZeroIsoSelf

/-- Checked wrapper: natural transformations induce maps on right-derived functors. -/
def rightDerivedNatTrans {F G : C ⥤ D} [F.Additive] [G.Additive]
    (α : F ⟶ G) (n : ℕ) :
    F.rightDerived n ⟶ G.rightDerived n :=
  NatTrans.rightDerived α n

/-- mathlib's first-quadrant `E₂` cohomological spectral-sequence object. -/
abbrev E₂CohomologicalSpectralSequenceNat (A : Type uE) [Category.{vE} A] [Abelian A] :=
  CategoryTheory.E₂CohomologicalSpectralSequenceNat A

/-! ## Audit probes -/

#check (fun (F : C ⥤ D) [F.Additive] (n : ℕ) => F.rightDerived n)
#check (fun (F : C ⥤ D) [F.Additive] (n : ℕ) (X : C) [Injective X] =>
  Functor.isZero_rightDerived_obj_injective_succ F n X)
#check (fun (F : C ⥤ D) [F.Additive] [PreservesFiniteLimits F] =>
  F.rightDerivedZeroIsoSelf)
#check (fun {F G : C ⥤ D} [F.Additive] [G.Additive] (α : F ⟶ G) (n : ℕ) =>
  NatTrans.rightDerived α n)
#check (CategoryTheory.E₂CohomologicalSpectralSequenceNat E)
#check CategoryTheory.Abelian.SpectralObject.coreE₂CohomologicalNat
#check HomologicalComplex.HomologySequence.composableArrows₃_exact
#check StatementShape
#check riouGrothendieckSpectralSequenceCandidate
#check grothendieckSpectralSequenceRouteDecision_20260501
#check grothendieckSpectralSequenceWrapperBlocker_20260501
#check grothendieckSpectralSequencePublicBackfillGate_20260501
#check grothendieckSpectralSequenceRepoLocalIntegrationDebtGate_20260501

end S1_M_094
end Stage1
end AwesomeTheorems
