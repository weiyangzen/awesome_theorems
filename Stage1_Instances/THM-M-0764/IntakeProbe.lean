import Mathlib.Computability.ContextFreeGrammar
import Mathlib.Computability.TuringMachine.StackTuringMachine

/-!
# THM-M-0764 discovery-only intake probe

These checks authenticate pinned formal-language, context-free-grammar, and general stack-machine
interfaces. They do not define a source-matched pushdown automaton, select an acceptance convention,
state a CFG/PDA equivalence, or prove THM-M-0764.
-/

#check Language
#check ContextFreeRule
#check ContextFreeGrammar
#check ContextFreeGrammar.Produces
#check ContextFreeGrammar.Derives
#check ContextFreeGrammar.Generates
#check ContextFreeGrammar.language
#check ContextFreeGrammar.mem_language_iff
#check Language.IsContextFree
#check Language.IsContextFree.reverse

-- Adjacent deterministic multi-stack machine substrate, not a standard NPDA target.
#check Turing.TM2.Stmt
#check Turing.TM2.Cfg
#check Turing.TM2.step
#check Turing.TM2.Reaches
#check Turing.TM2.init
#check Turing.TM2.eval
