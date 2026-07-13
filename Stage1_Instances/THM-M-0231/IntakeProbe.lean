import Mathlib.Analysis.Meromorphic.FactorizedRational
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Cotangent
import Mathlib.CategoryTheory.CofilteredSystem

/-!
# THM-M-0231 discovery-only intake probe

These checks authenticate pinned meromorphic, finite-divisor, and cotangent-series interfaces near
the catalog topic. They do not define arbitrary principal parts, select a canonical
Mittag-Leffler proposition, or prove the target. The category-theoretic declaration is checked only
to make the homonym boundary explicit.
-/

#check MeromorphicAt
#check MeromorphicOn
#check meromorphicOrderAt
#check MeromorphicOn.divisor
#check Function.FactorizedRational.meromorphicNFOn
#check Function.FactorizedRational.divisor
#check cotTerm
#check summable_cotTerm
#check cot_series_rep
#check CategoryTheory.Functor.IsMittagLeffler
