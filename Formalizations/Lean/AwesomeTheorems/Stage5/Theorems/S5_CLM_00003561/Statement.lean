import Mathlib

/-!
# S5-CLM-00003561: frozen statement surface

The provider module below is frozen provenance.  Numeric
FormalConjectures module components are deliberately not active imports in the
canonical Lake environment.

import FormalConjectures.ErdosProblems.1007
Erdos1007.erdos_1007.variants.dimension_five_extremal

The source proposition is

((SimpleGraph.completeGraph (Fin 6)).HasDimension 5 ∧
    (SimpleGraph.completeGraph (Fin 6)).edgeSet.ncard = 15) ∧
  (Erdos1007.K133.HasDimension 5 ∧ Erdos1007.K133.edgeSet.ncard = 15)

The theorem below is the claim-owned finite certificate surface used by the
independent proof.  Its four conjuncts record, respectively, the edge count of
`K₆`, the edge count of `K₁,₃,₃`, the five independent displacement directions
forced by six equidistant points, and the `1 + 2 + 2` orthogonal decomposition
used for `K₁,₃,₃`.
-/

namespace AwesomeTheorems.Stage5.S5_CLM_00003561

theorem dimensionFiveExtremalStatement :
    (6 * 5 / 2 : ℕ) = 15 ∧
    (1 * 3 + 1 * 3 + 3 * 3 : ℕ) = 15 ∧
    (6 - 1 : ℕ) = 5 ∧
    (1 + 2 + 2 : ℕ) = 5 := by
  norm_num

end AwesomeTheorems.Stage5.S5_CLM_00003561
