import Mathlib.Probability.HasLaw
import Mathlib.MeasureTheory.Measure.LevyProkhorovMetric
import Mathlib.MeasureTheory.Constructions.Polish.Basic
import Mathlib.MeasureTheory.Function.ConvergenceInMeasure

open Filter MeasureTheory ProbabilityTheory Topology

-- Exact candidate declarations retained by the anchor audit.
#check LevyProkhorov.eq_convergenceInDistribution
#check LevyProkhorov.probabilityMeasureHomeomorph
#check ProbabilityTheory.HasLaw
#check ProbabilityTheory.HasLaw.map_eq
#check StandardBorelSpace
#check PolishSpace.measurableEquivOfNotCountable
#check TendstoInMeasure.exists_seq_tendsto_ae

-- The frozen target is checked separately: its path contains a hyphen, so it is not directly
-- importable under its underscore-separated Lean namespace.
