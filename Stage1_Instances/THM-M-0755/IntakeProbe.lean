import Mathlib.Computability.Halting
import Mathlib.MeasureTheory.Constructions.Polish.Basic
import Mathlib.ModelTheory.Complexity
import Mathlib.SetTheory.Descriptive.Tree

/-!
Discovery-only API checks adjacent to possible analytical-hierarchy encodings.

This file does not select, state, or prove the target. In particular,
`MeasureTheory.AnalyticSet` is a boldface descriptive-set-theory notion and
`Descriptive.tree` is only generic tree infrastructure; neither is credited as Kleene's
lightface analytical hierarchy.
-/

#check PrimrecPred
#check ComputablePred
#check REPred
#check Set (Set Nat)
#check FirstOrder.Language.BoundedFormula
#check FirstOrder.Language.BoundedFormula.IsPrenex
#check FirstOrder.Language.BoundedFormula.toPrenex
#check FirstOrder.Language.BoundedFormula.realize_toPrenex
#check Descriptive.tree
#check Descriptive.Tree.mem_of_prefix
#check MeasureTheory.AnalyticSet
#check MeasureTheory.analyticSet_iff_exists_polishSpace_range
