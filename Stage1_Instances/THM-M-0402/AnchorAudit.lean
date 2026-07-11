import Mathlib.RingTheory.DedekindDomain.SInteger

/-!
# THM-M-0402 immutable anchor probe

This file checks the pinned mathlib object-model declarations found by the
anchor audit. They define S-units and their valuation behavior, but do not
state or prove finiteness of nondegenerate S-unit equations.
-/

open IsDedekindDomain

#check Set.integer
#check Set.integer_valuation_le_one
#check Set.unit
#check Set.unit_valuation_eq_one
#check Set.unitEquivUnitsInteger
