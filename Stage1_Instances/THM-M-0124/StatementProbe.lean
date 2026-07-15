import Mathlib.NumberTheory.ModularForms.Cusps

/-!
# THM-M-0124 statement substrate probe

This file checks the closest concrete pinned APIs available for a future Manin-Drinfeld
statement: congruence subgroups, cusps, cusp orbits, and finiteness of those orbits. It does not
define the canonical target. In particular, it supplies no compactified modular curve, curve
Jacobian or degree-zero Picard group, cuspidal divisor class, or Abel-Jacobi map.
-/

set_option autoImplicit false

namespace Stage1Instances.THM_M_0124

#check CongruenceSubgroup.IsCongruenceSubgroup
#check CongruenceSubgroup.Gamma
#check IsCusp
#check CuspOrbits

/-- A congruence subgroup has finitely many cusp orbits in the pinned cusp API. This is substrate
evidence only; finiteness of the cusp set is not the Manin-Drinfeld torsion conclusion. -/
example (Gamma : Subgroup (Matrix.SpecialLinearGroup (Fin 2) ℤ))
    (hGamma : CongruenceSubgroup.IsCongruenceSubgroup Gamma) :
    Finite (CuspOrbits (Gamma : Subgroup (GL (Fin 2) ℝ))) := by
  letI : Gamma.FiniteIndex := hGamma.finiteIndex
  infer_instance

end Stage1Instances.THM_M_0124
