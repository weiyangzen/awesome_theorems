import Mathlib.GroupTheory.GroupAction.Basic

/-!
# THM-M-1531 statement substrate probe

This file checks only the group-action vocabulary needed by a future exact
Higgs-mechanism statement. It is not the canonical target.
-/

namespace Stage1Instances.THM_M_1531

universe uG uV

/-- The unbroken transformations at a proposed vacuum are its stabilizer. -/
def UnbrokenAt (G : Type uG) (V : Type uV) [Group G] [MulAction G V]
    (vacuum : V) : Set G :=
  {g | g • vacuum = vacuum}

/-- A proper unbroken sector means that at least one transformation moves the vacuum. -/
def BreaksSomeSymmetry (G : Type uG) (V : Type uV) [Group G] [MulAction G V]
    (vacuum : V) : Prop :=
  ∃ g : G, g ∉ UnbrokenAt G V vacuum

theorem one_mem_unbrokenAt (G : Type uG) (V : Type uV) [Group G] [MulAction G V]
    (vacuum : V) : (1 : G) ∈ UnbrokenAt G V vacuum := by
  simp [UnbrokenAt]

end Stage1Instances.THM_M_1531

set_option pp.explicit true in
#check Stage1Instances.THM_M_1531.BreaksSomeSymmetry
