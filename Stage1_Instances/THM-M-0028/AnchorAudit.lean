import Mathlib.RingTheory.Noetherian.Defs

/-!
# THM-M-0028 immutable anchor probe

This module copies the frozen modern-unital target literally and checks the exact adapter to the
pinned mathlib declarations. It is candidate evidence only; it does not promote repository state.
-/

namespace Stage1Instances.THM_M_0028_AnchorAudit

universe u

/-- Literal audit copy of `Stage1Instances.THM_M_0028.IdealAscendingChainTarget`. -/
def ExactTarget : Prop :=
  forall {R : Type u} [CommRing R],
    (forall I : Ideal R, I.FG) ->
      forall f : Nat →o Ideal R,
        exists n, forall m, n <= m -> f n = f m

/-- Exact wrapper around the pinned finite-generation and chain-stabilization equivalences. -/
theorem exactTarget_mathlib_candidate : ExactTarget.{u} := by
  intro R _ hfg f
  have hNoetherian : IsNoetherianRing R :=
    (isNoetherianRing_iff_ideal_fg R).mpr hfg
  exact monotone_stabilizes_iff_noetherian.mpr hNoetherian f

#check monotone_stabilizes_iff_noetherian
#check isNoetherianRing_iff_ideal_fg
#check exactTarget_mathlib_candidate

#print monotone_stabilizes_iff_noetherian
#print isNoetherianRing_iff_ideal_fg
#print exactTarget_mathlib_candidate

#print sorries monotone_stabilizes_iff_noetherian
#print sorries isNoetherianRing_iff_ideal_fg
#print sorries exactTarget_mathlib_candidate

#print axioms monotone_stabilizes_iff_noetherian
#print axioms isNoetherianRing_iff_ideal_fg
#print axioms exactTarget_mathlib_candidate

set_option pp.universes true in
set_option pp.explicit true in
#print ExactTarget

end Stage1Instances.THM_M_0028_AnchorAudit
