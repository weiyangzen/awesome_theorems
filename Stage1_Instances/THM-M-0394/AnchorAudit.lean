import Mathlib.AlgebraicGeometry.Geometrically.Integral
import Mathlib.AlgebraicGeometry.Morphisms.Proper
import Mathlib.AlgebraicGeometry.Morphisms.Smooth
import Mathlib.AlgebraicGeometry.Properties
import Mathlib.RingTheory.DedekindDomain.SInteger
import Mathlib.NumberTheory.SiegelsLemma

/-!
# THM-M-0394 immutable anchor probe

This file elaborates the pinned mathlib declarations classified by the anchor
audit. They provide object-model infrastructure, or the unrelated linear
algebra theorem also called Siegel's lemma. None proves `Statement`.
-/

open CategoryTheory AlgebraicGeometry

universe u v

#check IsAffine
#check Smooth
#check GeometricallyIntegral
#check IsProper
#check Set.integer
#check Set.integer_valuation_le_one
#check Set.unit
#check Set.unitEquivUnitsInteger
#check Int.Matrix.exists_ne_zero_int_vec_norm_le
