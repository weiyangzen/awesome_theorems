import Mathlib.Analysis.Calculus.LocalExtr.Basic
import Mathlib.Analysis.InnerProductSpace.Laplacian
import Mathlib.Topology.Order.Compact

/-!
# THM-M-1188: pinned mathlib anchor probes

These are proof-architecture dependencies available at the pinned mathlib
revision. None states a time-dependent parabolic maximum principle.
-/

open Set
open scoped InnerProductSpace

#check IsCompact.exists_isMaxOn
#check IsLocalMax.hasFDerivAt_eq_zero
#check IsLocalMax.fderiv_eq_zero
#check IsLocalMax.deriv_eq_zero
#check InnerProductSpace.laplacian_eq_iteratedFDeriv_orthonormalBasis
#check InnerProductSpace.laplacian_eq_iteratedFDeriv_stdOrthonormalBasis
