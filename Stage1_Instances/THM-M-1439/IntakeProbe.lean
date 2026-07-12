import Mathlib.Analysis.Analytic.Composition
import Mathlib.Analysis.Complex.Basic
import Mathlib.Analysis.Normed.Operator.Basic
import Mathlib.Logic.Function.Iterate
import Mathlib.Topology.Separation.Connected

/-!
# THM-M-1439 discovery-only intake probe

These checks authenticate adjacent pinned complex, analytic, iteration, semiconjugacy, compactness,
connectedness, and linear-operator APIs. They do not define quadratic-like germs, hybrid classes,
or renormalization and do not select or prove a Lyubich theorem.
-/

#check Complex
#check AnalyticAt
#check AnalyticAt.comp
#check Function.iterate_succ_apply
#check Function.Semiconj
#check Function.Semiconj.iterate_right
#check IsCompact
#check IsConnected
#check IsPreconnected
#check ContinuousLinearMap
#check ContinuousLinearMap.comp
