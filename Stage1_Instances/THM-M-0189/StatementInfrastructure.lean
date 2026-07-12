import Mathlib.Analysis.Convex.Body
import Mathlib.MeasureTheory.Constructions.HaarToSphere

/-!
Pinned-environment probes for the THM-M-0189 statement gate.

This file is not the canonical Minkowski-problem target.  It checks the nearby
mathlib vocabulary and records that the defining surface-area-measure interface
needed by that target is absent at this revision.
-/

open Metric MeasureTheory

#check ConvexBody
#check ConvexBody.carrier
#check ConvexBody.isCompact
#check Measure
#check Measure.toSphere
#check MeasureTheory.integral
#check sphere

#check_failure ConvexBody.HasNonemptyInterior
#check_failure ConvexBody.surfaceAreaMeasure
#check_failure Measure.IsSurfaceAreaMeasure
#check_failure Measure.notConcentratedOnGreatSubsphere

