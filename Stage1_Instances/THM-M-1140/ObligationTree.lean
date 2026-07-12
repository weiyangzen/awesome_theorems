import Statement

/-!
# THM-M-1140 conditional obligation composition

This module checks the parent composition chosen by the frozen architecture.
Local harmonic rigidity and connected propagation remain explicit premises; no
proof of either analytic package is asserted here.
-/

open Set
open InnerProductSpace

namespace Stage1Instances.THM_M_1140

/-- Local mean-value consequence required at every interior maximizer. -/
def InteriorLocalRigidity : Prop :=
  ∀ (n : Nat) (Omega : Set (Space n)) (u : Space n -> Real)
      (y : Space n),
    IsOpen Omega → y ∈ Omega → HarmonicOnNhd u Omega →
    (∀ z ∈ Omega, u z ≤ u y) →
    ∃ V : Set (Space n), IsOpen V ∧ y ∈ V ∧ V ⊆ Omega ∧
      ∀ z ∈ V, u z = u y

/-- Pure topological propagation package for a locally constant level set in a
connected domain. It is kept separate from harmonic local rigidity. -/
def ConnectedLevelPropagation : Prop :=
  ∀ (n : Nat) (Omega : Set (Space n)) (u : Space n -> Real) (c : Real),
    Omega.Nonempty → IsOpen Omega → IsConnected Omega → ContinuousOn u Omega →
    (∃ y ∈ Omega, u y = c) →
    (∀ y ∈ Omega, u y = c →
      ∃ V : Set (Space n), IsOpen V ∧ y ∈ V ∧ V ⊆ Omega ∧
        ∀ z ∈ V, u z = c) →
    ∀ x ∈ Omega, u x = c

/-- Checked composition of the local analytic and connected-topological
packages into the exact canonical proposition. -/
theorem harmonicStrongMaximumPrinciple_of_packages
    (localRigidity : InteriorLocalRigidity)
    (propagation : ConnectedLevelPropagation) :
    HarmonicStrongMaximumPrinciple := by
  intro n Omega u x0 hne hopen hconn hx0 hharm hmax
  apply propagation n Omega u (u x0) hne hopen hconn hharm.continuousOn
  · exact ⟨x0, hx0, rfl⟩
  · intro y hyOmega hyLevel
    obtain ⟨V, hVopen, hyV, hVOmega, hVeq⟩ :=
      localRigidity n Omega u y hopen hyOmega hharm
        (fun z hz => by simpa [hyLevel] using hmax z hz)
    exact ⟨V, hVopen, hyV, hVOmega, fun z hz => (hVeq z hz).trans hyLevel⟩

#print axioms harmonicStrongMaximumPrinciple_of_packages

end Stage1Instances.THM_M_1140
