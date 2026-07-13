import Mathlib.Analysis.Complex.Hadamard
import Mathlib.MeasureTheory.Function.LpSpace.Basic

/-!
# THM-M-0296 discovery-only intake probe

These checks authenticate pinned `Lp`, `MemLp`, induced `Lp`-map, and Hadamard three-lines
interfaces that may be relevant to a future Riesz-Thorin formalization. They do not select a
canonical Riesz-Thorin statement, define the interpolated operator, or prove the catalog target.
-/

#check MeasureTheory.Lp
#check MeasureTheory.MemLp
#check ContinuousLinearMap.compLp
#check ContinuousLinearMap.compLpL
#check Complex.HadamardThreeLines.norm_le_interpStrip_of_mem_verticalClosedStrip₀₁
#check Complex.HadamardThreeLines.norm_le_interp_of_mem_verticalClosedStrip₀₁'
#check Complex.HadamardThreeLines.norm_le_interp_of_mem_verticalClosedStrip'
