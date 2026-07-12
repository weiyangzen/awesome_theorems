import Mathlib.Combinatorics.SimpleGraph.Connectivity.Connected
import Mathlib.Probability.ProductMeasure
import Mathlib.Probability.ProbabilityMassFunction.Constructions

/-!
# THM-M-1119: Kesten's square-lattice bond-percolation statement

This module freezes the statement boundary only. It contains no proof that the
critical probability is one half.
-/

noncomputable section

open MeasureTheory Set
open scoped ENNReal

namespace Stage1Instances.THM_M_1119

/-- Vertices of the planar square lattice. -/
abbrev Vertex := Int × Int

/-- Nearest-neighbor adjacency on `Z x Z`, written without an embedding choice. -/
def SquareLattice : SimpleGraph Vertex where
  Adj v w :=
    (v.1 = w.1 ∧ (v.2 - w.2).natAbs = 1) ∨
    (v.2 = w.2 ∧ (v.1 - w.1).natAbs = 1)
  symm := by
    intro v w h
    rcases h with h | h
    · left
      refine ⟨h.1.symm, ?_⟩
      rw [show w.2 - v.2 = -(v.2 - w.2) by omega, Int.natAbs_neg]
      exact h.2
    · right
      refine ⟨h.1.symm, ?_⟩
      rw [show w.1 - v.1 = -(v.1 - w.1) by omega, Int.natAbs_neg]
      exact h.2
  loopless := ⟨by simp⟩

/-- Unoriented nearest-neighbor bonds of the square lattice. -/
abbrev Bond := SquareLattice.edgeSet

/-- A bond configuration records which bonds are open. -/
abbrev Configuration := Bond → Bool

/-- Independent Bernoulli bond measure with opening parameter `p`. -/
def bondMeasure (p : NNReal) (hp : p ≤ 1) : Measure Configuration :=
  Measure.infinitePi (fun _ : Bond ↦ (PMF.bernoulli p hp).toMeasure)

/-- The open subgraph selected by a configuration. -/
def openGraph (configuration : Configuration) : SimpleGraph Vertex :=
  SimpleGraph.fromEdgeSet {edge | ∃ h : edge ∈ SquareLattice.edgeSet, configuration ⟨edge, h⟩ = true}

/-- The origin belongs to an infinite open cluster. The quantification over
finite vertex sets is the graph-theoretic unboundedness formulation used here. -/
def OriginInInfiniteCluster (configuration : Configuration) : Prop :=
  ∀ finiteVertices : Finset Vertex,
    ∃ vertex : Vertex, vertex ∉ finiteVertices ∧
      (openGraph configuration).Reachable (0, 0) vertex

/-- Percolation probability from the origin. -/
def percolationProbability (p : NNReal) (hp : p ≤ 1) : ENNReal :=
  bondMeasure p hp {configuration | OriginInInfiniteCluster configuration}

/-- The critical probability is the infimum of parameters in `[0,1]` at which
the origin has positive probability of lying in an infinite open cluster. -/
def criticalProbability : NNReal :=
  sInf {p : NNReal | ∃ hp : p ≤ 1, 0 < percolationProbability p hp}

/-- Kesten's critical-probability theorem for independent bond percolation on
the square lattice. -/
def KestenTarget : Prop :=
  criticalProbability = (1 / 2 : NNReal)

/-- Expanded spelling used as a checked transport for the selected target. -/
def ExpandedTarget : Prop :=
  sInf {p : NNReal | ∃ hp : p ≤ 1,
    0 < bondMeasure p hp {configuration |
      ∀ finiteVertices : Finset Vertex,
        ∃ vertex : Vertex, vertex ∉ finiteVertices ∧
          (openGraph configuration).Reachable (0, 0) vertex}} = (1 / 2 : NNReal)

theorem kestenTarget_iff_expandedTarget : KestenTarget ↔ ExpandedTarget := by
  rfl

-- Separately elaborated, deliberately non-equivalent statement mutations.
def mutationSiteDomain : Prop :=
  sInf {p : NNReal | ∃ hp : p ≤ 1,
    0 < Measure.infinitePi (fun _ : Vertex ↦ (PMF.bernoulli p hp).toMeasure)
      {configuration | configuration (0, 0) = true}} = (1 / 2 : NNReal)

def mutationRemovedInfiniteClusterEvent : Prop :=
  sInf {p : NNReal | ∃ _hp : p ≤ 1, 0 < p} = (1 / 2 : NNReal)

def mutationChangedBinderScope : Prop :=
  ∃ hp : (1 / 2 : NNReal) ≤ 1,
    criticalProbability = (1 / 2 : NNReal) ∧
      0 < percolationProbability (1 / 2 : NNReal) hp

def mutationIncludesCriticalEndpoint : Prop :=
  criticalProbability = (1 / 2 : NNReal) ∧
    ∀ hp : (1 / 2 : NNReal) ≤ 1,
      percolationProbability (1 / 2 : NNReal) hp = 0

end Stage1Instances.THM_M_1119

set_option pp.explicit true in
#print Stage1Instances.THM_M_1119.KestenTarget
