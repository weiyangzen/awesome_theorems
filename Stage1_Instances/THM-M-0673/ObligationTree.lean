import Statement
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0673 conditional obligation composition

This module checks the exact interfaces on the imported Los theorem route. The
bounded-formula package remains an explicit premise: this file neither invokes
the audited mathlib theorem nor installs a proof of the canonical root.
-/

set_option autoImplicit false

namespace Stage1Instances.THM_M_0673_Obligations

open Filter FirstOrder
open Stage1Instances.THM_M_0673

universe u v w x y

/-- The substantive bounded-formula induction exported by the pinned body. -/
def BoundedFormulaRealizePackage : Prop :=
  forall (I : Type u) (M : I -> Type v) (U : Ultrafilter I)
    (L : Language.{w, x}) [forall i, L.Structure (M i)] [forall i, Nonempty (M i)]
    {beta : Type y} {n : Nat} (phi : L.BoundedFormula beta n)
    (assign : beta -> forall i, M i) (bound : Fin n -> forall i, M i),
      phi.Realize (fun i => (assign i : (U : Filter I).Product M))
          (fun i => (bound i : (U : Filter I).Product M)) <->
        ∀ᶠ i : I in U,
          phi.Realize (fun j => assign j i) (fun j => bound j i)

/-- The formula interface obtained by specializing the bounded-formula route. -/
def FormulaRealizePackage : Prop :=
  forall (I : Type u) (M : I -> Type v) (U : Ultrafilter I)
    (L : Language.{w, x}) [forall i, L.Structure (M i)] [forall i, Nonempty (M i)]
    {beta : Type y} (phi : L.Formula beta) (assign : beta -> forall i, M i),
      phi.Realize (fun i => (assign i : (U : Filter I).Product M)) <->
        ∀ᶠ i : I in U, phi.Realize (fun j => assign j i)

/-- The exact sentence-level terminal interface used by the canonical target. -/
def SentenceRealizePackage : Prop :=
  forall (I : Type u) (M : I -> Type v) (U : Ultrafilter I)
    (L : Language.{w, x}) [forall i, L.Structure (M i)] [forall i, Nonempty (M i)]
    (phi : L.Sentence),
      (U : Filter I).Product M ⊨ phi ↔
        ∀ᶠ i : I in U, M i ⊨ phi

/-- A distinct terminal interface lets the root consume exactly one child. -/
def TerminalRootPackage : Prop :=
  LosSentenceTarget.{u, v, w, x}

/-- Checked bounded-formula-to-formula composition. The premise is open. -/
theorem formula_of_bounded
    (bounded : BoundedFormulaRealizePackage.{u, v, w, x, y}) :
    FormulaRealizePackage.{u, v, w, x, y} := by
  intro I M U L _ _ beta phi assign
  simp_rw [Language.Formula.Realize, <- bounded I M U L phi assign, iff_eq_eq]
  exact congr rfl (Subsingleton.elim _ _)

/-- Checked formula-to-sentence composition at the empty free-variable type. -/
theorem sentence_of_formula
    (formula : FormulaRealizePackage.{u, v, w, x, 0}) :
    SentenceRealizePackage.{u, v, w, x} := by
  intro I M U L _ _ phi
  simp_rw [Language.Sentence.Realize]
  rw [<- formula I M U L phi, iff_eq_eq]
  exact congr rfl (Subsingleton.elim _ _)

/-- Checked adapter from the sentence package to the distinct terminal root. -/
theorem terminal_of_sentence
    (sentence : SentenceRealizePackage.{u, v, w, x}) :
    TerminalRootPackage.{u, v, w, x} := by
  intro I M U L _ _ phi
  exact sentence I M U L phi

/-- Exact terminal-to-canonical-root identity composition. -/
theorem root_of_terminal
    (terminal : TerminalRootPackage.{u, v, w, x}) :
    LosSentenceTarget.{u, v, w, x} :=
  terminal

/-- Combined conditional route. Its bounded premise is deliberately open. -/
theorem root_of_bounded
    (bounded : BoundedFormulaRealizePackage.{u, v, w, x, 0}) :
    LosSentenceTarget.{u, v, w, x} :=
  root_of_terminal <| terminal_of_sentence <| sentence_of_formula <|
    formula_of_bounded bounded

#check FirstOrder.Language.Ultraproduct.boundedFormula_realize_cast
#check FirstOrder.Language.Ultraproduct.realize_formula_cast
#check FirstOrder.Language.Ultraproduct.sentence_realize
#check BoundedFormulaRealizePackage
#check FormulaRealizePackage
#check SentenceRealizePackage
#check TerminalRootPackage
#check formula_of_bounded
#check sentence_of_formula
#check terminal_of_sentence
#check root_of_terminal
#check root_of_bounded

set_option pp.explicit true in
set_option pp.universes true in
#print BoundedFormulaRealizePackage
set_option pp.explicit true in
set_option pp.universes true in
#print FormulaRealizePackage
set_option pp.explicit true in
set_option pp.universes true in
#print SentenceRealizePackage
set_option pp.explicit true in
set_option pp.universes true in
#print TerminalRootPackage

assert_no_sorry formula_of_bounded
assert_no_sorry sentence_of_formula
assert_no_sorry terminal_of_sentence
assert_no_sorry root_of_terminal
assert_no_sorry root_of_bounded

#print sorries formula_of_bounded sentence_of_formula terminal_of_sentence
  root_of_terminal root_of_bounded
#print axioms formula_of_bounded
#print axioms sentence_of_formula
#print axioms terminal_of_sentence
#print axioms root_of_terminal
#print axioms root_of_bounded

end Stage1Instances.THM_M_0673_Obligations
