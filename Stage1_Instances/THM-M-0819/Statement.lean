import Mathlib.Order.Antichain

set_option autoImplicit false

/-!
# THM-M-0819: Dilworth's primary finite-width statement

This module freezes Theorem 1.1 from Dilworth's 1950 paper. It states the
arbitrary-poset, finite-width decomposition theorem, not the modern finite-poset
minimum/maximum equality. It contains no proof of Dilworth's theorem.
-/

namespace Stage1Instances.THM_M_0819

universe u

/-- A set has exactly `k` elements when it is equivalent to `Fin k`. -/
def HasExactly {α : Type u} (k : Nat) (s : Set α) : Prop := Nonempty (s ≃ Fin k)

/-- A dependent set contains two distinct comparable elements. -/
def IsDependent {α : Type u} [LE α] (s : Set α) : Prop :=
  ∃ x ∈ s, ∃ y ∈ s, x ≠ y ∧ (x ≤ y ∨ y ≤ x)

/-- The carrier is the disjoint set sum of the indexed chain family. -/
def IsDisjointChainDecomposition {α : Type u} [LE α]
    (k : Nat) (C : Fin k → Set α) : Prop :=
  (∀ i, IsChain (fun x y : α => x ≤ y) (C i)) ∧
    ∀ x : α, ∃! i, x ∈ C i

/--
Dilworth's Theorem 1.1 in its primary arbitrary-poset finite-width form.

If every `(k + 1)`-element subset is dependent and some `k`-element subset is
independent, then the carrier is a set sum of `k` disjoint chains.
-/
def DilworthPrimaryTarget : Prop :=
  ∀ (α : Type u) [PartialOrder α] (k : Nat),
    (∀ s : Set α, HasExactly (k + 1) s → IsDependent s) →
    (∃ s : Set α, HasExactly k s ∧ IsAntichain (fun x y : α => x ≤ y) s) →
    ∃ C : Fin k → Set α, IsDisjointChainDecomposition k C

/-- The same target with chain decomposition expanded at the boundary. -/
def ExpandedDilworthPrimaryTarget : Prop :=
  ∀ (α : Type u) [PartialOrder α] (k : Nat),
    (∀ s : Set α, HasExactly (k + 1) s → IsDependent s) →
    (∃ s : Set α, HasExactly k s ∧ IsAntichain (fun x y : α => x ≤ y) s) →
    ∃ C : Fin k → Set α,
      (∀ i, IsChain (fun x y : α => x ≤ y) (C i)) ∧
        ∀ x : α, ∃! i, x ∈ C i

/-- Expanding the chain-decomposition predicate does not change the target. -/
theorem dilworthPrimaryTarget_iff_expanded :
    DilworthPrimaryTarget.{u} ↔ ExpandedDilworthPrimaryTarget.{u} := by
  rfl

/-! Structural mutations used only by the statement-identity checker. -/

/-- Removed-hypothesis mutation: no independent `k`-set must be attained. -/
def mutationRemovedIndependentWitness : Prop :=
  ∀ (α : Type u) [PartialOrder α] (k : Nat),
    (∀ s : Set α, HasExactly (k + 1) s → IsDependent s) →
    ∃ C : Fin k → Set α, IsDisjointChainDecomposition k C

/-- Changed-domain mutation: the arbitrary poset is fixed to the natural numbers. -/
def mutationChangedToNatDomain : Prop :=
  ∀ k : Nat,
    (∀ s : Set Nat, HasExactly (k + 1) s → IsDependent s) →
    (∃ s : Set Nat, HasExactly k s ∧ IsAntichain (fun x y : Nat => x ≤ y) s) →
    ∃ C : Fin k → Set Nat, IsDisjointChainDecomposition k C

/-- Changed-scope mutation: `k` is existential rather than universally bound. -/
def mutationChangedWidthBinderScope : Prop :=
  ∀ (α : Type u) [PartialOrder α],
    ∃ k : Nat,
      (∀ s : Set α, HasExactly (k + 1) s → IsDependent s) →
      (∃ s : Set α, HasExactly k s ∧ IsAntichain (fun x y : α => x ≤ y) s) →
      ∃ C : Fin k → Set α, IsDisjointChainDecomposition k C

/-- Boundary mutation: the `k = 0` case is excluded. -/
def mutationExcludesZeroWidth : Prop :=
  ∀ (α : Type u) [PartialOrder α] (k : Nat),
    0 < k →
    (∀ s : Set α, HasExactly (k + 1) s → IsDependent s) →
    (∃ s : Set α, HasExactly k s ∧ IsAntichain (fun x y : α => x ≤ y) s) →
    ∃ C : Fin k → Set α, IsDisjointChainDecomposition k C

#check_failure
  (rfl : DilworthPrimaryTarget.{u} = mutationRemovedIndependentWitness.{u})
#check_failure
  (rfl : DilworthPrimaryTarget.{u} = mutationChangedToNatDomain)
#check_failure
  (rfl : DilworthPrimaryTarget.{u} = mutationChangedWidthBinderScope.{u})
#check_failure
  (rfl : DilworthPrimaryTarget.{u} = mutationExcludesZeroWidth.{u})

/-- The hypotheses at width zero force the carrier to be empty. -/
theorem zeroWidth_forces_isEmpty
    (α : Type u) [PartialOrder α]
    (hdep : ∀ s : Set α, HasExactly 1 s → IsDependent s) : IsEmpty α := by
  refine ⟨fun x => ?_⟩
  have hsingle : HasExactly 1 ({x} : Set α) := by
    let e : ({x} : Set α) ≃ Fin 1 := {
      toFun _ := 0
      invFun _ := ⟨x, Set.mem_singleton x⟩
      left_inv y := Subtype.ext (Set.mem_singleton_iff.mp y.2).symm
      right_inv i := Subsingleton.elim _ _
    }
    exact ⟨e⟩
  obtain ⟨a, ha, b, hb, hab, _⟩ := hdep {x} hsingle
  exact hab ((Set.mem_singleton_iff.mp ha).trans (Set.mem_singleton_iff.mp hb).symm)

/-- The zero-indexed family is the required decomposition of an empty carrier. -/
theorem zeroWidth_decomposition
    (α : Type u) [PartialOrder α] [IsEmpty α] :
    ∃ C : Fin 0 → Set α, IsDisjointChainDecomposition 0 C := by
  let C : Fin 0 → Set α := Fin.elim0
  refine ⟨C, ?_⟩
  constructor
  · intro i
    exact Fin.elim0 i
  · intro x
    exact isEmptyElim x

/-- A singleton poset has the expected one-chain decomposition. -/
theorem singletonWidth_decomposition :
    ∃ C : Fin 1 → Set (Fin 1), IsDisjointChainDecomposition 1 C := by
  let C : Fin 1 → Set (Fin 1) := fun _ => Set.univ
  refine ⟨C, ?_⟩
  constructor
  · intro i
    exact Set.subsingleton_univ.isChain
  · intro x
    refine ⟨0, Set.mem_univ x, ?_⟩
    intro i _hi
    exact Subsingleton.elim i 0

#print axioms dilworthPrimaryTarget_iff_expanded
#print axioms zeroWidth_forces_isEmpty
#print axioms zeroWidth_decomposition
#print axioms singletonWidth_decomposition

end Stage1Instances.THM_M_0819

set_option pp.explicit true in
set_option pp.universes true in
#print Stage1Instances.THM_M_0819.DilworthPrimaryTarget
