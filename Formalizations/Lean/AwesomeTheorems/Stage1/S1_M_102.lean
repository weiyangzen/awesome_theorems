import Mathlib.Algebra.Homology.DerivedCategory.Ext.ExactSequences

/-!
# S1-M-102 / THM-M-0009

Stage1 Lean artifact for the long exact sequences of Ext groups.

The pinned mathlib dependency already contains the categorical Ext construction
for abelian categories and the covariant/contravariant long exact sequences
associated to a short exact sequence.  This file records a repo-local wrapper
around those exactness statements and a compact statement-shape proposition for
the Stage1 slot.
-/

noncomputable section

open CategoryTheory

universe w v u

namespace AwesomeTheorems.Stage1.S1_M_102

variable {C : Type u} [Category.{v} C] [Abelian C] [HasExt.{w} C]

/--
Statement-shape candidate for `Ext` long exact sequences.

For every short exact short complex in an abelian category with mathlib `Ext`
groups, both the covariant sequence
`Ext X S.X₁ n₀ → Ext X S.X₂ n₀ → Ext X S.X₃ n₀ →
 Ext X S.X₁ n₁ → Ext X S.X₂ n₁ → Ext X S.X₃ n₁`
and the contravariant sequence
`Ext S.X₃ Y n₀ → Ext S.X₂ Y n₀ → Ext S.X₁ Y n₀ →
 Ext S.X₃ Y n₁ → Ext S.X₂ Y n₁ → Ext S.X₁ Y n₁`
are exact when the degree shifts advance by one.
-/
def StatementShape (C : Type u) [Category.{v} C] [Abelian C] [HasExt.{w} C] : Prop :=
  (∀ (X : C) (S : ShortComplex C) (hS : S.ShortExact)
      (n₀ n₁ : ℕ) (h : n₀ + 1 = n₁),
      (Abelian.Ext.covariantSequence X hS n₀ n₁ h).Exact) ∧
    (∀ (Y : C) (S : ShortComplex C) (hS : S.ShortExact)
      (n₀ n₁ : ℕ) (h : 1 + n₀ = n₁),
      (Abelian.Ext.contravariantSequence hS Y n₀ n₁ h).Exact)

/-- Repo-local wrapper for mathlib's covariant Ext long exact sequence. -/
theorem covariantSequence_exact_wrapper
    (X : C) {S : ShortComplex C} (hS : S.ShortExact)
    (n₀ n₁ : ℕ) (h : n₀ + 1 = n₁) :
    (Abelian.Ext.covariantSequence X hS n₀ n₁ h).Exact :=
  Abelian.Ext.covariantSequence_exact X hS n₀ n₁ h

/-- Repo-local wrapper for mathlib's contravariant Ext long exact sequence. -/
theorem contravariantSequence_exact_wrapper
    (Y : C) {S : ShortComplex C} (hS : S.ShortExact)
    (n₀ n₁ : ℕ) (h : 1 + n₀ = n₁) :
    (Abelian.Ext.contravariantSequence hS Y n₀ n₁ h).Exact :=
  Abelian.Ext.contravariantSequence_exact hS Y n₀ n₁ h

/--
Repo-local wrapper for the naturality of the Ext class attached to a morphism
of short exact complexes.
-/
theorem extClass_naturality_wrapper
    {S₁ S₂ : ShortComplex C} (h₁ : S₁.ShortExact) (h₂ : S₂.ShortExact)
    (f : S₁ ⟶ S₂) :
    h₁.extClass.comp (Abelian.Ext.mk₀ f.τ₁) (add_zero 1) =
      (Abelian.Ext.mk₀ f.τ₃).comp h₂.extClass (zero_add 1) :=
  ShortComplex.ShortExact.extClass_naturality h₁ h₂ f

/--
The Stage1 statement shape is discharged by the pinned mathlib Ext exact
sequence API.  This is a local wrapper over upstream mathlib proof bodies, not
a new proof of the homological algebra development.
-/
theorem statementShape_of_mathlib : StatementShape C :=
  ⟨fun X _S hS n₀ n₁ h ↦ covariantSequence_exact_wrapper X hS n₀ n₁ h,
    fun Y _S hS n₀ n₁ h ↦ contravariantSequence_exact_wrapper Y hS n₀ n₁ h⟩

