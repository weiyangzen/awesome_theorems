import ObligationTree
import Mathlib.MeasureTheory.Constructions.SimpleGraph
import Mathlib.MeasureTheory.Measure.Dirac

/-!
# THM-M-1119 proof-phase bodies

This module implements elementary graph ingredients of the frozen Kesten
architecture.  It does not prove either percolation threshold inequality.
-/

namespace Stage1Instances.THM_M_1119

open MeasureTheory

/-- Coordinatewise inclusion of the open bonds in two configurations. -/
def ConfigurationLE (configuration configuration' : Configuration) : Prop :=
  ∀ edge, configuration edge = true → configuration' edge = true

/-- An open bond is an edge of the open subgraph selected by the configuration. -/
theorem openGraph_adj_of_open
    (configuration : Configuration) {v w : Vertex}
    (edge : SquareLattice.Adj v w)
    (isOpen : configuration ⟨s(v, w), edge⟩ = true) :
    (openGraph configuration).Adj v w := by
  rw [openGraph, SimpleGraph.fromEdgeSet_adj]
  exact ⟨⟨edge, isOpen⟩, edge.ne⟩

/-- Opening additional bonds can only enlarge the selected open graph. -/
theorem openGraph_mono {configuration configuration' : Configuration}
    (h : ConfigurationLE configuration configuration') :
    openGraph configuration ≤ openGraph configuration' := by
  intro v w adjacent
  rw [openGraph, SimpleGraph.fromEdgeSet_adj] at adjacent ⊢
  exact ⟨⟨adjacent.1.1, h ⟨s(v, w), adjacent.1.1⟩ adjacent.1.2⟩, adjacent.2⟩

/-- The rooted unbounded-reachability event is increasing in the open bonds. -/
theorem originInInfiniteCluster_mono {configuration configuration' : Configuration}
    (h : ConfigurationLE configuration configuration')
    (infinite : OriginInInfiniteCluster configuration) :
    OriginInInfiniteCluster configuration' := by
  intro finiteVertices
  obtain ⟨vertex, outside, reachable⟩ := infinite finiteVertices
  exact ⟨vertex, outside, reachable.mono (openGraph_mono h)⟩

/-- Every finite open walk gives reachability in the selected open graph. -/
theorem openGraph_reachable_of_walk
    (configuration : Configuration) {v w : Vertex}
    (walk : SquareLattice.Walk v w)
    (walkOpen : ∀ (edge : Sym2 Vertex) (edgeInWalk : edge ∈ walk.edges),
      configuration ⟨edge, walk.edges_subset_edgeSet edgeInWalk⟩ = true) :
    (openGraph configuration).Reachable v w := by
  exact ⟨walk.transfer (openGraph configuration) fun edge edgeInWalk => by
    induction edge using Sym2.ind with
    | _ x y =>
        rw [SimpleGraph.mem_edgeSet]
        exact openGraph_adj_of_open configuration
          (walk.edges_subset_edgeSet edgeInWalk)
          (walkOpen s(x, y) edgeInWalk)⟩

/-- The state of one fixed bond is measurable in the product space. -/
theorem measurable_bond_state (edge : Sym2 Vertex)
    (edgeInLattice : edge ∈ SquareLattice.edgeSet) :
    Measurable fun configuration : Configuration =>
      configuration (⟨edge, edgeInLattice⟩ : Bond) = true := by
  exact (show Measurable (fun configuration : Configuration =>
    configuration (⟨edge, edgeInLattice⟩ : Bond)) from
      measurable_pi_apply (⟨edge, edgeInLattice⟩ : Bond)).eq_const true

/-- Adjacency of two fixed vertices in the selected open graph is measurable. -/
theorem measurable_openGraph_adj (v w : Vertex) :
    Measurable fun configuration : Configuration =>
      (openGraph configuration).Adj v w := by
  simp only [openGraph, SimpleGraph.fromEdgeSet_adj]
  by_cases edgeInLattice : s(v, w) ∈ SquareLattice.edgeSet
  · simpa [edgeInLattice] using
      (measurable_bond_state s(v, w) edgeInLattice).and
        (measurable_const : Measurable fun _ : Configuration => v ≠ w)
  · simp [edgeInLattice]

private theorem measurable_walk_chain (vertices : List Vertex) :
    Measurable fun configuration : Configuration =>
      List.IsChain (openGraph configuration).Adj vertices := by
  rw [show (fun configuration : Configuration =>
      List.IsChain (openGraph configuration).Adj vertices) =
      (fun configuration => ∀ (i : Nat) (hi : i + 1 < vertices.length),
        (openGraph configuration).Adj vertices[i] vertices[i + 1]) by
    funext configuration
    exact propext List.isChain_iff_getElem]
  exact Measurable.forall fun i => Measurable.forall fun _hi =>
    measurable_openGraph_adj vertices[i] vertices[i + 1]

private theorem reachable_iff_list_witness
    (configuration : Configuration) (u v : Vertex) :
    (openGraph configuration).Reachable u v ↔
      ∃ vertices,
        List.IsChain (openGraph configuration).Adj (u :: vertices) ∧
          (u :: vertices).getLast (List.cons_ne_nil u vertices) = v := by
  rw [SimpleGraph.reachable_iff_reflTransGen]
  constructor
  · exact List.exists_isChain_cons_of_relationReflTransGen
  · rintro ⟨vertices, chain, last⟩
    exact List.relationReflTransGen_of_exists_isChain_cons vertices chain last

/-- Reachability of two fixed vertices is a measurable configuration event. -/
theorem measurable_openGraph_reachable (u v : Vertex) :
    Measurable fun configuration : Configuration =>
      (openGraph configuration).Reachable u v := by
  rw [show (fun configuration : Configuration =>
      (openGraph configuration).Reachable u v) =
      (fun configuration => ∃ vertices,
        List.IsChain (openGraph configuration).Adj (u :: vertices) ∧
          (u :: vertices).getLast (List.cons_ne_nil u vertices) = v) by
    funext configuration
    exact propext (reachable_iff_list_witness configuration u v)]
  exact Measurable.exists fun vertices =>
    (measurable_walk_chain (u :: vertices)).and measurable_const

/-- The frozen rooted infinite-cluster event is measurable. -/
theorem measurable_originInInfiniteCluster :
    Measurable fun configuration : Configuration =>
      OriginInInfiniteCluster configuration := by
  unfold OriginInInfiniteCluster
  exact Measurable.forall fun finiteVertices => Measurable.exists fun vertex =>
    (measurable_const : Measurable fun _ : Configuration =>
      vertex ∉ finiteVertices).and (measurable_openGraph_reachable (0, 0) vertex)

/-- Set form of measurability for direct use with `Measure.dirac`. -/
theorem measurableSet_originInInfiniteCluster :
    MeasurableSet {configuration : Configuration |
      OriginInInfiniteCluster configuration} :=
  measurable_originInInfiniteCluster.setOf

/-- At parameter one, every Bernoulli bond is open. -/
theorem bernoulli_one_eq_pure_true :
    PMF.bernoulli (1 : NNReal) (by norm_num) = PMF.pure true := by
  ext state
  cases state <;> simp [PMF.pure_apply]

/-- The parameter-one product measure is concentrated on the all-open configuration. -/
theorem bondMeasure_one_eq_dirac :
    bondMeasure (1 : NNReal) (by norm_num) = Measure.dirac (fun _ => true) := by
  rw [bondMeasure]
  have coordinates :
      (fun _ : Bond => (PMF.bernoulli (1 : NNReal) (by norm_num)).toMeasure) =
        (fun _ : Bond => Measure.dirac true) := by
    funext _
    rw [bernoulli_one_eq_pure_true]
    exact PMF.toMeasure_pure true
  rw [coordinates, Measure.infinitePi_dirac]

/-- The all-open configuration selects the entire square lattice. -/
theorem allOpen_openGraph_eq_square :
    openGraph (fun _ => true) = SquareLattice := by
  rw [openGraph]
  rw [show {edge | ∃ h : edge ∈ SquareLattice.edgeSet,
      (fun _ : Bond => true) ⟨edge, h⟩ = true} = SquareLattice.edgeSet by
    ext edge
    simp]
  exact SimpleGraph.fromEdgeSet_edgeSet SquareLattice

private theorem squareLattice_reachable_right (n : Nat) :
    SquareLattice.Reachable (0, 0) (Int.ofNat n, 0) := by
  induction n with
  | zero => rfl
  | succ n ih =>
      exact ih.trans (SimpleGraph.Adj.reachable (by
        right
        exact ⟨rfl, by simp⟩))

/-- The origin has an unbounded open cluster in the all-open configuration. -/
theorem originInInfiniteCluster_allOpen :
    OriginInInfiniteCluster (fun _ => true) := by
  intro finiteVertices
  let n : Nat := finiteVertices.sup (fun vertex => vertex.1.natAbs)
  let vertex : Vertex := (Int.ofNat (n + 1), 0)
  have outside : vertex ∉ finiteVertices := by
    intro inside
    have impossible : n + 1 ≤ n :=
      Finset.le_sup (f := fun vertex : Vertex => vertex.1.natAbs) inside
    omega
  refine ⟨vertex, outside, ?_⟩
  rw [allOpen_openGraph_eq_square]
  exact squareLattice_reachable_right (n + 1)

/-- Parameter one belongs to the positive-percolation set defining the critical infimum. -/
theorem one_mem_positiveParameters :
    (1 : NNReal) ∈ {p : NNReal | ∃ hp : p ≤ 1,
      0 < percolationProbability p hp} := by
  refine ⟨by norm_num, ?_⟩
  rw [percolationProbability, bondMeasure_one_eq_dirac]
  rw [Measure.dirac_apply' _ measurableSet_originInInfiniteCluster]
  simp [originInInfiniteCluster_allOpen]

/-- A checked endpoint sanity bound for the frozen critical infimum. -/
theorem criticalProbability_le_one : criticalProbability ≤ 1 := by
  unfold criticalProbability
  exact csInf_le (OrderBot.bddBelow _) one_mem_positiveParameters

/-- At parameter zero, every Bernoulli bond is closed. -/
theorem bernoulli_zero_eq_pure_false :
    PMF.bernoulli (0 : NNReal) (by norm_num) = PMF.pure false := by
  ext state
  cases state <;> simp [PMF.pure_apply]

/-- The parameter-zero product measure is concentrated on the all-closed configuration. -/
theorem bondMeasure_zero_eq_dirac :
    bondMeasure (0 : NNReal) (by norm_num) = Measure.dirac (fun _ => false) := by
  rw [bondMeasure]
  have coordinates :
      (fun _ : Bond => (PMF.bernoulli (0 : NNReal) (by norm_num)).toMeasure) =
        (fun _ : Bond => Measure.dirac false) := by
    funext _
    rw [bernoulli_zero_eq_pure_false]
    exact PMF.toMeasure_pure false
  rw [coordinates, Measure.infinitePi_dirac]

/-- The all-closed configuration selects the empty graph. -/
theorem allClosed_openGraph_eq_bot :
    openGraph (fun _ => false) = (⊥ : SimpleGraph Vertex) := by
  rw [openGraph]
  rw [show {edge | ∃ h : edge ∈ SquareLattice.edgeSet,
      (fun _ : Bond => false) ⟨edge, h⟩ = true} = ∅ by
    ext edge
    simp]
  simp

/-- The origin does not have an unbounded cluster in the all-closed configuration. -/
theorem not_originInInfiniteCluster_allClosed :
    ¬OriginInInfiniteCluster (fun _ => false) := by
  intro infinite
  obtain ⟨vertex, outside, reachable⟩ := infinite {(0, 0)}
  rw [allClosed_openGraph_eq_bot, SimpleGraph.reachable_bot] at reachable
  subst vertex
  simp at outside

/-- Percolation probability is zero at the closed endpoint. -/
theorem percolationProbability_zero :
    percolationProbability (0 : NNReal) (by norm_num) = 0 := by
  rw [percolationProbability, bondMeasure_zero_eq_dirac]
  rw [Measure.dirac_apply' _ measurableSet_originInInfiniteCluster]
  simp [not_originInInfiniteCluster_allClosed]

/-- Parameter zero is absent from the positive-percolation set. -/
theorem zero_not_mem_positiveParameters :
    (0 : NNReal) ∉ {p : NNReal | ∃ hp : p ≤ 1,
      0 < percolationProbability p hp} := by
  rintro ⟨hp, positive⟩
  rw [show hp = (by norm_num : (0 : NNReal) ≤ 1) by rfl,
    percolationProbability_zero] at positive
  exact (lt_irrefl 0 positive)

#print axioms Stage1Instances.THM_M_1119.openGraph_adj_of_open
#print axioms Stage1Instances.THM_M_1119.openGraph_mono
#print axioms Stage1Instances.THM_M_1119.originInInfiniteCluster_mono
#print axioms Stage1Instances.THM_M_1119.openGraph_reachable_of_walk
#print axioms Stage1Instances.THM_M_1119.measurable_openGraph_reachable
#print axioms Stage1Instances.THM_M_1119.measurable_originInInfiniteCluster
#print axioms Stage1Instances.THM_M_1119.bondMeasure_one_eq_dirac
#print axioms Stage1Instances.THM_M_1119.originInInfiniteCluster_allOpen
#print axioms Stage1Instances.THM_M_1119.one_mem_positiveParameters
#print axioms Stage1Instances.THM_M_1119.criticalProbability_le_one
#print axioms Stage1Instances.THM_M_1119.bondMeasure_zero_eq_dirac
#print axioms Stage1Instances.THM_M_1119.percolationProbability_zero
#print axioms Stage1Instances.THM_M_1119.zero_not_mem_positiveParameters

end Stage1Instances.THM_M_1119
