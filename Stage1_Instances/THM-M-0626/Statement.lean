import Mathlib.Topology.Connected.Basic

/-!
# THM-M-0626: continuous images preserve connectedness

This module freezes the globally continuous set-image formulation selected from the catalog claim
and the pinned Stacks Project statement. It checks the relationship to mathlib's more general
`ContinuousOn` formulation but does not prove the canonical target.
-/

namespace Stage1Instances.THM_M_0626

universe u v

/-- A globally continuous map sends every connected subset to a connected direct image.

Here `IsConnected` is mathlib's ordinary, nonempty connectedness predicate, so nonemptiness is not
a second hypothesis.
-/
def ConnectedImageTarget : Prop :=
  ∀ {α : Type u} {β : Type v} [TopologicalSpace α] [TopologicalSpace β]
    {s : Set α}, IsConnected s → ∀ f : α → β, Continuous f → IsConnected (f '' s)

/-- Expansion fixing mathlib's nonempty convention for both occurrences of connectedness. -/
def ExpandedConnectedImageTarget : Prop :=
  ∀ {α : Type u} {β : Type v} [TopologicalSpace α] [TopologicalSpace β]
    {s : Set α},
      (s.Nonempty ∧ IsPreconnected s) →
        ∀ f : α → β, Continuous f → (f '' s).Nonempty ∧ IsPreconnected (f '' s)

/-- Checked definitional transport to the binder-complete connectedness expansion. -/
theorem connectedImageTarget_iff_expanded :
    ConnectedImageTarget.{u, v} ↔ ExpandedConnectedImageTarget.{u, v} :=
  Iff.rfl

/-- Mathlib's sharper local-continuity form, recorded as an alternate rather than as the root. -/
def ContinuousOnConnectedImageTarget : Prop :=
  ∀ {α : Type u} {β : Type v} [TopologicalSpace α] [TopologicalSpace β]
    {s : Set α}, IsConnected s → ∀ f : α → β, ContinuousOn f s → IsConnected (f '' s)

/-- The local-continuity alternate implies the globally continuous canonical statement. -/
theorem continuousOnTarget_implies_connectedImageTarget :
    ContinuousOnConnectedImageTarget.{u, v} → ConnectedImageTarget.{u, v} := by
  intro h α β _ _ s hs f hf
  exact h hs f hf.continuousOn

-- Structural mutations elaborate separately and must fail identity checks against the root.
def mutationRemovedConnectedness : Prop :=
  ∀ {α : Type u} {β : Type v} [TopologicalSpace α] [TopologicalSpace β]
    {s : Set α}, ∀ f : α → β, Continuous f → IsConnected (f '' s)

def mutationRemovedContinuity : Prop :=
  ∀ {α : Type u} {β : Type v} [TopologicalSpace α] [TopologicalSpace β]
    {s : Set α}, IsConnected s → ∀ f : α → β, IsConnected (f '' s)

def mutationChangedDomain : Prop :=
  ∀ {α : Type u} [TopologicalSpace α] {s : Set α},
    IsConnected s → ∀ f : α → α, Continuous f → IsConnected (f '' s)

def mutationChangedBinderScope : Prop :=
  ∀ {α : Type u} {β : Type v} [TopologicalSpace α] [TopologicalSpace β]
    {s : Set α}, IsConnected s →
      ∃ f : α → β, Continuous f ∧ IsConnected (f '' s)

def mutationAllowsEmptySource : Prop :=
  ∀ {α : Type u} {β : Type v} [TopologicalSpace α] [TopologicalSpace β]
    {s : Set α}, IsPreconnected s →
      ∀ f : α → β, Continuous f → IsPreconnected (f '' s)

#check_failure (rfl : ConnectedImageTarget.{u, v} = mutationRemovedConnectedness.{u, v})
#check_failure (rfl : ConnectedImageTarget.{u, v} = mutationRemovedContinuity.{u, v})
#check_failure (rfl : ConnectedImageTarget.{u, v} = mutationChangedDomain.{u})
#check_failure (rfl : ConnectedImageTarget.{u, v} = mutationChangedBinderScope.{u, v})
#check_failure (rfl : ConnectedImageTarget.{u, v} = mutationAllowsEmptySource.{u, v})

/-- The chosen ordinary-connectedness convention excludes the empty source. -/
theorem empty_source_not_connected {α : Type u} [TopologicalSpace α] :
    ¬IsConnected (∅ : Set α) := by
  rintro ⟨⟨x, hx⟩, _⟩
  exact hx

/-- Singleton sources remain inside the target's boundary, with no continuity premise needed. -/
theorem singleton_image_connected {α : Type u} {β : Type v} [TopologicalSpace α]
    [TopologicalSpace β] (x : α) (f : α → β) : IsConnected (f '' ({x} : Set α)) := by
  simpa using (isConnected_singleton (α := β) (x := f x))

/-- Constant maps remain inside the target's boundary for every connected source. -/
theorem constant_image_connected {α : Type u} {β : Type v} [TopologicalSpace α]
    [TopologicalSpace β] {s : Set α} (hs : IsConnected s) (y : β) :
    IsConnected ((fun _ : α ↦ y) '' s) := by
  have hImage : (fun _ : α ↦ y) '' s = {y} := by
    ext z
    constructor
    · rintro ⟨x, _, rfl⟩
      rfl
    · intro hz
      rw [Set.mem_singleton_iff] at hz
      subst z
      obtain ⟨x, hx⟩ := hs.nonempty
      exact ⟨x, hx, rfl⟩
  rw [hImage]
  exact isConnected_singleton

end Stage1Instances.THM_M_0626

#print axioms Stage1Instances.THM_M_0626.connectedImageTarget_iff_expanded
#print axioms Stage1Instances.THM_M_0626.continuousOnTarget_implies_connectedImageTarget

set_option pp.explicit true in
set_option pp.universes true in
#print Stage1Instances.THM_M_0626.ConnectedImageTarget
