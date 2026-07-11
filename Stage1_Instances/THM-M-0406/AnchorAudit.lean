import Mathlib.AlgebraicGeometry.Morphisms.Proper
import Mathlib.AlgebraicGeometry.Morphisms.Smooth
import Mathlib.AlgebraicGeometry.OpenImmersion
import Mathlib.NumberTheory.Height.NumberField
import Mathlib.NumberTheory.Height.Northcott
import Mathlib.RingTheory.DedekindDomain.SInteger

/-!
# THM-M-0406 anchor-audit probes

These checks identify genuine substrate available at the pinned mathlib revision.
None is the Corvaja--Zannier surface theorem or a proof of the canonical target.
-/

#check AlgebraicGeometry.Scheme
#check AlgebraicGeometry.IsProper
#check AlgebraicGeometry.Smooth
#check AlgebraicGeometry.IsOpenImmersion
#check NumberField.FinitePlace
#check Height.AdmissibleAbsValues
#check Northcott
#check Set.integer
#check Set.unit
#check Set.unitEquivUnitsInteger
