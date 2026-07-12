import Mathlib.Analysis.Matrix.Normed
import Mathlib.Analysis.Calculus.Deriv.Basic

/-!
# THM-M-1550 conditional obligation composition

This file repeats the frozen statement interface and checks only the planned
child-to-root composition. The spectrum-under-conjugation leaf is an explicit
premise, so this certificate does not prove or close the theorem.
-/

noncomputable section

namespace Stage1Instances.THM_M_1550.ObligationTree

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

def Root : Prop :=
  forall (n : Type u) [Fintype n] [DecidableEq n]
    (L P : Real -> LaxMatrix n) (timeDomain : Set Real),
      LaxEquationOn L P timeDomain ->
      ConjugatingEvolutionOn L timeDomain -> IsospectralOn L timeDomain

def SpectrumUnderConjugation : Prop :=
  forall (n : Type u) [Fintype n] [DecidableEq n]
    (L : Real -> LaxMatrix n) (t0 t : Real),
      ConjugatesAt L t0 t ->
      spectrum Complex (L t) = spectrum Complex (L t0)

/-- Consume the supplied evolution at each pair of times and pass its witness
to the spectrum leaf. The Lax-equation premise is retained exactly but is
logically redundant under the stronger conjugating-evolution premise. -/
theorem root_compose (spectrumLeaf : SpectrumUnderConjugation.{u}) : Root.{u} := by
  intro n _ _ L P timeDomain _hLax hEvolution t0 ht0 t ht
  exact spectrumLeaf n L t0 t (hEvolution t0 ht0 t ht)

#print axioms root_compose

end Stage1Instances.THM_M_1550.ObligationTree
