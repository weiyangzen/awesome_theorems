import Mathlib.LinearAlgebra.Matrix.ToLin
import Mathlib.Data.Complex.Basic

/-!
# THM-M-1526: exact free Dirac factorization statement

This module freezes the algebraic operator statement selected by the rev-5.6
intake. It does not prove that concrete spacetime derivatives or gamma matrices
satisfy its hypotheses.
-/

namespace Stage1Instances.THM_M_1526

universe u

/-- A complex-linear operator on the chosen space of sufficiently regular
spinor fields. -/
abbrev SpinorOperator (Psi : Type u) [AddCommGroup Psi] [Module Complex Psi] :=
  Module.End Complex Psi

/-- The exact algebraic hypotheses needed to square a constant-coefficient
free Dirac operator. The metric is encoded through the scalar coefficients
`g`; the factor `2` is cancelled in the diagonal/off-diagonal expansion below.
-/
structure FreeDiracData (I : Type) (Psi : Type u)
    [Fintype I] [DecidableEq I] [AddCommGroup Psi] [Module Complex Psi] where
  gamma : I -> SpinorOperator Psi
  deriv : I -> SpinorOperator Psi
  g : I -> I -> Complex
  mass : Complex
  clifford_diagonal : forall mu,
    gamma mu * gamma mu = g mu mu • (1 : SpinorOperator Psi)
  clifford_offDiagonal : forall mu nu, mu != nu ->
    gamma mu * gamma nu + gamma nu * gamma mu =
      (g mu nu + g nu mu) • (1 : SpinorOperator Psi)
  gamma_deriv_commute : forall mu nu,
    gamma mu * deriv nu = deriv nu * gamma mu
  deriv_commute : forall mu nu,
    deriv mu * deriv nu = deriv nu * deriv mu

/-- The massless first-order part `sum_mu gamma^mu partial_mu`. -/
def slash {I : Type} {Psi : Type u}
    [Fintype I] [DecidableEq I] [AddCommGroup Psi] [Module Complex Psi]
    (D : FreeDiracData I Psi) : SpinorOperator Psi :=
  Finset.univ.sum fun mu => D.gamma mu * D.deriv mu

/-- The componentwise Klein-Gordon operator represented by the metric
contraction of two commuting derivatives. -/
def kleinGordon {I : Type} {Psi : Type u}
    [Fintype I] [DecidableEq I] [AddCommGroup Psi] [Module Complex Psi]
    (D : FreeDiracData I Psi) : SpinorOperator Psi :=
  Finset.univ.sum fun mu =>
    Finset.univ.sum fun nu => D.g mu nu • (D.deriv mu * D.deriv nu)

/-- The exact target: the two conjugate free Dirac factors compose to the
Klein-Gordon operator minus the squared mass, and every vector killed by the
right factor is consequently killed by that second-order operator. -/
def FreeDiracFactorizationTarget : Prop :=
  forall (I : Type) (Psi : Type u)
    [Fintype I] [DecidableEq I] [AddCommGroup Psi] [Module Complex Psi]
    (D : FreeDiracData I Psi),
      (slash D + D.mass • (1 : SpinorOperator Psi)) *
          (slash D - D.mass • (1 : SpinorOperator Psi)) =
        kleinGordon D - D.mass ^ 2 • (1 : SpinorOperator Psi) /\
      forall psi : Psi,
        (slash D - D.mass • (1 : SpinorOperator Psi)) psi = 0 ->
          (kleinGordon D - D.mass ^ 2 • (1 : SpinorOperator Psi)) psi = 0

/-- A named alternate encoding of the same factorization and consequence. -/
abbrev DirectConsequenceShape : Prop := FreeDiracFactorizationTarget.{u}

/-- Checked identity with the direct consequence encoding. -/
theorem freeDiracFactorizationTarget_iff_directConsequenceShape :
    FreeDiracFactorizationTarget.{u} <-> DirectConsequenceShape.{u} :=
  Iff.rfl

-- Separately elaborated structural mutations for statement-identity tests.
def mutationRemovedDerivativeCommutation : Prop :=
  forall (I : Type) (Psi : Type u)
    [Fintype I] [DecidableEq I] [AddCommGroup Psi] [Module Complex Psi],
      (I -> SpinorOperator Psi) -> (I -> SpinorOperator Psi) -> True

def mutationChangedScalarDomain : Prop :=
  forall (I : Type) (Psi : Type u)
    [Fintype I] [DecidableEq I] [AddCommGroup Psi] [Module Rat Psi], True

def mutationChangedBinderScope : Prop :=
  forall (I : Type) [Fintype I] [DecidableEq I],
    forall (Psi : Type u) [AddCommGroup Psi] [Module Complex Psi],
      Nonempty (FreeDiracData I Psi) -> True

def mutationPositiveMassOnly : Prop :=
  forall (I : Type) (Psi : Type u)
    [Fintype I] [DecidableEq I] [AddCommGroup Psi] [Module Complex Psi]
    (D : FreeDiracData I Psi), D.mass != 0 -> True

/-- The target explicitly includes the zero-mass boundary. -/
def zeroMassBoundary {I : Type} {Psi : Type u}
    [Fintype I] [DecidableEq I] [AddCommGroup Psi] [Module Complex Psi]
    (D : FreeDiracData I Psi) : FreeDiracData I Psi :=
  { D with mass := 0 }

end Stage1Instances.THM_M_1526

set_option pp.explicit true in
#print Stage1Instances.THM_M_1526.FreeDiracFactorizationTarget
