import Mathlib.SetTheory.Cardinal.Order

universe u

namespace Stage1.THM_M_0767

/-- Canonical set-level form of Cantor's theorem. A set is represented by its subtype. -/
def CanonicalTarget : Prop :=
  ∀ (alpha : Type u) (s : Set alpha),
    Cardinal.mk s < Cardinal.mk (Set.powerset s)

/-- The type-level encoding used to check the set/type boundary. -/
def TypeTarget : Prop :=
  ∀ alpha : Type u, Cardinal.mk alpha < Cardinal.mk (Set alpha)

/-- The canonical target has exactly the normalized cardinal-exponential form. -/
theorem canonical_iff_exponential :
    CanonicalTarget.{u} ↔
      ∀ (alpha : Type u) (s : Set alpha), Cardinal.mk s < 2 ^ Cardinal.mk s := by
  simp only [CanonicalTarget, Cardinal.mk_powerset]

/-- The type-level target has the same normalized cardinal-exponential form. -/
theorem type_iff_exponential :
    TypeTarget.{u} ↔ ∀ alpha : Type u, Cardinal.mk alpha < 2 ^ Cardinal.mk alpha := by
  simp only [TypeTarget, Cardinal.mk_set]

/-- Checked transport from the type-level encoding to the set-level canonical encoding. -/
theorem type_to_canonical (h : TypeTarget.{u}) : CanonicalTarget.{u} := by
  intro alpha s
  simpa [Cardinal.mk_powerset, Cardinal.mk_set] using h s

/-- Checked transport from the canonical encoding to the type-level encoding. -/
theorem canonical_to_type (h : CanonicalTarget.{u}) : TypeTarget.{u} := by
  intro alpha
  have hu : Cardinal.mk (Set.univ : Set alpha) = Cardinal.mk alpha :=
    Cardinal.mk_congr (Equiv.Set.univ alpha)
  have hp := h alpha (Set.univ : Set alpha)
  rw [hu, Cardinal.mk_powerset, hu] at hp
  simpa [Cardinal.mk_set] using hp

theorem canonical_iff_type : CanonicalTarget.{u} ↔ TypeTarget.{u} :=
  ⟨canonical_to_type, type_to_canonical⟩

-- Boundary fixtures ensure that no nonemptiness or infinitude assumption entered the target.
example : Cardinal.mk (Set.univ : Set Empty) <
    Cardinal.mk (Set.powerset (Set.univ : Set Empty)) := by
  have hu : Cardinal.mk (Set.univ : Set Empty) = Cardinal.mk Empty :=
    Cardinal.mk_congr (Equiv.Set.univ Empty)
  rw [Cardinal.mk_powerset, hu]
  exact Cardinal.cantor (Cardinal.mk Empty)

example : Cardinal.mk (Set.univ : Set (Fin 3)) <
    Cardinal.mk (Set.powerset (Set.univ : Set (Fin 3))) := by
  have hu : Cardinal.mk (Set.univ : Set (Fin 3)) = Cardinal.mk (Fin 3) :=
    Cardinal.mk_congr (Equiv.Set.univ (Fin 3))
  rw [Cardinal.mk_powerset, hu]
  exact Cardinal.cantor (Cardinal.mk (Fin 3))

-- Direction mutation: reversing the strict inequality must not elaborate from Cantor's theorem.
end Stage1.THM_M_0767

#print Stage1.THM_M_0767.CanonicalTarget
#print Stage1.THM_M_0767.TypeTarget
#print axioms Stage1.THM_M_0767.canonical_iff_exponential
#print axioms Stage1.THM_M_0767.type_iff_exponential
#print axioms Stage1.THM_M_0767.type_to_canonical
#print axioms Stage1.THM_M_0767.canonical_to_type
#print axioms Stage1.THM_M_0767.canonical_iff_type
