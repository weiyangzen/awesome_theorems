import Mathlib.Algebra.Polynomial.Eval.Defs
import Mathlib.Analysis.Complex.Basic
import Mathlib.Topology.MetricSpace.Pseudo.Defs

/-!
# THM-M-1477 discovery-only intake probe

These checks authenticate pinned polynomial-evaluation, complex-norm, and metric-region interfaces
adjacent to possible A-stability encodings. They do not define a numerical method, stability
function, multistep polynomial pair, A-stability predicate, or Dahlquist barrier theorem.
-/

#check Polynomial.eval
#check Polynomial.eval₂
#check norm
#check Complex.normSq
#check Metric.mem_closedBall

#print axioms Polynomial.eval_mul
#print axioms Complex.normSq_mul
