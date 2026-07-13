import Mathlib.RepresentationTheory.Semisimple

/-!
# THM-M-0067 uncredited statement candidate probe

This module checks that the complemented-subrepresentation reading of Maschke's theorem can be
stated using the pinned semisimple-representation vocabulary without importing the proof-bearing
Maschke module. It is not the canonical target: the repository source does not decide whether
"completely reducible" means this complement condition or a finite-dimensional direct sum of
irreducibles.
-/

namespace Stage1Instances.THM_M_0067

universe u v w

/-- The direct pinned complement-form candidate. This receives feasibility evidence only. -/
def ComplementedSubrepresentationCandidate : Prop :=
  forall (k : Type u) (G : Type v) (V : Type w)
    [Field k] [Group G] [Finite G] [NeZero (Nat.card G : k)]
    [AddCommGroup V] [Module k V] (rho : Representation k G V),
    Representation.IsSemisimpleRepresentation rho

set_option pp.universes true in
set_option pp.explicit true in
#print ComplementedSubrepresentationCandidate

end Stage1Instances.THM_M_0067
