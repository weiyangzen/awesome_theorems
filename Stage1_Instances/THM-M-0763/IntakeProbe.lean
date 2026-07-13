import Mathlib.Computability.ContextFreeGrammar
import Mathlib.Computability.DFA
import Mathlib.Computability.Halting

/-!
# THM-M-0763 discovery-only intake probe

These checks authenticate pinned formal-language, regular-language, context-free-grammar, and
recursive-enumerability interfaces near possible Chomsky-hierarchy encodings. They do not select a
hierarchy variant, state the catalog root, or prove THM-M-0763.
-/

#check Language
#check Language.IsRegular
#check ContextFreeRule
#check ContextFreeGrammar
#check ContextFreeGrammar.language
#check ContextFreeGrammar.mem_language_iff
#check Language.IsContextFree
#check ComputablePred
#check REPred
