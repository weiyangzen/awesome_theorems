import Statement
import Mathlib.Combinatorics.Compactness
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0819 obligation-tree composition harness

This module checks only the exact child-to-parent interfaces selected by the
frozen obligation registry. The positive-width package is an explicit premise;
no proof of Dilworth's theorem is asserted here. The width-zero branch is the
already checked conservative boundary result from the statement phase.
-/

set_option autoImplicit false

namespace Stage1Instances.THM_M_0819_Obligations

open Stage1Instances.THM_M_0819

universe u

/-- The printed positive-width part of Dilworth's Theorem 1.1. This is an open
proof interface, not an inhabitant of the theorem. -/
def PositiveWidthPackage : Prop :=
  forall (alpha : Type u) [PartialOrder alpha] (k : Nat),
    0 < k ->
    (forall s : Set alpha, HasExactly (k + 1) s -> IsDependent s) ->
    (exists s : Set alpha,
      HasExactly k s /\ IsAntichain (fun x y : alpha => x <= y) s) ->
    exists C : Fin k -> Set alpha, IsDisjointChainDecomposition k C

/-- The separately checked width-zero extension of the printed theorem. -/
def ZeroWidthPackage : Prop :=
  forall (alpha : Type u) [PartialOrder alpha],
    (forall s : Set alpha, HasExactly 1 s -> IsDependent s) ->
    (exists s : Set alpha,
      HasExactly 0 s /\ IsAntichain (fun x y : alpha => x <= y) s) ->
    exists C : Fin 0 -> Set alpha, IsDisjointChainDecomposition 0 C

/-- Both exhaustive width branches bundled without hiding either premise. -/
def WidthBranchPackage : Prop :=
  PositiveWidthPackage.{u} /\ ZeroWidthPackage.{u}

/-- The statement phase's checked unfolding relationship. -/
def RootTransportPackage : Prop :=
  DilworthPrimaryTarget.{u} <-> ExpandedDilworthPrimaryTarget.{u}

/-- The exact root conclusion delivered by terminal assembly. This distinct
interface lets the canonical root consume one terminal child by identity. -/
def TerminalRootPackage : Prop :=
  DilworthPrimaryTarget.{u}

/-- The statement phase proves the width-zero branch from its dependence
hypothesis; the antichain witness is retained in the exact interface. -/
theorem zeroWidth_of_statement : ZeroWidthPackage.{u} := by
  intro alpha _ hdep _hindependent
  letI : IsEmpty alpha := zeroWidth_forces_isEmpty alpha hdep
  exact zeroWidth_decomposition alpha

/-- Conditional branch bundle. The substantive positive-width child is named
and consumed; the checked boundary child remains explicit. -/
theorem widthBranches_of_positive_and_zero
    (positive : PositiveWidthPackage.{u})
    (zero : ZeroWidthPackage.{u}) : WidthBranchPackage.{u} :=
  And.intro positive zero

/-- Exhaustive recomposition of the `k = 0` and `0 < k` branches. -/
theorem expanded_of_widthBranches
    (branches : WidthBranchPackage.{u}) :
    ExpandedDilworthPrimaryTarget.{u} := by
  intro alpha _ k hdep hindependent
  rcases Nat.eq_zero_or_pos k with rfl | hk
  . exact branches.2 alpha hdep hindependent
  . exact branches.1 alpha k hk hdep hindependent

/-- Local wrapper exposing the exact statement transport. -/
theorem checked_root_transport : RootTransportPackage.{u} :=
  dilworthPrimaryTarget_iff_expanded

/-- Exact conditional branch-to-root certificate. -/
theorem root_of_widthBranches
    (transport : RootTransportPackage.{u})
    (branches : WidthBranchPackage.{u}) : TerminalRootPackage.{u} :=
  transport.mpr (expanded_of_widthBranches branches)

/-- Exact terminal-to-canonical-root identity certificate. -/
theorem root_of_terminal
    (terminal : TerminalRootPackage.{u}) : DilworthPrimaryTarget.{u} :=
  terminal

/-- Combined conditional harness. It does not inhabit the positive-width
premise and therefore supplies no proof of Dilworth's theorem. -/
theorem root_of_positiveWidth
    (positive : PositiveWidthPackage.{u}) : DilworthPrimaryTarget.{u} :=
  root_of_terminal <| root_of_widthBranches checked_root_transport
    (widthBranches_of_positive_and_zero positive zeroWidth_of_statement)

#check PositiveWidthPackage
#check ZeroWidthPackage
#check WidthBranchPackage
#check RootTransportPackage
#check TerminalRootPackage
#check Finset.rado_selection_subtype
#check zeroWidth_of_statement
#check widthBranches_of_positive_and_zero
#check expanded_of_widthBranches
#check checked_root_transport
#check root_of_widthBranches
#check root_of_terminal
#check root_of_positiveWidth

/-! Fully explicit interface serialization for composition-fingerprint checks. -/
set_option pp.explicit true in
set_option pp.universes true in
#print PositiveWidthPackage
set_option pp.explicit true in
set_option pp.universes true in
#print ZeroWidthPackage
set_option pp.explicit true in
set_option pp.universes true in
#print WidthBranchPackage
set_option pp.explicit true in
set_option pp.universes true in
#print RootTransportPackage
set_option pp.explicit true in
set_option pp.universes true in
#print TerminalRootPackage

assert_no_sorry zeroWidth_of_statement
assert_no_sorry widthBranches_of_positive_and_zero
assert_no_sorry expanded_of_widthBranches
assert_no_sorry checked_root_transport
assert_no_sorry root_of_widthBranches
assert_no_sorry root_of_terminal
assert_no_sorry root_of_positiveWidth

#print sorries zeroWidth_of_statement widthBranches_of_positive_and_zero
  expanded_of_widthBranches checked_root_transport root_of_widthBranches
  root_of_terminal root_of_positiveWidth
#print axioms zeroWidth_of_statement
#print axioms widthBranches_of_positive_and_zero
#print axioms expanded_of_widthBranches
#print axioms checked_root_transport
#print axioms root_of_widthBranches
#print axioms root_of_terminal
#print axioms root_of_positiveWidth

end Stage1Instances.THM_M_0819_Obligations
