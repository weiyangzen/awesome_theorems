import Mathlib.MeasureTheory.Integral.Layercake
import Mathlib.MeasureTheory.Measure.Lebesgue.VolumeOfBalls

/-!
# THM-M-1285: pinned anchor probes

These declarations support the distribution-function and centered-ball route
to Schwarz rearrangement. None constructs a symmetric decreasing
rearrangement or proves the frozen target.
-/

open MeasureTheory Metric
open scoped ENNReal

#check measurable_norm
#check measurableSet_lt
#check EuclideanSpace.volume_ball
#check InnerProductSpace.volume_ball
#check measure_ball_pos
#check measure_ball_ne_top
#check lintegral_eq_lintegral_meas_lt
#check lintegral_eq_lintegral_meas_le
