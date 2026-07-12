import Mathlib.Analysis.Matrix.Normed
import Mathlib.Analysis.Calculus.Deriv.Basic

/-!
# THM-M-1550 independent validation probe

This module reconstructs the frozen proposition and its proof without importing
the proof-phase module. It is a same-worker corroboration probe, not the
distinct-runner independent verification required for release.
-/

noncomputable section

namespace Stage1Instances.THM_M_1550.Validation

universe u

abbrev LaxMatrix (n : Type u) := Matrix n n Complex

def MatrixCommutator {n : Type u} [Fintype n] [DecidableEq n]
    (A B : LaxMatrix n) : LaxMatrix n :=
  A * B - B * A

def LaxEquationOn {n : Type u} [Fintype n] [DecidableEq n]
    (L P : Real -> LaxMatrix n) (timeDomain : Set Real) : Prop :=
  forall t, timeDomain t ->
    HasDerivWithinAt L (MatrixCommutator (P t) (L t)) timeDomain t

def IsospectralOn {n : Type u} [Fintype n] [DecidableEq n]
    (L : Real -> LaxMatrix n) (timeDomain : Set Real) : Prop :=
  forall t0, timeDomain t0 -> forall t, timeDomain t ->
    spectrum Complex (L t) = spectrum Complex (L t0)

def ConjugatesAt {n : Type u} [Fintype n] [DecidableEq n]
    (L : Real -> LaxMatrix n) (t0 t : Real) : Prop :=
  exists U : (LaxMatrix n)ˣ,
    L t = (U : LaxMatrix n) * L t0 * (U⁻¹ : LaxMatrix n)

def ConjugatingEvolutionOn {n : Type u} [Fintype n] [DecidableEq n]
    (L : Real -> LaxMatrix n) (timeDomain : Set Real) : Prop :=
  forall t0, timeDomain t0 -> forall t, timeDomain t -> ConjugatesAt L t0 t

def LaxPairIsospectrality : Prop :=
  forall (n : Type u) [Fintype n] [DecidableEq n]
    (L P : Real -> LaxMatrix n) (timeDomain : Set Real),
      LaxEquationOn L P timeDomain ->
      ConjugatingEvolutionOn L timeDomain -> IsospectralOn L timeDomain

/-- Separately written direct proof of the frozen proposition shape. -/
theorem independentLaxPairIsospectrality : LaxPairIsospectrality.{u} := by
  intro n _ _ L P timeDomain _hLax hEvolution t0 ht0 t ht
  obtain ⟨U, hU⟩ := hEvolution t0 ht0 t ht
  rw [hU, ← Matrix.GeneralLinearGroup.coe_inv U]
  exact spectrum.units_conjugate

#print axioms independentLaxPairIsospectrality

end Stage1Instances.THM_M_1550.Validation
