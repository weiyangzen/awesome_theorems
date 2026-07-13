import Mathlib.Computability.DFA
import Mathlib.Computability.ContextFreeGrammar

/-!
Discovery-only checks for pinned language, regular-automaton, and context-free-grammar interfaces.
No declaration below freezes or proves the source-identical two-component target.
-/

open Computability

#check Language
#check Language.mul_def
#check Language.kstar_def
#check DFA
#check DFA.accepts
#check DFA.evalFrom_split
#check DFA.pumping_lemma
#check Language.IsRegular
#check ContextFreeRule
#check ContextFreeGrammar
#check ContextFreeGrammar.Derives
#check ContextFreeGrammar.language
#check ContextFreeGrammar.mem_language_iff
#check Language.IsContextFree

-- Prospective branch container only, not the canonical target or a proof-bearing declaration.
#check (fun (regularBranch contextFreeBranch : Prop) => regularBranch ∧ contextFreeBranch)
