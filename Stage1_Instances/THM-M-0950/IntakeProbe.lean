import Mathlib.Combinatorics.HalesJewett
import Mathlib.Data.Finset.Density
import Mathlib.Data.Fintype.BigOperators

/-!
Discovery-only substrate checks for a later source-selected density Hales-Jewett target.

This file introduces no theorem declaration. In particular, the ordinary Hales-Jewett theorem
checked below is not the density theorem and receives no proof credit for `THM-M-0950`.
-/

namespace Stage1Instances.THM_M_0950

open Combinatorics

/-- A finite-density predicate in the prospective ambient word space. -/
def HasDensityAtLeast {alpha iota : Type*} [Fintype alpha] [Fintype iota]
    [Fintype (iota -> alpha)] (delta : NNRat) (A : Finset (iota -> alpha)) : Prop :=
  delta <= A.dens

/-- The line-containment conclusion used by a prospective finite encoding. -/
def ContainsCombinatorialLine {alpha iota : Type*}
    (A : Finset (iota -> alpha)) : Prop :=
  Exists fun line : Line alpha iota => forall x, line x ∈ A

#check Combinatorics.Line
#check Combinatorics.Line.IsMono
#check Combinatorics.Line.exists_mono_in_high_dimension
#check Finset.dens
#check Fintype.card_pi
#check HasDensityAtLeast
#check ContainsCombinatorialLine

end Stage1Instances.THM_M_0950
