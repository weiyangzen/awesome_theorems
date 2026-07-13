import Mathlib.Analysis.Complex.UnitDisc.Basic
import Mathlib.Analysis.Analytic.Basic
import Mathlib.Analysis.Normed.Algebra.Basic
import Mathlib.Analysis.CStarAlgebra.GelfandDuality

/-!
# THM-M-0252 discovery-only intake probe

These checks authenticate pinned APIs adjacent to the unit disc, analytic functions, character
spaces, and maximal ideals. They do not define the intended `H∞` Banach algebra, select a density
or Bezout statement, or prove the corona theorem.
-/

#check Complex.UnitDisc
#check Complex.UnitDisc.norm_lt_one
#check AnalyticOnNhd
#check WeakDual.characterSpace
#check Ideal.IsMaximal
#check Ideal.toCharacterSpace
#check DenseRange
