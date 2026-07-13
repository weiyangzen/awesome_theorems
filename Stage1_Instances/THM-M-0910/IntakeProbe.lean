import Mathlib.ModelTheory.Graph
import Mathlib.Computability.DFA
import Mathlib.Computability.Halting

/-!
# THM-M-0910 discovery-only intake probe

These checks authenticate adjacent pinned first-order graph/model-theory, regular-language, finite-
automata, and computability interfaces. They do not encode monadic second-order set quantification,
define Caucal's graph classes or transformations, select the source statement, establish a source
transport, or prove any Caucal decidability result.
-/

#check FirstOrder.Language.graph
#check SimpleGraph.structure
#check FirstOrder.Language.Theory.simpleGraph
#check FirstOrder.Language.Sentence
#check FirstOrder.Language.Formula.Realize
#check FirstOrder.Language.completeTheory
#check Language
#check DFA
#check DFA.accepts
#check Language.IsRegular
#check ComputablePred
