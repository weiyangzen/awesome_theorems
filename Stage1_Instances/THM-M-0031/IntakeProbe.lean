import Mathlib.Algebra.CharP.MixedCharZero
import Mathlib.RingTheory.AdicCompletion.Completeness
import Mathlib.RingTheory.AdicCompletion.LocalRing
import Mathlib.RingTheory.MvPowerSeries.Basic

/-!
# THM-M-0031 discovery-only intake probe

These checks authenticate pinned interfaces adjacent to a future Cohen structure theorem
statement. They do not choose between coefficient-ring existence, power-series quotient,
equicharacteristic, mixed-characteristic, or regular-local formulations, and they provide no proof
credit for any such root.
-/

#check IsLocalRing
#check IsLocalRing.maximalIdeal
#check IsLocalRing.ResidueField
#check IsLocalRing.residue
#check IsNoetherianRing
#check IsHausdorff
#check IsPrecomplete
#check IsAdicComplete
#check AdicCompletion
#check AdicCompletion.isAdicComplete
#check isLocalRing_of_isAdicComplete_maximal
#check MvPowerSeries
#check MvPowerSeries.C
#check MvPowerSeries.X
#check MixedCharZero
#check split_equalCharZero_mixedCharZero

#print axioms AdicCompletion.isAdicComplete
#print axioms isLocalRing_of_isAdicComplete_maximal
