import Statement

/-!
# THM-M-0442 obligation composition

Typed interfaces for the frozen Mazur rational-torsion proof architecture.  The
interfaces are premises for later proof work; this module supplies no instance
of them and therefore does not prove Mazur's theorem.
-/

noncomputable section

namespace Stage1Instances.THMM0442.ObligationTree

open Stage1Instances.THMM0442

/-- The group-structure branch, before the numerical restrictions are proved. -/
def TorsionStructureDichotomy (E : WeierstrassCurve Rat) [E.IsElliptic] : Prop :=
  (∃ n : Nat, HasCyclicTorsionOrder E n) ∨
    (∃ m : Nat, HasBicyclicTorsionIndex E m)

/-- A typed boundary between the structural, modular-curve, and arithmetic
parts of the classical proof.  Its fields are uninhabited obligations. -/
structure MazurEngine where
  torsionStructure :
    ∀ (E : WeierstrassCurve Rat) [E.IsElliptic], TorsionStructureDichotomy E
  restrictCyclic :
    ∀ (E : WeierstrassCurve Rat) [E.IsElliptic] (n : Nat),
      HasCyclicTorsionOrder E n → IsMazurCyclicOrder n
  restrictBicyclic :
    ∀ (E : WeierstrassCurve Rat) [E.IsElliptic] (m : Nat),
      HasBicyclicTorsionIndex E m → IsMazurBicyclicIndex m

/-- Binder-preserving assembly of the three open mathematical engines into the
exact canonical target. -/
theorem engine_compose (engine : MazurEngine) : MazurRationalTorsionTarget := by
  intro E hE
  rcases engine.torsionStructure E with ⟨n, hn⟩ | ⟨m, hm⟩
  · exact Or.inl ⟨n, engine.restrictCyclic E n hn, hn⟩
  · exact Or.inr ⟨m, engine.restrictBicyclic E m hm, hm⟩

/-- The local structural interface expands to exactly the two group families. -/
theorem torsionStructureDichotomy_iff (E : WeierstrassCurve Rat) [E.IsElliptic] :
    TorsionStructureDichotomy E ↔
      (∃ n : Nat, HasCyclicTorsionOrder E n) ∨
        (∃ m : Nat, HasBicyclicTorsionIndex E m) := by
  rfl

#check engine_compose
#print axioms engine_compose

end Stage1Instances.THMM0442.ObligationTree
