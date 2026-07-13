import ObligationTree
import Mathlib.Analysis.Distribution.FourierMultiplier

/-!
# THM-M-1255 proof execution

This module closes the frozen commutation and polynomial-action obligations. The arbitrary-symbol
tempered-distribution division and fundamental-solution obligations remain open, so this module does
not prove the Malgrange-Ehrenpreis root.
-/

noncomputable section

open scoped SchwartzMap

namespace Stage1Instances.THM_M_1255.Proof

universe u

/-- Distributional coordinate derivatives commute. This closes `M1255-L-COMMUTE`. -/
theorem coordinateDerivatives_commute
    (ι : Type u) [Fintype ι] [DecidableEq ι] (i j : ι) :
    Commute (coordinateDerivative ι i) (coordinateDerivative ι j) := by
  change coordinateDerivative ι i * coordinateDerivative ι j =
    coordinateDerivative ι j * coordinateDerivative ι i
  apply LinearMap.ext
  intro T
  change coordinateDerivative ι i (coordinateDerivative ι j T) =
    coordinateDerivative ι j (coordinateDerivative ι i T)
  simp only [coordinateDerivative]
  change
    LineDeriv.lineDerivOp (coordinateDirection ι i)
        (LineDeriv.lineDerivOp (coordinateDirection ι j) T) =
      LineDeriv.lineDerivOp (coordinateDirection ι j)
        (LineDeriv.lineDerivOp (coordinateDirection ι i) T)
  simp_rw [TemperedDistribution.lineDeriv_eq_fourierMultiplierCLM]
  rw [map_smul, map_smul, smul_smul, smul_smul]
  congr 1
  rw [TemperedDistribution.fourierMultiplierCLM_fourierMultiplierCLM_apply
        (by fun_prop) (by fun_prop),
      TemperedDistribution.fourierMultiplierCLM_fourierMultiplierCLM_apply
        (by fun_prop) (by fun_prop)]
  congr 2
  funext x
  simp [mul_comm]

/-- Powers of one coordinate derivative, viewed as a monoid homomorphism. -/
def coordinatePowerHom
    (ι : Type u) [Fintype ι] [DecidableEq ι] (i : ι) :
    Multiplicative ℕ →* OperatorEnd ι where
  toFun n := (coordinateDerivative ι i) ^ n.toAdd
  map_one' := pow_zero _
  map_mul' _ _ := pow_add _ _ _

/-- Evaluate a finite coordinate exponent vector as a commuting product of derivatives. -/
def coordinatePowers
    (ι : Type u) [Fintype ι] [DecidableEq ι] :
    Multiplicative (ι → ℕ) →* OperatorEnd ι :=
  MonoidHom.noncommPiCoprod (coordinatePowerHom ι) fun i j _ _ _ =>
    (coordinateDerivatives_commute ι i j).pow_pow _ _

/-- Evaluate a finitely supported exponent vector as a derivative endomorphism. -/
def exponentAction
    (ι : Type u) [Fintype ι] [DecidableEq ι] :
    Multiplicative (ι →₀ ℕ) →* OperatorEnd ι :=
  (coordinatePowers ι).comp
    Finsupp.addEquivFunOnFinite.toAddMonoidHom.toMultiplicative

/-- The constant-coefficient polynomial action on tempered distributions. -/
def polynomialAction
    (ι : Type u) [Fintype ι] [DecidableEq ι] :
    MvPolynomial ι ℂ →ₐ[ℂ] OperatorEnd ι :=
  AddMonoidAlgebra.lift ℂ (OperatorEnd ι) (ι →₀ ℕ) (exponentAction ι)

theorem exponentAction_single
    (ι : Type u) [Fintype ι] [DecidableEq ι] (i : ι) :
    exponentAction ι (Multiplicative.ofAdd (Finsupp.single i 1)) =
      coordinateDerivative ι i := by
  classical
  change coordinatePowers ι
      (Multiplicative.ofAdd (Finsupp.addEquivFunOnFinite (Finsupp.single i 1))) = _
  have hfun : Finsupp.addEquivFunOnFinite (Finsupp.single i 1) =
      Pi.single i (1 : ℕ) := Finsupp.equivFunOnFinite_single i 1
  rw [hfun]
  change coordinatePowers ι
      (fun j => Multiplicative.ofAdd ((Pi.single i (1 : ℕ) : ι → ℕ) j)) = _
  rw [show (fun j => Multiplicative.ofAdd ((Pi.single i (1 : ℕ) : ι → ℕ) j)) =
      Pi.mulSingle i (Multiplicative.ofAdd 1) by
        funext j
        simp only [Pi.single_apply, Pi.mulSingle_apply]
        split <;> rfl]
  exact MonoidHom.noncommPiCoprod_mulSingle (coordinatePowerHom ι) i
    (Multiplicative.ofAdd 1)

theorem polynomialAction_map_X
    (ι : Type u) [Fintype ι] [DecidableEq ι] (i : ι) :
    polynomialAction ι (MvPolynomial.X i) = coordinateDerivative ι i := by
  classical
  change polynomialAction ι
      (AddMonoidAlgebra.single (Finsupp.single i 1) 1) = coordinateDerivative ι i
  rw [polynomialAction, AddMonoidAlgebra.lift_single, one_smul,
    exponentAction_single]

/-- The differential action induced by the coordinate derivative algebra homomorphism. -/
def differentialAction
    (ι : Type u) [Fintype ι] [DecidableEq ι] :
    PolynomialDifferentialAction ι where
  toAlgHom := polynomialAction ι
  map_X := polynomialAction_map_X ι

/-- The exact frozen action package. This closes `M1255-C-ACTION`. -/
def polynomialActionPackage : PolynomialActionPackage.{u} where
  action := differentialAction

#print axioms Stage1Instances.THM_M_1255.Proof.coordinateDerivatives_commute
#print axioms Stage1Instances.THM_M_1255.Proof.exponentAction_single
#print axioms Stage1Instances.THM_M_1255.Proof.polynomialAction_map_X
#print axioms Stage1Instances.THM_M_1255.Proof.polynomialActionPackage

end Stage1Instances.THM_M_1255.Proof
