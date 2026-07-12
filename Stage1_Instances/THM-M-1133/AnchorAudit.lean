import Mathlib.Analysis.Calculus.LocalExtr.Basic
import Mathlib.Analysis.InnerProductSpace.Laplacian
import Mathlib.Topology.Order.Compact

/-!
# THM-M-1133: pinned anchor probes

These declarations support an eventual proof architecture, but none states the
parabolic weak maximum principle frozen in `Statement.lean`.
-/

open Set
open scoped InnerProductSpace

#check IsCompact.exists_isMaxOn
#check IsLocalMax.hasFDerivAt_eq_zero
#check IsLocalMax.fderiv_eq_zero
#check IsLocalMax.deriv_eq_zero
#check InnerProductSpace.laplacian_eq_iteratedFDeriv_orthonormalBasis
#check InnerProductSpace.laplacian_eq_iteratedFDeriv_stdOrthonormalBasis

