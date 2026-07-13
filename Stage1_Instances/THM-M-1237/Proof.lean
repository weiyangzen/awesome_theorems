import «ObligationTree»

/-!
# THM-M-1237 proved proof units

This module closes only the frozen representative-construction obligation.
The two analytic estimate families remain open and are not assumed here.
-/

noncomputable section

open MeasureTheory Filter
open scoped ENNReal NNReal Topology

namespace Stage1Rev56.THMM1237.Proof

open Stage1Rev56.THMM1237
open Stage1Rev56.THMM1237.ObligationTree

/-- The input function itself is a representative agreeing with the input
almost everywhere. This closes `M1237-C`; it supplies no regularity estimate. -/
theorem representativeFamily : RepresentativeFamily := by
  intro n hn Ω hΩm hΩb p α hp hα u ext
  exact ⟨u.function, Eventually.of_forall (fun _ => rfl)⟩

/-- One-dimensional space used to expose the quantifier error in the frozen
`ValueEstimateFamily` interface. -/
abbrev CounterexampleSpace := Space 1

private def zeroSingletonW1p :
    W1pData ({0} : Set CounterexampleSpace) 2 where
  function := 0
  weakGradient := 0
  functionMemLp := MemLp.zero
  gradientMemLp := MemLp.zero
  isWeakDerivative := by
    intro i φ _hφ
    simp [spatialDerivative]

private def zeroSingletonExtension : ExtensionData zeroSingletonW1p where
  extendedFunction := 0
  extendedGradient := 0
  agreesOnDomain := Eventually.of_forall (by simp [zeroSingletonW1p])
  functionMemLp := MemLp.zero
  gradientMemLp := MemLp.zero
  isWeakDerivative := by
    intro i φ _hφ
    simp [spatialDerivative]
  operatorBound := 0
  normBound := by simp [zeroSingletonW1p]

private def singletonSpike (x : CounterexampleSpace) : ℝ :=
  if x = 0 then 1 else 0

private theorem singletonSpike_ae_zero :
    ∀ᵐ x ∂volume.restrict ({0} : Set CounterexampleSpace),
      singletonSpike x = zeroSingletonW1p.function x := by
  rw [Measure.restrict_singleton']
  simp

/-- The frozen value-estimate premise is inconsistent with valid zero data: it
quantifies over every a.e.-equal representative and every constant, including
the point-modified representative above and `C = 0`. -/
theorem not_valueEstimateFamily : ¬ ValueEstimateFamily := by
  intro value
  have impossible := value 1 (by norm_num) ({0} : Set CounterexampleSpace)
    (measurableSet_singleton 0) Bornology.isBounded_singleton
    2 (1 / 2 : ℝ≥0) (by norm_num) (by norm_num)
    zeroSingletonW1p zeroSingletonExtension
    singletonSpike singletonSpike_ae_zero 0 0 (by simp)
  norm_num [singletonSpike] at impossible

#check representativeFamily
#print axioms representativeFamily
#check not_valueEstimateFamily
#print axioms not_valueEstimateFamily

end Stage1Rev56.THMM1237.Proof
