import Mathlib.RingTheory.Noetherian.Defs

/-!
# THM-M-0028 discovery-only intake probe

These checks authenticate the pinned Noetherian-ring definitions and ascending-chain interfaces
adjacent to the catalog claim. They do not freeze the canonical Lean target, inspect a proof body,
perform the later anchor audit, or grant proof credit.
-/

universe u

variable {R : Type u} [CommRing R]

#check Ideal
#check IsNoetherian
#check IsNoetherianRing
#check isNoetherianRing_iff_ideal_fg
#check (monotone_stabilizes_iff_noetherian (R := R) (M := R))
#check isNoetherian_iff
#check set_has_maximal_iff_noetherian
#print axioms monotone_stabilizes_iff_noetherian
#print axioms isNoetherianRing_iff_ideal_fg