/--
Policy witness for child task `S1-M-102-C003`: the Stage1 public completion
target for `Ext` long exact sequences is the two-branch statement shape, not
only one variance direction.  Thus a completed public audit should account for
both mathlib anchors `Abelian.Ext.covariantSequence_exact` and
`Abelian.Ext.contravariantSequence_exact`.
-/
theorem publicCompletion_requires_both_branches :
    (∀ (X : C) (S : ShortComplex C) (hS : S.ShortExact)
        (n₀ n₁ : ℕ) (h : n₀ + 1 = n₁),
        (Abelian.Ext.covariantSequence X hS n₀ n₁ h).Exact) ∧
      (∀ (Y : C) (S : ShortComplex C) (hS : S.ShortExact)
        (n₀ n₁ : ℕ) (h : 1 + n₀ = n₁),
        (Abelian.Ext.contravariantSequence hS Y n₀ n₁ h).Exact) :=
  statementShape_of_mathlib

/-- A checked metadata row for the public theorem-tree route of the Ext LES. -/
structure TheoremTreeLink where
  node : String
  role : String
  upstreamAnchors : List String
  status : String
deriving Repr, DecidableEq

/--
Integration-ready theorem-tree note for child task `S1-M-102-C004`.

This is checked metadata for the public backfill.  It records the mathlib route
from a short exact complex to the Ext long exact sequence: the short exact
complex supplies `ShortExact.extClass`; the associated single triangle is
distinguished by `singleTriangle_distinguished`; and the exactness packages are
transported from `DerivedCategory.HomologySequence.exact₁/exact₂/exact₃` to the
covariant and contravariant Ext sequence wrappers.
-/
def publicTheoremTreeNote : List TheoremTreeLink := [
  { node := "P04.1.short_exact_to_ext_class",
    role := "Construct the connecting Ext class attached to a short exact short complex.",
    upstreamAnchors := [
      "ShortComplex.ShortExact.extClass",
      "ShortComplex.ShortExact.extClass_naturality"
    ],
    status := "checked_upstream_anchor" },
  { node := "P04.2.short_exact_to_distinguished_triangle",
    role := "Use the single-triangle construction as the distinguished-triangle source for homology-sequence exactness.",
    upstreamAnchors := [
      "ShortComplex.ShortExact.singleTriangle_distinguished"
    ],
    status := "checked_upstream_anchor" },
  { node := "P04.3.homology_sequence_exactness",
    role := "Apply the three homology-sequence exactness positions that become the repeating exactness blocks of the Ext sequence.",
    upstreamAnchors := [
      "DerivedCategory.HomologySequence.exact₁",
      "DerivedCategory.HomologySequence.exact₂",
      "DerivedCategory.HomologySequence.exact₃"
    ],
    status := "checked_upstream_anchor" },
  { node := "P04.4.ext_sequence_transport",
    role := "Transport homology-sequence exactness through Ext equivalences and the Ext-class boundary map.",
    upstreamAnchors := [
      "Abelian.Ext.covariant_sequence_exact₁'",
      "Abelian.Ext.covariant_sequence_exact₂'",
      "Abelian.Ext.covariant_sequence_exact₃'",
      "Abelian.Ext.contravariant_sequence_exact₁'",
      "Abelian.Ext.contravariant_sequence_exact₂'",
      "Abelian.Ext.contravariant_sequence_exact₃'"
    ],
    status := "checked_upstream_anchor" },
  { node := "P04.5.public_wrapper_gate",
    role := "Expose both variance directions as the repo-local Stage1 wrapper for the public Ext long exact sequence item.",
    upstreamAnchors := [
      "Abelian.Ext.covariantSequence_exact",
      "Abelian.Ext.contravariantSequence_exact",
      "AwesomeTheorems.Stage1.S1_M_102.statementShape_of_mathlib"
    ],
    status := "local_wrapper_upstream_mathlib" }
]

/-- The public theorem-tree note has the five P04 rows expected by this child. -/
theorem publicTheoremTreeNote_length : publicTheoremTreeNote.length = 5 := rfl

/--
Checked integration note for child task `S1-M-102-C005`.

