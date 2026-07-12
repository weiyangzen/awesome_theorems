import Mathlib.Probability.StrongLaw

/-!
# THM-M-0984 conditional obligation composition

This module checks the frozen architecture without claiming the imported
strong-law proof. The terminal strong-law body remains an explicit premise.
-/

noncomputable section

open Filter Finset Function MeasureTheory
open scoped MeasureTheory ProbabilityTheory Topology

namespace Stage1Instances.THM_M_0984.ObligationTree

universe u v

def Root : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega],
    forall (E : Type v) [NormedAddCommGroup E] [NormedSpace Real E]
      [CompleteSpace E] [MeasurableSpace E] [BorelSpace E],
      forall (mu : Measure Omega) (X : Nat -> Omega -> E),
        Integrable (X 0) mu ->
        Pairwise ((fun Y Z => Y ⟂ᵢ[mu] Z) on X) ->
        (forall i, ProbabilityTheory.IdentDistrib (X i) (X 0) mu mu) ->
        ∀ᵐ omega ∂mu,
          Tendsto
            (fun n : Nat => (n : Real)⁻¹ • (∑ i ∈ range n, X i omega))
            atTop (nhds (integral mu (X 0)))

/-- The terminal bridge has the exact root type. Its deep proof body is a
separate proof-phase obligation, not discharged here. -/
def TerminalStrongLaw : Prop := Root.{u, v}

/-- Checked child-to-parent composition. The mathematical terminal theorem is
kept as a premise, so this certificate gives no proof-phase credit. -/
theorem root_of_terminal (terminal : TerminalStrongLaw.{u, v}) : Root.{u, v} :=
  terminal

theorem root_exact_type :
    Root.{u, v} =
      (forall (Omega : Type u) [MeasurableSpace Omega],
        forall (E : Type v) [NormedAddCommGroup E] [NormedSpace Real E]
          [CompleteSpace E] [MeasurableSpace E] [BorelSpace E],
          forall (mu : Measure Omega) (X : Nat -> Omega -> E),
            Integrable (X 0) mu ->
            Pairwise ((fun Y Z => Y ⟂ᵢ[mu] Z) on X) ->
            (forall i, ProbabilityTheory.IdentDistrib (X i) (X 0) mu mu) ->
            ∀ᵐ omega ∂mu,
              Tendsto
                (fun n : Nat => (n : Real)⁻¹ • (∑ i ∈ range n, X i omega))
                atTop (nhds (integral mu (X 0)))) :=
  rfl

#print root_of_terminal
#print axioms root_of_terminal

end Stage1Instances.THM_M_0984.ObligationTree
