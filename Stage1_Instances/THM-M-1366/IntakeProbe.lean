import Mathlib.Dynamics.Flow

/-!
# THM-M-1366 discovery-only intake probe

These checks authenticate adjacent pinned interfaces for flows, orbits, invariant sets,
homeomorphisms, semiconjugacy, and factors. They do not choose a perturbation topology, state a
structural-stability proposition, or provide a proof body.
-/

#check Flow
#check Flow.orbit
#check IsInvariant
#check Flow.IsSemiconjugacy
#check Flow.IsFactorOf
#check Flow.toHomeomorph
#check Homeomorph
#check Function.Semiconj
