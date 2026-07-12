import Mathlib.Data.Set.Basic

/-!
# THM-M-0696: completeness of classical propositional logic

This module freezes the exact object-language statement only. It does not prove completeness.
-/

namespace Stage1Instances.THM_M_0696

universe u

/-- Formulas over atoms `Atom`, using the classically complete basis false and implication. -/
inductive Formula (Atom : Type u) where
  | atom : Atom -> Formula Atom
  | falsum : Formula Atom
  | imp : Formula Atom -> Formula Atom -> Formula Atom
  deriving DecidableEq

namespace Formula

/-- Two-valued semantics for the false/implication basis. -/
def eval {Atom : Type u} (valuation : Atom -> Bool) : Formula Atom -> Bool
  | atom a => valuation a
  | falsum => false
  | imp phi psi => !eval valuation phi || eval valuation psi

end Formula

/-- A Boolean valuation satisfies every formula in a (possibly infinite) premise set. -/
def Satisfies {Atom : Type u} (valuation : Atom -> Bool) (Gamma : Set (Formula Atom)) : Prop :=
  forall phi, phi ∈ Gamma -> Formula.eval valuation phi = true

/-- Semantic consequence over all two-valued valuations. -/
def SemanticallyEntails {Atom : Type u} (Gamma : Set (Formula Atom))
    (phi : Formula Atom) : Prop :=
  forall valuation : Atom -> Bool, Satisfies valuation Gamma -> Formula.eval valuation phi = true

/-- Hilbert derivability from premises, with K, S, double-negation elimination, and modus ponens. -/
inductive Derives {Atom : Type u} (Gamma : Set (Formula Atom)) : Formula Atom -> Prop where
  | assumption {phi} : phi ∈ Gamma -> Derives Gamma phi
  | axiomK (phi psi) : Derives Gamma (.imp phi (.imp psi phi))
  | axiomS (phi psi chi) :
      Derives Gamma (.imp (.imp phi (.imp psi chi)) (.imp (.imp phi psi) (.imp phi chi)))
  | axiomDNE (phi) : Derives Gamma (.imp (.imp (.imp phi .falsum) .falsum) phi)
  | modusPonens {phi psi} : Derives Gamma (.imp phi psi) -> Derives Gamma phi -> Derives Gamma psi

/-- Exact target: semantic consequence implies derivability in the fixed classical Hilbert calculus. -/
def PropositionalCompletenessTarget : Prop :=
  forall (Atom : Type u) (Gamma : Set (Formula Atom)) (phi : Formula Atom),
    SemanticallyEntails Gamma phi -> Derives Gamma phi

/-- The direct expansion records the selected syntax, semantics, and calculus without aliases. -/
def ExpandedTarget : Prop :=
  forall (Atom : Type u) (Gamma : Set (Formula Atom)) (phi : Formula Atom),
    (forall valuation : Atom -> Bool,
      (forall psi, psi ∈ Gamma -> Formula.eval valuation psi = true) ->
        Formula.eval valuation phi = true) ->
      Derives Gamma phi

/-- Checked transport from the named canonical target to its direct semantic expansion. -/
theorem propositionalCompletenessTarget_iff_expandedTarget :
    PropositionalCompletenessTarget.{u} <-> ExpandedTarget.{u} := by
  rfl

-- Structural mutations are elaborated and then distinguished by `check_statement.py`.
def mutationRemovedSemanticHypothesis : Prop :=
  forall (Atom : Type u) (Gamma : Set (Formula Atom)) (phi : Formula Atom), Derives Gamma phi

def mutationChangedAtomDomain : Prop :=
  forall (Gamma : Set (Formula Nat)) (phi : Formula Nat),
    SemanticallyEntails Gamma phi -> Derives Gamma phi

def mutationChangedBinderScope : Prop :=
  forall (Atom : Type u) (phi : Formula Atom),
    (forall Gamma : Set (Formula Atom), SemanticallyEntails Gamma phi) ->
      forall Gamma : Set (Formula Atom), Derives Gamma phi

def mutationFiniteContexts : Prop :=
  forall (Atom : Type u) (Gamma : List (Formula Atom)) (phi : Formula Atom),
    (forall valuation : Atom -> Bool,
      (forall psi, psi ∈ Gamma -> Formula.eval valuation psi = true) ->
        Formula.eval valuation phi = true) ->
      Derives {psi | psi ∈ Gamma} phi

/-- Empty premises do not semantically entail an arbitrary atom. -/
theorem empty_context_atom_boundary (a : Unit) :
    ¬ SemanticallyEntails (Atom := Unit) ({} : Set (Formula Unit)) (.atom a) := by
  intro h
  have := h (fun _ => false) (by simp [Satisfies])
  simp [Formula.eval] at this

/-- A context containing false has no satisfying Boolean valuation. -/
theorem falsum_context_boundary (Atom : Type u) (phi : Formula Atom) :
    SemanticallyEntails ({.falsum} : Set (Formula Atom)) phi := by
  intro valuation h
  have hf := h .falsum rfl
  simp [Formula.eval] at hf

/-- Premises are available as derivation leaves, including at the empty atom type. -/
theorem assumption_boundary (phi : Formula Empty) : Derives ({phi} : Set (Formula Empty)) phi := by
  exact .assumption rfl

end Stage1Instances.THM_M_0696

set_option pp.explicit true in
#print Stage1Instances.THM_M_0696.PropositionalCompletenessTarget
