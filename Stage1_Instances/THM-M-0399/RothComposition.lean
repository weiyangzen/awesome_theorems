import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.RingTheory.Algebraic.Defs
import Mathlib.Topology.Instances.Irrational

/-!
# THM-M-0399: checked root composition

This file proves only the specialization from the stronger constant-`C` interface to the frozen
constant-one root. The `StrongFiniteStatement` premise is deliberately explicit: this composition
term is not a proof of Roth's theorem by itself.
-/

noncomputable section

namespace Stage1Instances.THM_M_0399

/-- The frozen canonical exceptional set, repeated here because the owned dossier is outside the
Lake source tree and therefore is not importable as a module during narrow file elaboration. -/
def exceptionalRationals (alpha epsilon : ℝ) : Set ℚ :=
  {x | |alpha - (x : ℝ)| < Real.rpow (x.den : ℝ) (-(2 + epsilon))}

/-- The frozen canonical proposition from `RothStatement.lean`. -/
def RothStatement : Prop :=
  ∀ (alpha : ℝ), IsAlgebraic ℚ alpha → Irrational alpha →
    ∀ (epsilon : ℝ), 0 < epsilon → (exceptionalRationals alpha epsilon).Finite

/-- The constant-`C` exceptional set used by the frozen proof architecture. -/
def strongExceptionalRationals (alpha epsilon C : ℝ) : Set ℚ :=
  {x | |alpha - (x : ℝ)| < C * Real.rpow (x.den : ℝ) (-(2 + epsilon))}

/-- The stronger finite-approximants interface from which the canonical root follows at `C = 1`. -/
def StrongFiniteStatement : Prop :=
  ∀ (alpha : ℝ), IsAlgebraic ℚ alpha → Irrational alpha →
    ∀ (epsilon : ℝ), 0 < epsilon →
      ∀ (C : ℝ), 0 < C → (strongExceptionalRationals alpha epsilon C).Finite

/-- Exact child-to-parent composition certificate for `M0399-ROOT-COMPOSE`. -/
theorem rothStatement_of_strongFinite (h : StrongFiniteStatement) : RothStatement := by
  intro alpha halg hirr epsilon hepsilon
  simpa [exceptionalRationals, strongExceptionalRationals] using
    h alpha halg hirr epsilon hepsilon 1 zero_lt_one

end Stage1Instances.THM_M_0399

#check Stage1Instances.THM_M_0399.rothStatement_of_strongFinite
