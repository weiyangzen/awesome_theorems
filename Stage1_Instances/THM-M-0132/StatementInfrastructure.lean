import Mathlib.AlgebraicGeometry.EllipticCurve.Weierstrass
import Mathlib.NumberTheory.ModularForms.Basic
import Mathlib.NumberTheory.ModularForms.CongruenceSubgroups

/-!
# THM-M-0132 statement infrastructure

This module checks the two object families needed by the modularity theorem in the pinned
environment. It deliberately does not define a modularity predicate: pinned mathlib does not
provide the newform, conductor, or elliptic-curve/modular-form compatibility data needed to give
that predicate its source-faithful meaning.
-/

namespace Stage1Instances.THM_M_0132.StatementInfrastructure

open Matrix
open scoped MatrixGroups ModularForm

/-- The pinned representation of a Weierstrass curve over the rationals. -/
abbrev RationalWeierstrassCurve : Type := WeierstrassCurve Rat

/-- The pinned type of weight-two cusp forms at level `Gamma_0(N)`. This is only an object-model
probe; it does not assert normalization, Hecke-eigenform status, newness, or curve compatibility. -/
abbrev Gamma0WeightTwoCuspForm (N : Nat) : Type :=
  CuspForm (CongruenceSubgroup.Gamma0 N : Subgroup (GL (Fin 2) Real)) 2

#check WeierstrassCurve.IsElliptic
#check CongruenceSubgroup.Gamma0
#check CuspForm

end Stage1Instances.THM_M_0132.StatementInfrastructure
