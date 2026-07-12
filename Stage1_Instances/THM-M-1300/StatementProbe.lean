import Mathlib.Analysis.Distribution.TemperedDistribution

/-!
Elaboration probe for the THM-M-1300 statement blocker.

This checks only that the pinned environment contains standard substrates from
which a future, source-selected Triebel-Lizorkin definition might be built. It
does not define a Triebel-Lizorkin space or select a theorem about one: the
catalog record does not determine either without additional source evidence.
-/

open MeasureTheory

#check TemperedDistribution
#check SchwartzMap
#check MemLp
#check eLpNorm
