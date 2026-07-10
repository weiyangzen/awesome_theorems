import Mathlib.Analysis.Calculus.ContDiff.Basic
import Mathlib.Analysis.Calculus.FDeriv.Basic
import Mathlib.Topology.Connected.PathConnected
import Mathlib.Topology.Order.Compact
import Mathlib.Topology.Order.LocalExtr
import Mathlib.Topology.Sequences

/-!
# S1-M-164 / THM-M-1271: Mountain pass lemma

This Stage1 artifact records a conservative Lean 4 statement boundary for the
mountain pass lemma in variational analysis.

The pinned mathlib snapshot has the basic object model needed to state the
boundary: Frechet derivatives, `ContDiff`, continuous paths, local extrema, and
compact subsequence extraction.  This audit did not find a terminal
Palais-Smale or mountain-pass theorem in local mathlib.  The declarations below
therefore normalize the theorem shape and add only checked wrappers around
available mathlib facts.
-/

noncomputable section

open Filter
open scoped Topology unitInterval

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_164

universe u

/-- Critical point for a real-valued functional on a real normed space. -/
def CriticalPoint {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    (Φ : E → ℝ) (x : E) : Prop :=
  fderiv ℝ Φ x = 0

/--
A Palais-Smale sequence at level `c` for a real Frechet-differentiable
functional.

This uses the Banach-space dual norm formulation: `fderiv ℝ Φ (u n)` is the
continuous linear functional `E →L[ℝ] ℝ`, and its operator norm tends to zero.
-/
structure PalaisSmaleSequence {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    (Φ : E → ℝ) (c : ℝ) (u : ℕ → E) : Prop where
  values_tendsto : Tendsto (fun n : ℕ => Φ (u n)) atTop (𝓝 c)
  derivative_norm_tendsto :
    Tendsto (fun n : ℕ => ‖fderiv ℝ Φ (u n)‖) atTop (𝓝 (0 : ℝ))

/--
Palais-Smale compactness at a fixed level for the selected Banach-space
formulation.

Every sequence whose functional values converge to `c` and whose Frechet
derivative norms converge to zero has a convergent subsequence.  The
`CompleteSpace E` instance records the classical Banach-space ambient
assumption for this Stage1 mountain-pass statement; Hilbert-space gradient
versions should be bridged later by identifying the dual derivative norm with
the chosen gradient norm.
-/
def PalaisSmaleAt {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E] [CompleteSpace E]
    (Φ : E → ℝ) (c : ℝ) : Prop :=
  ∀ u : ℕ → E,
    PalaisSmaleSequence Φ c u →
      ∃ x : E, ∃ φ : ℕ → ℕ, StrictMono φ ∧ Tendsto (u ∘ φ) atTop (𝓝 x)

/--
Mountain-pass geometry for a functional.

The fields encode the usual data: `Φ 0 = 0`, a positive barrier on the sphere of
radius `radius`, and an endpoint outside that sphere with nonpositive energy.
-/
structure MountainPassGeometry (E : Type u) [NormedAddCommGroup E] [NormedSpace ℝ E] :
    Type u where
  energy : E → ℝ
  endpoint : E
  radius : ℝ
  barrier : ℝ
  energy_contDiff : ContDiff ℝ 1 energy
  origin_value : energy 0 = 0
  radius_pos : 0 < radius
  barrier_pos : 0 < barrier
  endpoint_outside : radius < ‖endpoint‖
  endpoint_value_nonpos : energy endpoint ≤ 0
  barrier_on_sphere : ∀ x : E, ‖x‖ = radius → barrier ≤ energy x

/-- Continuous paths from the origin to the selected endpoint. -/
abbrev AdmissiblePath {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    (D : MountainPassGeometry E) : Type u :=
  Path (0 : E) D.endpoint

/-- Energy of an admissible path as a continuous function on the unit interval. -/
def pathEnergy {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    (D : MountainPassGeometry E) (γ : AdmissiblePath D) : I → ℝ :=
  fun t => D.energy (γ t)

/--
The path-energy map is continuous.  This is the continuity hypothesis needed to
turn the compact unit interval into a maximum-over-path API.
-/
theorem pathEnergy_continuous {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    (D : MountainPassGeometry E) (γ : AdmissiblePath D) :
    Continuous (pathEnergy D γ) :=
  D.energy_contDiff.continuous.comp γ.continuous

/--
The energy along an admissible path attains a maximum on the compact unit
interval.
-/
theorem pathEnergy_exists_isMax {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    (D : MountainPassGeometry E) (γ : AdmissiblePath D) :
    ∃ t₀ : I, ∀ t : I, pathEnergy D γ t ≤ pathEnergy D γ t₀ := by
  obtain ⟨t₀, _ht₀, ht₀⟩ :=
    (isCompact_univ : IsCompact (Set.univ : Set I)).exists_isMaxOn
      Set.univ_nonempty (pathEnergy_continuous D γ).continuousOn
  exact ⟨t₀, fun t => (isMaxOn_iff.mp ht₀) t (Set.mem_univ t)⟩

/--
A maximizing parameter for the energy of an admissible path.

This is noncomputable because it selects a witness from the compactness
argument above.
-/
noncomputable def pathHeightPoint {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    (D : MountainPassGeometry E) (γ : AdmissiblePath D) : I :=
  Classical.choose (pathEnergy_exists_isMax D γ)

/--
The path-height functional: the maximum energy achieved along an admissible
path.
-/
noncomputable def pathHeight {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    (D : MountainPassGeometry E) (γ : AdmissiblePath D) : ℝ :=
  pathEnergy D γ (pathHeightPoint D γ)

/-- The selected path-height point realizes a maximum over the unit interval. -/
theorem pathEnergy_le_pathHeight {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    (D : MountainPassGeometry E) (γ : AdmissiblePath D) (t : I) :
    pathEnergy D γ t ≤ pathHeight D γ := by
  simpa [pathHeight, pathHeightPoint] using
    (Classical.choose_spec (pathEnergy_exists_isMax D γ) t)

/-- The path height is exactly the energy at its selected maximizing parameter. -/
theorem pathHeight_eq_energy_at_point
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    (D : MountainPassGeometry E) (γ : AdmissiblePath D) :
    pathHeight D γ = D.energy (γ (pathHeightPoint D γ)) :=
  rfl

/-- The origin endpoint energy is bounded above by the path height. -/
theorem origin_energy_le_pathHeight
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    (D : MountainPassGeometry E) (γ : AdmissiblePath D) :
    D.energy 0 ≤ pathHeight D γ := by
  simpa [pathEnergy, Path.source γ] using pathEnergy_le_pathHeight D γ 0

/-- The selected endpoint energy is bounded above by the path height. -/
theorem endpoint_energy_le_pathHeight
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    (D : MountainPassGeometry E) (γ : AdmissiblePath D) :
    D.energy D.endpoint ≤ pathHeight D γ := by
  simpa [pathEnergy, Path.target γ] using pathEnergy_le_pathHeight D γ 1

/--
Minimax characterization of the mountain-pass level without introducing a
maximum-over-path API.

The first field says every admissible path crosses energy at least `c`.  The
second says paths can be found whose pointwise energy is bounded by `c + ε`,
which is the infimum-over-paths side of the usual minimax formula.
-/
structure MountainPassLevel {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    (D : MountainPassGeometry E) (c : ℝ) : Prop where
  lower_bound_on_paths :
    ∀ γ : AdmissiblePath D, ∃ t : I, c ≤ D.energy (γ t)
  almost_minimizing_paths :
    ∀ ε : ℝ, 0 < ε → ∃ γ : AdmissiblePath D, ∀ t : I, D.energy (γ t) ≤ c + ε

/--
Concrete minimax formula for the mountain-pass level:
`c` is the infimum over admissible paths of the maximum path energy.

The maximum over the compact unit interval is represented by `pathHeight`.
-/
def MountainPassMinimaxFormula {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    (D : MountainPassGeometry E) (c : ℝ) : Prop :=
  IsGLB (Set.range (pathHeight D)) c

/-- Predicate-level lower bounds imply lower bounds for the path-height functional. -/
theorem MountainPassLevel.le_pathHeight
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {D : MountainPassGeometry E} {c : ℝ} (h : MountainPassLevel D c)
    (γ : AdmissiblePath D) :
    c ≤ pathHeight D γ := by
  obtain ⟨t, ht⟩ := h.lower_bound_on_paths γ
  exact le_trans ht (by simpa [pathEnergy] using pathEnergy_le_pathHeight D γ t)

/-- Predicate-level almost-minimizers imply almost-minimizers of `pathHeight`. -/
theorem MountainPassLevel.exists_pathHeight_le_add
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {D : MountainPassGeometry E} {c ε : ℝ} (h : MountainPassLevel D c)
    (hε : 0 < ε) :
    ∃ γ : AdmissiblePath D, pathHeight D γ ≤ c + ε := by
  obtain ⟨γ, hγ⟩ := h.almost_minimizing_paths ε hε
  exact ⟨γ, by
    simpa [pathHeight, pathEnergy] using hγ (pathHeightPoint D γ)⟩

/--
The predicate-level mountain-pass level determines the concrete minimax
formula `c = inf_γ max_t Φ (γ t)`.
-/
theorem MountainPassLevel.to_minimaxFormula
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {D : MountainPassGeometry E} {c : ℝ} (h : MountainPassLevel D c) :
    MountainPassMinimaxFormula D c := by
  refine ⟨?_, ?_⟩
  · intro y hy
    rcases hy with ⟨γ, rfl⟩
    exact h.le_pathHeight γ
  · intro b hb
    apply le_of_forall_pos_le_add
    intro ε hε
    obtain ⟨γ, hγ⟩ := h.exists_pathHeight_le_add hε
    exact le_trans (hb ⟨γ, rfl⟩) hγ

/--
The concrete minimax formula supplies the predicate-level mountain-pass level
used by the Stage1 statement shape.
-/
theorem MountainPassMinimaxFormula.to_level
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {D : MountainPassGeometry E} {c : ℝ} (h : MountainPassMinimaxFormula D c) :
    MountainPassLevel D c := by
  refine ⟨?_, ?_⟩
  · intro γ
    refine ⟨pathHeightPoint D γ, ?_⟩
    exact by
      have hc : c ≤ pathHeight D γ := h.1 ⟨γ, rfl⟩
      simpa [pathHeight, pathEnergy] using hc
  · intro ε hε
    by_contra hnone
    have hLower : c + ε ∈ lowerBounds (Set.range (pathHeight D)) := by
      intro y hy
      rcases hy with ⟨γ, rfl⟩
      by_contra hnot
      have hlt : pathHeight D γ < c + ε := not_le.mp hnot
      exact hnone ⟨γ, fun t =>
        le_trans (by simpa [pathEnergy] using pathEnergy_le_pathHeight D γ t)
          (le_of_lt hlt)⟩
    have hle : c + ε ≤ c := h.2 hLower
    exact (not_lt_of_ge hle) (lt_add_of_pos_right c hε)

/--
Equivalence between the Stage1 predicate-level package and the concrete
minimax formula.
-/
theorem mountainPassLevel_iff_minimaxFormula
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {D : MountainPassGeometry E} {c : ℝ} :
    MountainPassLevel D c ↔ MountainPassMinimaxFormula D c :=
  ⟨MountainPassLevel.to_minimaxFormula, MountainPassMinimaxFormula.to_level⟩

/--
Path-level consequence of a deformation lemma near the minimax level.

The classical deformation lemma is usually supplied by a pseudo-gradient flow
on the ambient Banach or Hilbert space.  This Stage1 boundary records only the
consequence needed for the mountain-pass contradiction: every path with height
at most `c + ε` can be deformed inside the admissible class to height at most
`c - ε`.
-/
structure PathLoweringDeformation
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    (D : MountainPassGeometry E) (c ε : ℝ) : Type u where
  mapPath : AdmissiblePath D → AdmissiblePath D
  lowers_almost_minimizer :
    ∀ γ : AdmissiblePath D, pathHeight D γ ≤ c + ε →
      pathHeight D (mapPath γ) ≤ c - ε

/--
At a genuine mountain-pass level, a path-lowering deformation of the above form
cannot exist for any positive `ε`.

This is the checked minimax contradiction that the later analytic deformation
lemma must feed: combine an almost-minimizing path with the deformation, then
use the lower bound for every admissible path.
-/
theorem MountainPassLevel.not_pathLoweringDeformation
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {D : MountainPassGeometry E} {c ε : ℝ} (h : MountainPassLevel D c)
    (hε : 0 < ε) :
    ¬ Nonempty (PathLoweringDeformation D c ε) := by
  intro hdeform
  rcases hdeform with ⟨η⟩
  obtain ⟨γ, hγ⟩ := h.exists_pathHeight_le_add hε
  have hLower : c ≤ pathHeight D (η.mapPath γ) :=
    h.le_pathHeight (η.mapPath γ)
  have hUpper : pathHeight D (η.mapPath γ) ≤ c - ε :=
    η.lowers_almost_minimizer γ hγ
  have hc : c ≤ c - ε := le_trans hLower hUpper
  exact (not_lt_of_ge hc) (sub_lt_self c hε)

/--
Formalization boundary for the deformation lemma branch.

A terminal proof should replace this proposition-valued interface by either a
repo-local pseudo-gradient deformation proof or a pinned upstream theorem.  Its
required output is a Palais-Smale sequence at the minimax level.
-/
structure MinimaxDeformationLemma
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    (D : MountainPassGeometry E) (c : ℝ) : Prop where
  exists_palaisSmaleSequence :
    MountainPassLevel D c → ∃ u : ℕ → E, PalaisSmaleSequence D.energy c u

/-- Apply the deformation-lemma interface to construct a Palais-Smale sequence. -/
theorem MinimaxDeformationLemma.exists_ps_sequence
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {D : MountainPassGeometry E} {c : ℝ}
    (hdef : MinimaxDeformationLemma D c) (hlevel : MountainPassLevel D c) :
    ∃ u : ℕ → E, PalaisSmaleSequence D.energy c u :=
  hdef.exists_palaisSmaleSequence hlevel

/-- Output package expected from the mountain pass lemma. -/
structure MountainPassCriticalPoint {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    (D : MountainPassGeometry E) (c : ℝ) : Type u where
  point : E
  critical : CriticalPoint D.energy point
  energy_eq_level : D.energy point = c

/--
Normalized Stage1 statement shape for the mountain pass lemma.

For every real Banach space and functional with mountain-pass geometry, if `c`
is the minimax level and the Palais-Smale compactness condition holds at `c`,
then there is a critical point at level `c`.
-/
def StatementShape : Prop :=
  ∀ (E : Type u) [NormedAddCommGroup E] [NormedSpace ℝ E] [CompleteSpace E]
    (D : MountainPassGeometry E) (c : ℝ),
      MountainPassLevel D c →
        PalaisSmaleAt D.energy c →
          Nonempty (MountainPassCriticalPoint D c)

/-- Low-risk introduction wrapper for the normalized statement shape. -/
theorem StatementShape.intro
    (h : ∀ (E : Type u) [NormedAddCommGroup E] [NormedSpace ℝ E] [CompleteSpace E]
      (D : MountainPassGeometry E) (c : ℝ),
        MountainPassLevel D c →
          PalaisSmaleAt D.energy c →
            Nonempty (MountainPassCriticalPoint D c)) :
    StatementShape.{u} :=
  h

/-- Apply the Banach-space Palais-Smale compactness predicate to a sequence. -/
theorem PalaisSmaleAt.subseq
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E] [CompleteSpace E]
    {Φ : E → ℝ} {c : ℝ} {u : ℕ → E}
    (hPS : PalaisSmaleAt Φ c) (hu : PalaisSmaleSequence Φ c u) :
    ∃ x : E, ∃ φ : ℕ → ℕ, StrictMono φ ∧ Tendsto (u ∘ φ) atTop (𝓝 x) :=
  hPS u hu

/--
Limit passage for the energy level along a convergent Palais-Smale subsequence.

This is the value-convergence half of the terminal Palais-Smale passage:
if `Φ (u n) → c`, a strictly increasing subsequence `u (φ n)` converges to `x`,
and `Φ` is continuous at `x`, then the limit point has energy `c`.
-/
theorem PalaisSmaleSequence.energy_eq_of_subseq_tendsto
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {Φ : E → ℝ} {c : ℝ} {u : ℕ → E} {x : E} {φ : ℕ → ℕ}
    (hu : PalaisSmaleSequence Φ c u) (hφ : StrictMono φ)
    (hx : Tendsto (u ∘ φ) atTop (𝓝 x)) (hΦ : ContinuousAt Φ x) :
    Φ x = c := by
  have hvaluesSubseq : Tendsto (fun n : ℕ => Φ (u (φ n))) atTop (𝓝 c) := by
    simpa [Function.comp_def] using hu.values_tendsto.comp hφ.tendsto_atTop
  have hvaluesLimit : Tendsto (fun n : ℕ => Φ (u (φ n))) atTop (𝓝 (Φ x)) := by
    simpa [Function.comp_def] using hΦ.tendsto.comp hx
  exact tendsto_nhds_unique hvaluesLimit hvaluesSubseq

/--
Limit passage for criticality along a convergent Palais-Smale subsequence.

This isolates the analytic continuity obligation needed for the Frechet
derivative branch: if the derivative map is continuous at the subsequential
limit and the derivative norms of the Palais-Smale sequence tend to zero, then
`fderiv ℝ Φ x = 0`.
-/
theorem PalaisSmaleSequence.criticalPoint_of_subseq_tendsto
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {Φ : E → ℝ} {c : ℝ} {u : ℕ → E} {x : E} {φ : ℕ → ℕ}
    (hu : PalaisSmaleSequence Φ c u) (hφ : StrictMono φ)
    (hx : Tendsto (u ∘ φ) atTop (𝓝 x))
    (hfderiv : ContinuousAt (fun y : E => fderiv ℝ Φ y) x) :
    CriticalPoint Φ x := by
  have hderivNormSubseq :
      Tendsto (fun n : ℕ => ‖fderiv ℝ Φ (u (φ n))‖) atTop (𝓝 (0 : ℝ)) := by
    simpa [Function.comp_def] using hu.derivative_norm_tendsto.comp hφ.tendsto_atTop
  have hderivLimit :
      Tendsto (fun n : ℕ => fderiv ℝ Φ (u (φ n))) atTop (𝓝 (fderiv ℝ Φ x)) := by
    simpa [Function.comp_def] using hfderiv.tendsto.comp hx
  have hderivNormLimit :
      Tendsto (fun n : ℕ => ‖fderiv ℝ Φ (u (φ n))‖) atTop
        (𝓝 ‖fderiv ℝ Φ x‖) :=
    hderivLimit.norm
  have hnorm : ‖fderiv ℝ Φ x‖ = 0 :=
    tendsto_nhds_unique hderivNormLimit hderivNormSubseq
  exact norm_eq_zero.mp hnorm

/--
Combined terminal limit passage from a Palais-Smale subsequence.

This closes the child leaf that turns a convergent Palais-Smale subsequence
into the two expected output facts, under the explicit continuity hypotheses
that a later Banach/Hilbert-space theorem must discharge.
-/
theorem PalaisSmaleSequence.limit_criticalPoint_and_energy_eq
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {Φ : E → ℝ} {c : ℝ} {u : ℕ → E} {x : E} {φ : ℕ → ℕ}
    (hu : PalaisSmaleSequence Φ c u) (hφ : StrictMono φ)
    (hx : Tendsto (u ∘ φ) atTop (𝓝 x)) (hΦ : ContinuousAt Φ x)
    (hfderiv : ContinuousAt (fun y : E => fderiv ℝ Φ y) x) :
    CriticalPoint Φ x ∧ Φ x = c :=
  ⟨hu.criticalPoint_of_subseq_tendsto hφ hx hfderiv,
    hu.energy_eq_of_subseq_tendsto hφ hx hΦ⟩

/--
Use the Palais-Smale compactness predicate and the checked limit-passage
lemmas to produce a critical point at the target energy level.
-/
theorem PalaisSmaleAt.exists_criticalPoint_and_energy_eq
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E] [CompleteSpace E]
    {Φ : E → ℝ} {c : ℝ} {u : ℕ → E}
    (hPS : PalaisSmaleAt Φ c) (hu : PalaisSmaleSequence Φ c u)
    (hΦ : ∀ x : E, ContinuousAt Φ x)
    (hfderiv : ∀ x : E, ContinuousAt (fun y : E => fderiv ℝ Φ y) x) :
    ∃ x : E, ∃ φ : ℕ → ℕ,
      StrictMono φ ∧ Tendsto (u ∘ φ) atTop (𝓝 x) ∧ CriticalPoint Φ x ∧ Φ x = c := by
  obtain ⟨x, φ, hφ, hx⟩ := hPS.subseq hu
  exact ⟨x, φ, hφ, hx, hu.criticalPoint_of_subseq_tendsto hφ hx (hfderiv x),
    hu.energy_eq_of_subseq_tendsto hφ hx (hΦ x)⟩

/--
Mountain-pass output from an already constructed Palais-Smale sequence and
the explicit derivative-continuity bridge.

This is not the full mountain pass lemma: the construction of the
Palais-Smale sequence and the proof that the derivative map is continuous in
the selected topology remain separate formalization leaves.
-/
theorem PalaisSmaleAt.exists_mountainPassCriticalPoint_of_ps_sequence
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E] [CompleteSpace E]
    {D : MountainPassGeometry E} {c : ℝ} {u : ℕ → E}
    (hPS : PalaisSmaleAt D.energy c) (hu : PalaisSmaleSequence D.energy c u)
    (hfderiv : ∀ x : E, ContinuousAt (fun y : E => fderiv ℝ D.energy y) x) :
    Nonempty (MountainPassCriticalPoint D c) := by
  obtain ⟨x, _φ, _hφ, _hx, hcrit, henergy⟩ :=
    hPS.exists_criticalPoint_and_energy_eq hu
      (fun _x => D.energy_contDiff.continuous.continuousAt) hfderiv
  exact ⟨{ point := x, critical := hcrit, energy_eq_level := henergy }⟩

/-- A path in the admissible class starts at the origin. -/
theorem admissiblePath_source {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {D : MountainPassGeometry E} (γ : AdmissiblePath D) :
    γ 0 = (0 : E) :=
  Path.source γ

/-- A path in the admissible class ends at the selected endpoint. -/
theorem admissiblePath_target {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {D : MountainPassGeometry E} (γ : AdmissiblePath D) :
    γ 1 = D.endpoint :=
  Path.target γ

/-- Expose the differentiability field of the mountain-pass input package. -/
theorem energy_contDiff {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    (D : MountainPassGeometry E) :
    ContDiff ℝ 1 D.energy :=
  D.energy_contDiff

/-- Expose the positive barrier-on-sphere hypothesis. -/
theorem barrier_on_sphere {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    (D : MountainPassGeometry E) {x : E} (hx : ‖x‖ = D.radius) :
    D.barrier ≤ D.energy x :=
  D.barrier_on_sphere x hx

/-- Extract the criticality component from the output package. -/
theorem MountainPassCriticalPoint.critical_point
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {D : MountainPassGeometry E} {c : ℝ} (H : MountainPassCriticalPoint D c) :
    CriticalPoint D.energy H.point :=
  H.critical

/-- Extract the energy-level equality from the output package. -/
theorem MountainPassCriticalPoint.energy_level
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {D : MountainPassGeometry E} {c : ℝ} (H : MountainPassCriticalPoint D c) :
    D.energy H.point = c :=
  H.energy_eq_level

/-- Checked mathlib anchor: a local minimum is a local extremum. -/
theorem isLocalMin_to_isLocalExtr
    {X : Type u} [TopologicalSpace X] {f : X → ℝ} {x : X}
    (h : IsLocalMin f x) :
    IsLocalExtr f x :=
  Or.inl h

/-- Checked mathlib anchor: compact sets in first-countable spaces have convergent subsequences. -/
theorem compact_tendsto_subseq_anchor
    {X : Type u} [TopologicalSpace X] [FirstCountableTopology X]
    {s : Set X} (hs : IsCompact s) {x : ℕ → X} (hx : ∀ n, x n ∈ s) :
    ∃ a ∈ s, ∃ φ : ℕ → ℕ, StrictMono φ ∧ Tendsto (x ∘ φ) atTop (𝓝 a) :=
  hs.tendsto_subseq hx

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Analysis.Calculus.ContDiff.Basic",
  "Mathlib.Analysis.Calculus.FDeriv.Basic",
  "Mathlib.Topology.Path",
  "Mathlib.Topology.Connected.PathConnected",
  "Mathlib.Topology.Order.Compact",
  "Mathlib.Topology.Order.LocalExtr",
  "Mathlib.Topology.Sequences",
  "Mathlib.Analysis.FunctionalSpaces.SobolevInequality",
  "Mathlib.Analysis.Distribution.Distribution"
]

/-- Checked declaration names used as Stage1 anchors. -/
def mathlibAnchorNames : List String := [
  "fderiv",
  "ContDiff",
  "Path",
  "Path.source",
  "Path.target",
  "I",
  "CompactSpace I",
  "IsCompact.exists_isMaxOn",
  "isCompact_univ",
  "Tendsto",
  "Filter.Tendsto.norm",
  "tendsto_nhds_unique",
  "ContinuousAt",
  "StrictMono",
  "StrictMono.tendsto_atTop",
  "IsLocalMin",
  "IsLocalExtr",
  "IsCompact.tendsto_subseq",
  "CompleteSpace",
  "ContinuousLinearMap",
  "MeasureTheory.MemLp",
  "Distribution"
]

/-- Search terms that did not locate a terminal mountain-pass theorem in pinned mathlib. -/
def absentTerminalSearchTerms : List String := [
  "MountainPass",
  "mountain pass",
  "Palais",
  "Smale",
  "PalaisSmale",
  "critical point theorem",
  "minimax critical point",
  "Cerami",
  "deformation lemma"
]

/--
Readiness conditions for replacing the current statement-shape artifact by a
terminal repo-local wrapper theorem.

The wrapper may only be introduced once either the proof body is local to this
repository or an upstream dependency has been pinned/imported and validated by
the local Lake project.
-/
structure TerminalWrapperReadiness where
  exactTerminalStatementSelected : Prop
  localProofBodyAvailable : Prop
  pinnedUpstreamDependencyValidates : Prop
  wrapperTheoremLocallyChecked : Prop
  publicBackfillSeriallyMerged : Prop
  theoremTreeBudgetChecked : Prop

/--
C007 completion gate for a terminal mountain-pass wrapper.

This gate deliberately keeps the current `StatementShape` artifact separate
from a completed theorem claim: anchor-only evidence is insufficient.
-/
def TerminalWrapperCreationGate (R : TerminalWrapperReadiness) : Prop :=
  R.exactTerminalStatementSelected ∧
    (R.localProofBodyAvailable ∨ R.pinnedUpstreamDependencyValidates) ∧
      R.wrapperTheoremLocallyChecked ∧
        R.publicBackfillSeriallyMerged ∧
          R.theoremTreeBudgetChecked

/-- Missing local proof body and missing pinned upstream validation block C007 closure. -/
theorem not_terminalWrapperCreationGate_without_proof_source
    (R : TerminalWrapperReadiness)
    (hlocal : ¬ R.localProofBodyAvailable)
    (hupstream : ¬ R.pinnedUpstreamDependencyValidates) :
    ¬ TerminalWrapperCreationGate R := by
  intro hgate
  exact hgate.2.1.elim hlocal hupstream

/-- Missing local validation of the wrapper theorem blocks C007 closure. -/
theorem not_terminalWrapperCreationGate_without_local_wrapper_check
    (R : TerminalWrapperReadiness)
    (hchecked : ¬ R.wrapperTheoremLocallyChecked) :
    ¬ TerminalWrapperCreationGate R := by
  intro hgate
  exact hchecked hgate.2.2.1

/-- Current machine-proof debt classification for the mountain-pass artifact. -/
def machineProofDebtClassification : List String := [
  "formalization_debt: the classical mountain pass lemma is known mathematics, but this repository has no terminal Lean proof body",
  "not_repo_local_closed: the current artifact validates statement-shape, minimax, deformation-interface, and Palais-Smale limit-passage scaffolding only",
  "no_completed_repo_local_integration_debt: C006 found no terminal external Lean 4 theorem to pin/import/check during accessible search",
  "completion_gate: replace StatementShape by a terminal repo-local wrapper only after local proof body or pinned upstream dependency validates with lake env lean or lake build"
]

/-- C007 public-doc integration payload for the serialized integrator. -/
def terminalWrapperGateAuditC007 : List String := [
  "S1-M-164-C007 is a wrapper-replacement gate, not a completed terminal theorem",
  "current wrapper status: StatementShape is a checked statement-shape boundary, not a proof of the mountain pass lemma",
  "proof-source requirement: local_proof_body or external_upstream_pinned must validate in the repo before a terminal wrapper theorem is introduced",
  "anchor-only prohibition: a URL, module, or theorem name alone cannot close the child or parent theorem",
  "current external-anchor result: no terminal MountainPass or PalaisSmale theorem was found in pinned mathlib or other accessible local pinned dependencies",
  "public-doc action: keep the public child unchecked until wrapper theorem validation or a concrete integration blocker is recorded"
]

/--
C008 readiness conditions for merging the private Stage1 audit into the
authoritative public surface.

This is a documentation-integration gate, not a proof of the mountain pass
lemma.  It records the serial merge conditions that must be true before a
public blueprint/todo/status update is marked complete.
-/
structure PublicSurfaceMergeReadiness where
  directLeanValidationPassed : Prop
  noPlaceholderProofs : Prop
  noCompletedRepoLocalIntegrationDebt : Prop
  blueprintUpdateSerialized : Prop
  todoUpdateSerialized : Prop
  statusDocsSerialized : Prop
  authoritativeSurfaceSynchronized : Prop

/--
C008 public-surface merge gate.

Parallel child workers may prepare this payload, but public planning documents
must be updated only by a serialized integrator after validation and debt-gate
results are synchronized.
-/
def PublicSurfaceMergeGate (R : PublicSurfaceMergeReadiness) : Prop :=
  R.directLeanValidationPassed ∧
    R.noPlaceholderProofs ∧
      R.noCompletedRepoLocalIntegrationDebt ∧
        R.blueprintUpdateSerialized ∧
          R.todoUpdateSerialized ∧
            R.statusDocsSerialized ∧
              R.authoritativeSurfaceSynchronized

/-- Missing serialized public-doc updates block the C008 public merge gate. -/
theorem not_publicSurfaceMergeGate_without_serial_public_docs
    (R : PublicSurfaceMergeReadiness)
    (hblueprint : ¬ R.blueprintUpdateSerialized)
    (_htodo : ¬ R.todoUpdateSerialized)
    (_hstatus : ¬ R.statusDocsSerialized) :
    ¬ PublicSurfaceMergeGate R := by
  intro hgate
  exact hblueprint hgate.2.2.2.1

/-- Missing repo-local validation blocks the C008 public merge gate. -/
theorem not_publicSurfaceMergeGate_without_direct_validation
    (R : PublicSurfaceMergeReadiness)
    (hlean : ¬ R.directLeanValidationPassed) :
    ¬ PublicSurfaceMergeGate R := by
  intro hgate
  exact hlean hgate.1

/-- C008 public-doc integration payload for the serialized integrator. -/
def publicSurfaceMergeAuditC008 : List String := [
  "S1-M-164-C008 is serialized public-surface integration work, not terminal proof work",
  "owned Lean artifact status: S1_M_164.lean is a checked statement-shape and partial scaffold for the mountain pass lemma",
  "public-doc constraint: child workers must not edit Stage1 blueprint, todo, README, status, or shared import aggregators directly",
  "merge prerequisite: direct Lean validation, placeholder scan, and no-completed-state repo_local_integration_debt gate must be synchronized before public checklist updates",
  "completion boundary: keep THM-M-1271 not completed under formalization_debt until a local proof body or pinned upstream dependency validates the terminal theorem",
  "serial action: integrator may merge the prepared backfill text into blueprint/todo/status docs after collecting child ledgers C001-C008"
]

/-! ## Audit probes -/

#check fderiv
#check ContDiff
#check Path
#check Path.source
#check Path.target
#check IsLocalMin
#check IsLocalExtr
#check IsCompact.tendsto_subseq
#check CriticalPoint
#check PalaisSmaleSequence
#check PalaisSmaleAt
#check PalaisSmaleAt.subseq
#check PalaisSmaleSequence.energy_eq_of_subseq_tendsto
#check PalaisSmaleSequence.criticalPoint_of_subseq_tendsto
#check PalaisSmaleSequence.limit_criticalPoint_and_energy_eq
#check PalaisSmaleAt.exists_criticalPoint_and_energy_eq
#check PalaisSmaleAt.exists_mountainPassCriticalPoint_of_ps_sequence
#check MountainPassLevel
#check MountainPassMinimaxFormula
#check MountainPassLevel.to_minimaxFormula
#check MountainPassMinimaxFormula.to_level
#check mountainPassLevel_iff_minimaxFormula
#check PathLoweringDeformation
#check MountainPassLevel.not_pathLoweringDeformation
#check MinimaxDeformationLemma
#check MinimaxDeformationLemma.exists_ps_sequence
#check StatementShape
#check TerminalWrapperReadiness
#check TerminalWrapperCreationGate
#check not_terminalWrapperCreationGate_without_proof_source
#check not_terminalWrapperCreationGate_without_local_wrapper_check
#check machineProofDebtClassification
#check terminalWrapperGateAuditC007
#check PublicSurfaceMergeReadiness
#check PublicSurfaceMergeGate
#check not_publicSurfaceMergeGate_without_serial_public_docs
#check not_publicSurfaceMergeGate_without_direct_validation
#check publicSurfaceMergeAuditC008

end S1_M_164
end Stage1
end AwesomeTheorems
