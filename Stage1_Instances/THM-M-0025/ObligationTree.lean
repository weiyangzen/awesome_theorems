import Statement
import Mathlib.RingTheory.Polynomial.Basic

/-!
# THM-M-0025 conditional obligation composition

This module checks the exact child-to-root interfaces frozen by the obligation registry. The
pinned mathlib theorem remains an explicit premise. Installing that theorem as the canonical proof
belongs to the later proof phase.
-/

namespace Stage1Instances.THM_M_0025.ObligationTree

universe u

/-- Exact conclusion exported by the audited pinned Hilbert-basis theorem. -/
def ExactPolynomialAnchor : Prop :=
  forall {R : Type u} [CommRing R] [IsNoetherianRing R],
    IsNoetherianRing (Polynomial R)

/-- The every-ideal-is-finitely-generated interface used by the visible terminal body. -/
def EveryPolynomialIdealFG : Prop :=
  forall {R : Type u} [CommRing R] [IsNoetherianRing R],
    forall I : Ideal (Polynomial R), I.FG

/-- Checked transport from the exact anchor to finite generation of every polynomial ideal. -/
theorem everyPolynomialIdealFG_of_exactPolynomialAnchor
    (anchor : ExactPolynomialAnchor.{u}) : EveryPolynomialIdealFG.{u} := by
  intro R _ _ I
  exact (isNoetherianRing_iff_ideal_fg (Polynomial R)).1 (anchor (R := R)) I

/-- Checked transport from finite generation of every polynomial ideal to the canonical root. -/
theorem root_of_everyPolynomialIdealFG
    (idealFG : EveryPolynomialIdealFG.{u}) :
    Stage1Instances.THM_M_0025.HilbertBasisTheoremTarget.{u} := by
  intro R _ _
  exact (isNoetherianRing_iff_ideal_fg (Polynomial R)).2 (idealFG (R := R))

/-- Checked exact child-to-root composition. The audited anchor is still an explicit premise. -/
theorem root_of_exactPolynomialAnchor
    (anchor : ExactPolynomialAnchor.{u}) :
    Stage1Instances.THM_M_0025.HilbertBasisTheoremTarget.{u} :=
  root_of_everyPolynomialIdealFG
    (everyPolynomialIdealFG_of_exactPolynomialAnchor anchor)

#check Polynomial.isNoetherianRing
#check Ideal.is_fg_degreeLE
#check Ideal.leadingCoeffNth
#check Ideal.mem_leadingCoeffNth
#check Polynomial.degree_sub_lt
#print axioms everyPolynomialIdealFG_of_exactPolynomialAnchor
#print axioms root_of_everyPolynomialIdealFG
#print axioms root_of_exactPolynomialAnchor

end Stage1Instances.THM_M_0025.ObligationTree
