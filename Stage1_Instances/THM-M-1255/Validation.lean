import Statement
import Mathlib.Analysis.Distribution.FourierMultiplier
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-1255 same-worker differential validation

This module deliberately imports neither `Proof` nor `ObligationTree`. It reconstructs the
coordinate-derivative commutation and polynomial action directly from the canonical statement
definitions. The analytic division and fundamental-solution packages remain open, so this is
neither a root proof nor the distinct-runner verification required for release.
-/

noncomputable section

open scoped SchwartzMap

namespace Stage1Instances.THM_M_1255.Validation

universe u

/-- Differential reconstruction of the frozen coordinate-derivative commutation obligation. -/
theorem differentialCoordinateDerivativesCommute
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

private def validationCoordinatePowerHom
    (ι : Type u) [Fintype ι] [DecidableEq ι] (i : ι) :
    Multiplicative ℕ →* OperatorEnd ι where
  toFun n := (coordinateDerivative ι i) ^ n.toAdd
  map_one' := pow_zero _
  map_mul' _ _ := pow_add _ _ _

private def validationCoordinatePowers
    (ι : Type u) [Fintype ι] [DecidableEq ι] :
    Multiplicative (ι → ℕ) →* OperatorEnd ι :=
  MonoidHom.noncommPiCoprod (validationCoordinatePowerHom ι) fun i j _ _ _ =>
    (differentialCoordinateDerivativesCommute ι i j).pow_pow _ _

private def validationExponentAction
    (ι : Type u) [Fintype ι] [DecidableEq ι] :
    Multiplicative (ι →₀ ℕ) →* OperatorEnd ι :=
  (validationCoordinatePowers ι).comp
    Finsupp.addEquivFunOnFinite.toAddMonoidHom.toMultiplicative

private def validationPolynomialAction
    (ι : Type u) [Fintype ι] [DecidableEq ι] :
    MvPolynomial ι ℂ →ₐ[ℂ] OperatorEnd ι :=
  AddMonoidAlgebra.lift ℂ (OperatorEnd ι) (ι →₀ ℕ) (validationExponentAction ι)

private theorem validationExponentActionSingle
    (ι : Type u) [Fintype ι] [DecidableEq ι] (i : ι) :
    validationExponentAction ι (Multiplicative.ofAdd (Finsupp.single i 1)) =
      coordinateDerivative ι i := by
  classical
  change validationCoordinatePowers ι
      (Multiplicative.ofAdd (Finsupp.addEquivFunOnFinite (Finsupp.single i 1))) = _
  have hfun : Finsupp.addEquivFunOnFinite (Finsupp.single i 1) =
      Pi.single i (1 : ℕ) := Finsupp.equivFunOnFinite_single i 1
  rw [hfun]
  change validationCoordinatePowers ι
      (fun j => Multiplicative.ofAdd ((Pi.single i (1 : ℕ) : ι → ℕ) j)) = _
  rw [show (fun j => Multiplicative.ofAdd ((Pi.single i (1 : ℕ) : ι → ℕ) j)) =
      Pi.mulSingle i (Multiplicative.ofAdd 1) by
        funext j
        simp only [Pi.single_apply, Pi.mulSingle_apply]
        split <;> rfl]
  exact MonoidHom.noncommPiCoprod_mulSingle (validationCoordinatePowerHom ι) i
    (Multiplicative.ofAdd 1)

private theorem validationPolynomialActionMapX
    (ι : Type u) [Fintype ι] [DecidableEq ι] (i : ι) :
    validationPolynomialAction ι (MvPolynomial.X i) = coordinateDerivative ι i := by
  classical
  change validationPolynomialAction ι
      (AddMonoidAlgebra.single (Finsupp.single i 1) 1) = coordinateDerivative ι i
  rw [validationPolynomialAction, AddMonoidAlgebra.lift_single, one_smul,
    validationExponentActionSingle]

/-- Canonical action reconstructed without importing the proof or obligation-tree modules. -/
def differentialPolynomialAction
    (ι : Type u) [Fintype ι] [DecidableEq ι] :
    PolynomialDifferentialAction ι where
  toAlgHom := validationPolynomialAction ι
  map_X := validationPolynomialActionMapX ι

/-- Canonical, premise-free action-existence witness for frozen obligation `M1255-C-ACTION`. -/
theorem differentialPolynomialActionExists :
    ∀ (ι : Type u) [Fintype ι] [DecidableEq ι],
      Nonempty (PolynomialDifferentialAction ι) := by
  intro ι _ _
  exact ⟨differentialPolynomialAction ι⟩

assert_no_sorry differentialCoordinateDerivativesCommute
assert_no_sorry differentialPolynomialActionExists
#print sorries differentialCoordinateDerivativesCommute differentialPolynomialActionExists
#print axioms differentialCoordinateDerivativesCommute
#print axioms differentialPolynomialActionExists

end Stage1Instances.THM_M_1255.Validation