The local wrapper is intentionally not exposed through a shared Lean aggregator
in this worker pass.  If aggregator exposure is desired, an integrator should
add the import in a separate patch and rerun the relevant aggregate build.
-/
def aggregatorExposurePlan : TheoremTreeLink :=
  { node := "P05.aggregator_exposure",
    role := "Add import AwesomeTheorems.Stage1.S1_M_102 only in a separate integrator patch, then rerun the relevant aggregate build.",
    upstreamAnchors := [
      "Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_102.lean",
      "Formalizations/Lean/AwesomeTheorems.lean"
    ],
    status := "integrator_patch_required_no_child_aggregator_edit" }

/-- The P05 integration note records that this worker did not edit aggregators. -/
theorem aggregatorExposurePlan_status :
    aggregatorExposurePlan.status =
      "integrator_patch_required_no_child_aggregator_edit" := rfl

/--
Checked integration note for child task `S1-M-102-C006`.

The public blueprint/todo/README status update is intentionally serial
integrator work.  It should happen only after the integrator accepts the
repo-local mathlib wrapper as satisfying the Stage1 completion gate.
-/
def publicStatusBackfillPlan : TheoremTreeLink :=
  { node := "P06.public_status_backfill",
    role := "Update Docs/Stage1_Blueprint.md, Docs/todos_20260430.md, and README.md consistently only after accepting the local Ext wrapper as the Stage1 completion gate.",
    upstreamAnchors := [
      "AwesomeTheorems.Stage1.S1_M_102.statementShape_of_mathlib",
      "AwesomeTheorems.Stage1.S1_M_102.publicCompletion_requires_both_branches",
      "AwesomeTheorems.Stage1.S1_M_102.publicTheoremTreeNote",
      "AwesomeTheorems.Stage1.S1_M_102.aggregatorExposurePlan"
    ],
    status := "serial_public_doc_backfill_required_after_integrator_acceptance" }

/-- The P06 integration note records a serial public-document backfill gate. -/
theorem publicStatusBackfillPlan_status :
    publicStatusBackfillPlan.status =
      "serial_public_doc_backfill_required_after_integrator_acceptance" := rfl

/-- mathlib anchor modules audited for this Stage1 slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Algebra.Homology.DerivedCategory.Ext.Basic",
  "Mathlib.Algebra.Homology.DerivedCategory.Ext.ExtClass",
  "Mathlib.Algebra.Homology.DerivedCategory.Ext.ExactSequences",
  "Mathlib.Algebra.Homology.DerivedCategory.HomologySequence",
  "Mathlib.Algebra.Homology.DerivedCategory.ShortExact",
  "Mathlib.Algebra.Homology.ShortComplex.ShortExact"
]

/-- Pinned mathlib revision audited for this Stage1 slot. -/
def pinnedMathlibRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/--
Main upstream theorem names checked in the pinned mathlib dependency.

The first three entries are the exact anchors requested by the Stage1 child
task `S1-M-102-C002`.
-/
def mathlibAnchorTheorems : List String := [
  "Abelian.Ext.covariantSequence_exact",
  "Abelian.Ext.contravariantSequence_exact",
  "ShortComplex.ShortExact.extClass_naturality",
  "Abelian.Ext.covariantSequence",
  "Abelian.Ext.contravariantSequence",
  "ShortComplex.ShortExact.extClass",
  "ShortComplex.ShortExact.singleTriangle_distinguished",
  "DerivedCategory.HomologySequence.exact₁",
  "DerivedCategory.HomologySequence.exact₂",
  "DerivedCategory.HomologySequence.exact₃"
]

#check StatementShape
#check covariantSequence_exact_wrapper
#check contravariantSequence_exact_wrapper
#check extClass_naturality_wrapper
#check statementShape_of_mathlib
#check publicCompletion_requires_both_branches
#check publicTheoremTreeNote
#check publicTheoremTreeNote_length
#check aggregatorExposurePlan
#check aggregatorExposurePlan_status
#check publicStatusBackfillPlan
#check publicStatusBackfillPlan_status
#check pinnedMathlibRevision
#check Abelian.Ext.covariantSequence_exact
#check Abelian.Ext.contravariantSequence_exact
#check ShortComplex.ShortExact.extClass
#check ShortComplex.ShortExact.singleTriangle_distinguished
#check ShortComplex.ShortExact.extClass_naturality
#check DerivedCategory.HomologySequence.exact₁
#check DerivedCategory.HomologySequence.exact₂
#check DerivedCategory.HomologySequence.exact₃

end AwesomeTheorems.Stage1.S1_M_102
