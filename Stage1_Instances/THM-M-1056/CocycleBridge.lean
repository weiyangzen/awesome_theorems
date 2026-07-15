import IntegrabilityBridge
import Mathlib.Analysis.SpecificLimits.Basic

open Filter Function MeasureTheory
open scoped Matrix.Norms.L2Operator

noncomputable section

universe u v

namespace Stage1Instances.THM_M_1056

variable {Omega : Type u}
variable {E : Type v} [NormedAddCommGroup E] [NormedSpace Real E]
variable [FiniteDimensional Real E]

def bridgeCocycleVector (T : Omega -> Omega) (A : Omega -> E ≃L[Real] E) :
    Nat -> Omega -> E -> E
  | 0, _, x => x
  | n + 1, omega, x => A (T^[n] omega) (bridgeCocycleVector T A n omega x)

def matrixGenerator (A : Omega -> E ≃L[Real] E) :
    Omega -> Matrix (Fin (dE (E := E))) (Fin (dE (E := E))) Real :=
  fun omega => matrixOfCLM (A omega).toContinuousLinearMap

def matrixCocycle (B : Omega -> Matrix (Fin (dE (E := E))) (Fin (dE (E := E))) Real)
    (T : Omega -> Omega) : Nat -> Omega -> Matrix (Fin (dE (E := E))) (Fin (dE (E := E))) Real
  | 0, _ => 1
  | n + 1, omega => matrixCocycle B T n (T omega) * B omega

@[simp] theorem matrixCocycle_zero
    (B : Omega -> Matrix (Fin (dE (E := E))) (Fin (dE (E := E))) Real)
    (T : Omega -> Omega) (omega : Omega) :
    matrixCocycle (E := E) B T 0 omega = 1 := rfl

theorem matrixCocycle_succ
    (B : Omega -> Matrix (Fin (dE (E := E))) (Fin (dE (E := E))) Real)
    (T : Omega -> Omega) (n : Nat) (omega : Omega) :
    matrixCocycle (E := E) B T (n + 1) omega =
      matrixCocycle B T n (T omega) * B omega := rfl

theorem cocycleVector_succ_iterate
    (T : Omega -> Omega) (A : Omega -> E ≃L[Real] E)
    (n : Nat) (omega : Omega) (x : E) :
    bridgeCocycleVector T A (n + 1) omega x =
      A (T^[n] omega) (bridgeCocycleVector T A n omega x) := rfl

theorem cocycleVector_succ_base
    (T : Omega -> Omega) (A : Omega -> E ≃L[Real] E)
    (n : Nat) (omega : Omega) (x : E) :
    bridgeCocycleVector T A (n + 1) omega x =
      bridgeCocycleVector T A n (T omega) (A omega x) := by
  induction n generalizing omega x with
  | zero => rfl
  | succ n ih =>
      rw [cocycleVector_succ_iterate, ih]
      rw [iterate_succ_apply]
      rfl

theorem matrixCocycle_generator_apply
    (T : Omega -> Omega) (A : Omega -> E ≃L[Real] E)
    (n : Nat) (omega : Omega) (x : E) :
    Matrix.toEuclideanCLM (𝕜 := Real)
        (matrixCocycle (matrixGenerator A) T n omega)
        (coordEquiv (E := E) x) =
      coordEquiv (E := E) (bridgeCocycleVector T A n omega x) := by
  induction n generalizing omega x with
  | zero =>
      simp [matrixCocycle, bridgeCocycleVector]
  | succ n ih =>
      rw [matrixCocycle_succ, map_mul]
      change Matrix.toEuclideanCLM (𝕜 := Real)
          (matrixCocycle (matrixGenerator A) T n (T omega))
          (Matrix.toEuclideanCLM (𝕜 := Real) (matrixGenerator A omega)
            (coordEquiv (E := E) x)) = _
      rw [show Matrix.toEuclideanCLM (𝕜 := Real) (matrixGenerator A omega)
          (coordEquiv (E := E) x) = coordEquiv (E := E) (A omega x) by
        rw [matrixGenerator, toEuclideanCLM_matrixOfCLM, conjugateCLM_apply]
        rfl]
      rw [ih]
      rw [cocycleVector_succ_base]

end Stage1Instances.THM_M_1056

