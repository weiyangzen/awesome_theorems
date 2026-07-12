import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Topology.Algebra.InfiniteSum.ENNReal
import «Statement»

/-!
Typed interfaces for the frozen BDJ proof architecture.  The analytic and
combinatorial packages are deliberately hypotheses: this file checks only the
child-to-root composition and does not supply either missing proof body.
-/

namespace Stage1Instances.THM_M_1108

open Filter Topology
open scoped ENNReal NNReal Topology

noncomputable section

/-- Poissonized uniform-permutation CDF, retaining the canonical LIS statistic
but centering and scaling at the Poisson parameter. -/
def poissonizedLISCDF (n : ℕ) (t : ℝ) : ℝ :=
  ∑' N : ℕ,
    (Real.exp (-(n : ℝ)) * (n : ℝ) ^ N / (N.factorial : ℝ)) *
      ((Fintype.card {σ : Equiv.Perm (Fin N) //
          (lisLength σ : ℝ) ≤ 2 * Real.sqrt n + t * (n : ℝ) ^ (1 / 6 : ℝ)} : ℝ) /
        (Fintype.card (Equiv.Perm (Fin N)) : ℝ))

/-- The source's RSK/Toeplitz/Riemann--Hilbert analysis, exposed as the exact
pointwise Poissonized limit rather than hidden behind the root theorem. -/
def PoissonizedAsymptotics : Prop :=
  ∀ F : ℝ → ℝ, IsTracyWidomCDF F →
    ∀ t : ℝ, Tendsto (fun n : ℕ => poissonizedLISCDF n t) atTop (nhds (F t))

/-- The monotonicity and uniform estimates required to transfer the
Poissonized result back to permutations of each fixed size. -/
def DePoissonizationTransfer : Prop :=
  PoissonizedAsymptotics → CanonicalStatement

/-- Checked composition certificate for the two open terminal packages. -/
theorem canonicalStatement_of_poissonized_depoissonized
    (hPoissonized : PoissonizedAsymptotics)
    (hTransfer : DePoissonizationTransfer) : CanonicalStatement :=
  hTransfer hPoissonized

#check poissonizedLISCDF
#check PoissonizedAsymptotics
#check DePoissonizationTransfer
#check canonicalStatement_of_poissonized_depoissonized
#print axioms canonicalStatement_of_poissonized_depoissonized

end
end Stage1Instances.THM_M_1108
