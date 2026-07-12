import Mathlib.Topology.Algebra.Module.LinearPMap
import Mathlib.Analysis.Normed.Operator.Basic

/-! # THM-M-0330 anchor audit

This checks only the pinned mathlib substrate used by the frozen statement.
It contains no Hille-Yosida proof or proof wrapper. -/

#check LinearPMap.IsClosed
#check LinearPMap.graph
#check ContinuousLinearMap.id
#check ContinuousLinearMap.comp
#check Dense
#check Filter.Tendsto

example {X : Type} [NormedAddCommGroup X] [NormedSpace ℝ X]
    (A : X →ₗ.[ℝ] X) : Prop :=
  Dense (A.domain : Set X) ∧ A.IsClosed
