import Mathlib.NumberTheory.ModularForms.Cusps

#check Subgroup.IsArithmetic
#check IsCusp
#check CuspOrbits
#check isCusp_SL2Z_iff
#check Subgroup.IsArithmetic.isCusp_iff_isCusp_SL2Z

example (G : Subgroup (GL (Fin 2) ℝ)) [G.IsArithmetic] : Finite (CuspOrbits G) := by
  infer_instance
