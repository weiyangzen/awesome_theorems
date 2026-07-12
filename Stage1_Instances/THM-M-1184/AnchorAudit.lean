import Mathlib.MeasureTheory.Measure.ProbabilityMeasure
import Mathlib.MeasureTheory.Measure.Prokhorov
import Mathlib.MeasureTheory.Integral.Bochner.Basic
import Mathlib.Analysis.Convex.StoneSeparation
import Mathlib.Analysis.LocallyConvex.Separation

/-!
# THM-M-1184 anchor-audit probes

These checks deliberately do not wrap or prove the rev-5.6 target. They bind
the audit ledger to adjacent declarations actually present in pinned mathlib.
Repo-local historical candidates are checked by elaborating their source file
directly because this worker's reused build cache has no project-module olean.
-/

#check exists_convex_convex_compl_subset
#check geometric_hahn_banach_open
#check geometric_hahn_banach_compact_closed
#check isCompact_closure_of_isTightMeasureSet
#check MeasureTheory.ProbabilityMeasure.le_liminf_measure_open_of_tendsto
