import Mathlib.Analysis.InnerProductSpace.Harmonic.Basic
import Mathlib.Analysis.InnerProductSpace.Harmonic.Constructions
import Mathlib.Analysis.Complex.Harmonic.MeanValue
import Mathlib.LinearAlgebra.Complex.FiniteDimensional

/-!
# THM-M-1146 anchor-audit probes

These probes check the strongest supporting declarations found in the pinned
mathlib tree. None is a Schwarz reflection theorem or closes the frozen root.
-/

open Complex InnerProductSpace

#check HarmonicOnNhd
#check HarmonicOnNhd.neg
#check harmonicAt_congr_nhds
#check HarmonicAt.eventually
#check Complex.conjCLE
#check HarmonicOnNhd.circleAverage_eq

#print axioms HarmonicOnNhd.neg
#print axioms harmonicAt_congr_nhds
#print axioms HarmonicAt.eventually
#print axioms HarmonicOnNhd.circleAverage_eq
