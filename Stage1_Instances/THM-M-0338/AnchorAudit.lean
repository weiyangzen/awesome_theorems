import Mathlib.Analysis.CStarAlgebra.GelfandNaimarkSegal
import Mathlib.Analysis.CStarAlgebra.ContinuousLinearMap
import Mathlib.Analysis.InnerProductSpace.l2Space

/-!
# THM-M-0338: pinned anchor probes

These checks identify the strongest relevant APIs found in the pinned mathlib
revision. They are statement infrastructure, not a Kadison-Singer proof.
-/

#check PositiveLinearMap
#check PositiveLinearMap.GNS
#check StarSubalgebra
#check StarSubalgebra.cstarAlgebra
#check ContinuousLinearMap
#check HilbertBasis
#check HilbertBasis.orthonormal
#check HilbertBasis.hasSum_repr

