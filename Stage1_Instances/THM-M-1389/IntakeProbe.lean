import Mathlib.Analysis.Asymptotics.AsymptoticEquivalent
import Mathlib.Analysis.InnerProductSpace.Spectrum

/-!
# THM-M-1389 discovery-only intake probe

These checks authenticate adjacent pinned asymptotic and finite-dimensional spectral APIs. They do
not define a spectral counting function, select a PDE or Sturm-Liouville operator, state the
leading factor, or prove THM-M-1389.
-/

#check Asymptotics.IsEquivalent
#check Asymptotics.IsEquivalent.isLittleO
#check Asymptotics.IsEquivalent.tendsto_atTop_iff
#check LinearMap.IsSymmetric.eigenvalues
#check LinearMap.IsSymmetric.eigenvalues_antitone
#check LinearMap.IsSymmetric.card_filter_eigenvalues_eq
#check LinearMap.IsSymmetric.eigenvectorBasis
