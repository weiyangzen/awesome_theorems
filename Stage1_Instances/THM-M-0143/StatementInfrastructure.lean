import Mathlib.Combinatorics.Quiver.Basic

/-!
# THM-M-0143 statement infrastructure probe

The repository record names Nakajima quiver varieties but does not identify a proposition or fix
the data needed for their construction. This module therefore declares no canonical target. It
only checks the pinned combinatorial quiver API, without inventing representation spaces, a moment
map, stability data, a quotient, or a geometric conclusion.
-/

namespace Stage1Instances.THM_M_0143.StatementInfrastructure

universe u v

/-- The vertex-and-arrow API available in pinned mathlib. This is not a quiver variety. -/
abbrev ArrowFamily (V : Type u) [Quiver.{v} V] (source target : V) : Type v :=
  source ⟶ target

#check Quiver
#check ArrowFamily

end Stage1Instances.THM_M_0143.StatementInfrastructure
