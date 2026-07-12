import Mathlib.Probability.Process.Kolmogorov
import Mathlib.MeasureTheory.Measure.Typeclasses.Probability
import Mathlib.Topology.MetricSpace.Holder

/-!
# THM-M-1083 proof execution

Checked proof bodies for the part of the frozen Kolmogorov--Chentsov route supported by the pinned
mathlib environment.  The terminal modification construction is deliberately not postulated here.
-/

noncomputable section

open MeasureTheory Set
open scoped ENNReal NNReal

namespace Stage1Instances.THM_M_1083.Proof

universe u

abbrev TimeInterval (T : ℝ) := Set.Icc (0 : ℝ) T
abbrev RealProcess (T : ℝ) (Ω : Type u) := TimeInterval T → Ω → ℝ

def IsModification {T : ℝ} {Ω : Type u} [MeasurableSpace Ω]
    (P : Measure Ω) (X Y : RealProcess T Ω) : Prop :=
  ∀ t, X t =ᵐ[P] Y t

def HasHolderPath {T : ℝ} {Ω : Type u} (Y : RealProcess T Ω)
    (gamma : ℝ≥0) (ω : Ω) : Prop :=
  ∃ K : ℝ≥0, HolderWith K gamma (fun t => Y t ω)

def KolmogorovContinuity : Prop :=
  ∀ (Ω : Type u) [MeasurableSpace Ω] (P : Measure Ω) [IsProbabilityMeasure P]
      (T alpha beta : ℝ) (C : ℝ≥0) (X : RealProcess T Ω),
    0 < T →
    0 < alpha →
    0 < beta →
    (∀ t, Measurable (X t)) →
    (∀ s t,
      ∫⁻ ω, edist (X s ω) (X t ω) ^ alpha ∂P ≤
        (C : ℝ≥0∞) * edist s t ^ (1 + beta)) →
    ∃ Y : RealProcess T Ω,
      IsModification P X Y ∧
        ∀ gamma : ℝ≥0,
          0 < gamma →
          (gamma : ℝ) < beta / alpha →
          ∀ᵐ ω ∂P, HasHolderPath Y gamma ω

/-- The canonical hypotheses form mathlib's Kolmogorov-process substrate, with no loss or changed
exponent.  This closes frozen obligation `M1083-N-KOLMOGOROV`. -/
theorem isKolmogorovProcess_of_increment
    {Ω : Type u} [MeasurableSpace Ω] (P : Measure Ω)
    {T alpha beta : ℝ} {C : ℝ≥0} {X : RealProcess T Ω}
    (halpha : 0 < alpha) (hbeta : 0 < beta)
    (hmeas : ∀ t, Measurable (X t))
    (hmoment : ∀ s t,
      ∫⁻ ω, edist (X s ω) (X t ω) ^ alpha ∂P ≤
        (C : ℝ≥0∞) * edist s t ^ (1 + beta)) :
    ProbabilityTheory.IsKolmogorovProcess X P alpha (1 + beta) C := by
  exact ProbabilityTheory.IsKolmogorovProcess.mk_of_secondCountableTopology
    hmeas hmoment halpha (by linarith)

/-- The exponent produced by the `d = 1`, `q = 1 + beta` specialization is exactly the exponent
in the frozen target. -/
theorem exponent_transport {alpha beta gamma : ℝ} :
    gamma < ((1 + beta) - 1) / alpha ↔ gamma < beta / alpha := by
  ring_nf

/-- `HolderOnWith` on the full subtype is the target's global `HolderWith` predicate. -/
theorem holderOnUniv_to_holderWith {T Ω : Type*} [PseudoEMetricSpace T]
    {Y : T → Ω → ℝ} {K gamma : ℝ≥0} {ω : Ω}
    (h : HolderOnWith K gamma (fun t => Y t ω) Set.univ) :
    HolderWith K gamma (fun t => Y t ω) := by
  exact holderOnWith_univ.mp h

/-- Fixed-time equality returned in the reverse orientation still gives the frozen modification
relation. -/
theorem modification_of_reverse {T : ℝ} {Ω : Type u} [MeasurableSpace Ω]
    {P : Measure Ω} {X Y : RealProcess T Ω} (h : ∀ t, Y t =ᵐ[P] X t) :
    IsModification P X Y := by
  intro t
  exact (h t).symm

#check isKolmogorovProcess_of_increment
#check exponent_transport
#check holderOnUniv_to_holderWith
#check modification_of_reverse

end Stage1Instances.THM_M_1083.Proof
