import Mathlib.Probability.Martingale.OptionalStopping

/-!
# THM-M-1005 canonical statement

The repository gloss selects the finite-horizon strong `L^p` form of Doob's maximal
inequality for real-valued discrete-time martingales. This file freezes that proposition;
it does not assert or prove it.
-/

noncomputable section

open MeasureTheory
open scoped ENNReal NNReal MeasureTheory ProbabilityTheory

namespace Stage1Instances.THM_M_1005

universe u

/-- `max_{0 <= k <= n} |f k omega|`, with the nonempty range made explicit. -/
def runningAbsMax {Omega : Type u} (f : Nat -> Omega -> Real) (n : Nat) (omega : Omega) : Real :=
  (Finset.range (n + 1)).sup' Finset.nonempty_range_add_one fun k => |f k omega|

/--
The finite-horizon strong Doob `L^p` maximal inequality selected by the repository phrase
"moment estimate for a martingale maximum".

The exponent is an `ENNReal` because that is the exponent domain of mathlib's `eLpNorm`.
The assumptions `1 < p` and `p < top` make `p.toReal / (p.toReal - 1)` the usual conjugate
exponent constant. The horizon is inclusive (`0, ..., n`).
-/
def DoobLpMomentEstimate : Prop :=
  forall (Omega : Type u) [mOmega : MeasurableSpace Omega] (mu : Measure Omega)
    [IsFiniteMeasure mu] (G : Filtration Nat mOmega) (f : Nat -> Omega -> Real),
      Martingale f G mu ->
        forall (p : ENNReal), 1 < p -> p < (⊤ : ENNReal) -> forall n : Nat,
          eLpNorm (runningAbsMax f n) p mu <=
            ENNReal.ofReal (p.toReal / (p.toReal - 1)) * eLpNorm (f n) p mu

/-- Public canonical target for the statement phase. -/
abbrev Statement : Prop := DoobLpMomentEstimate.{u}

-- Structural mutations used by the statement fingerprint validator.
def MutationWeakL1 : Prop :=
  forall (Omega : Type u) [mOmega : MeasurableSpace Omega] (mu : Measure Omega)
    [IsFiniteMeasure mu] (G : Filtration Nat mOmega) (f : Nat -> Omega -> Real),
      Submartingale f G mu -> 0 <= f -> forall (epsilon : NNReal) (n : Nat),
        epsilon * mu {omega | (epsilon : Real) <=
          (Finset.range (n + 1)).sup' Finset.nonempty_range_add_one (fun k => f k omega)} <=
          ENNReal.ofReal (∫ omega, f n omega ∂mu)

def MutationNonnegativeSubmartingale : Prop :=
  forall (Omega : Type u) [mOmega : MeasurableSpace Omega] (mu : Measure Omega)
    [IsFiniteMeasure mu] (G : Filtration Nat mOmega) (f : Nat -> Omega -> Real),
      Submartingale f G mu -> 0 <= f ->
        forall (p : ENNReal), 1 < p -> p < (⊤ : ENNReal) -> forall n : Nat,
          eLpNorm (runningAbsMax f n) p mu <=
            ENNReal.ofReal (p.toReal / (p.toReal - 1)) * eLpNorm (f n) p mu

def MutationExtendedHorizon : Prop :=
  forall (Omega : Type u) [mOmega : MeasurableSpace Omega] (mu : Measure Omega)
    [IsFiniteMeasure mu] (G : Filtration Nat mOmega) (f : Nat -> Omega -> Real),
      Martingale f G mu ->
        forall (p : ENNReal), 1 < p -> p < (⊤ : ENNReal) -> forall n : Nat,
          eLpNorm
              (fun omega => (Finset.range (n + 2)).sup' Finset.nonempty_range_add_one
                fun k => |f k omega|) p mu <=
            ENNReal.ofReal (p.toReal / (p.toReal - 1)) * eLpNorm (f n) p mu

def MutationAllowsPOne : Prop :=
  forall (Omega : Type u) [mOmega : MeasurableSpace Omega] (mu : Measure Omega)
    [IsFiniteMeasure mu] (G : Filtration Nat mOmega) (f : Nat -> Omega -> Real),
      Martingale f G mu ->
        forall (p : ENNReal), 1 <= p -> p < (⊤ : ENNReal) -> forall n : Nat,
          eLpNorm (runningAbsMax f n) p mu <=
            ENNReal.ofReal (p.toReal / (p.toReal - 1)) * eLpNorm (f n) p mu

#check Statement
#print DoobLpMomentEstimate
#print MutationWeakL1
#print MutationNonnegativeSubmartingale
#print MutationExtendedHorizon
#print MutationAllowsPOne

end Stage1Instances.THM_M_1005
