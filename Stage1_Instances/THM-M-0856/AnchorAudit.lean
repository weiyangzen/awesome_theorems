import Mathlib.Combinatorics.SimpleGraph.Tutte

set_option autoImplicit false

/-!
# THM-M-0856 pinned mathlib anchor audit

This module checks an exact adapter from the frozen finite-simple-graph target to
`SimpleGraph.tutte` at the repository's pinned mathlib revision.  It is candidate evidence for the
anchor-audit phase, not an accepted proof, trust closure, or release declaration.
-/

namespace Stage1Instances.THM_M_0856.AnchorAudit

universe u

open SimpleGraph

/-- A literal copy of the expanded proposition frozen by `Statement.lean`. -/
def ExactTarget.{v} : Prop :=
  forall {V : Type v} (G : SimpleGraph V),
    [Finite V] ->
      (Exists fun M : G.Subgraph => M.IsPerfectMatching) <->
        forall U : Set V,
          ((⊤ : G.Subgraph).deleteVerts U).coe.oddComponents.ncard <= U.ncard

/-- Exact adapter over the pinned mathlib terminal theorem. -/
theorem exactTarget_mathlib_candidate : ExactTarget.{u} := by
  intro V G _
  simpa only [SimpleGraph.IsTutteViolator, not_lt] using (SimpleGraph.tutte (G := G))

#check @SimpleGraph.IsTutteViolator
#check @SimpleGraph.not_isTutteViolator_of_isPerfectMatching
#check @SimpleGraph.IsTutteViolator.empty
#check @SimpleGraph.exists_isTutteViolator
#check @SimpleGraph.tutte
#print SimpleGraph.tutte
#print sorries SimpleGraph.tutte
#print sorries exactTarget_mathlib_candidate
#print axioms SimpleGraph.not_isTutteViolator_of_isPerfectMatching
#print axioms SimpleGraph.exists_isTutteViolator
#print axioms SimpleGraph.tutte
#print axioms exactTarget_mathlib_candidate

end Stage1Instances.THM_M_0856.AnchorAudit

set_option pp.universes true in
set_option pp.explicit true in
#print Stage1Instances.THM_M_0856.AnchorAudit.ExactTarget
