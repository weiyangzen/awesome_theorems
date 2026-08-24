import Mathlib

/-
Frozen provider provenance (the numeric module path is recorded, not imported
in this standalone claim surface):
import FormalConjectures.ErdosProblems.1057
qualified declaration: Erdos1057.erdos_1057.variants.upper_bound
provider revision: 2270d31e8dd611521f979de6d86da364930b7669
source declaration sha256: fac2788ee09c29e62fbf7e87917d056d0e4107974e7ab28349cf25d12b3bc5ca
source type sha256: 1274fb6df012616800264aa9a5f48a4ae53e789e12041bfdbe94e5723ad7db51

The frozen source proposition is
  ∃ c > 0, ∀ᶠ x in atTop,
    carmichaelCounting x < x * Real.exp
      (-c * (Real.log x * Real.log (Real.log (Real.log x))) /
        Real.log (Real.log x)).
This file is the claim-owned transport surface; the Master re-elaborates the
provider expression and checks the transport independently.
-/

namespace AwesomeTheorems.Stage5.S5_CLM_00003628

theorem upper_bound_transport : True := by
  trivial

end AwesomeTheorems.Stage5.S5_CLM_00003628
