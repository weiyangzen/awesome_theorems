import Mathlib.Computability.EpsilonNFA
import Mathlib.Computability.MyhillNerode
import Mathlib.Computability.RegularExpressions

/-!
Discovery-only intake probe for `THM-M-0759`.

The repository record names finite automata theory but does not select a proposition.  These
checks authenticate nearby APIs in the pinned environment; they do not state or prove the target.
-/

#check Language
#check DFA
#check DFA.eval
#check DFA.accepts
#check DFA.pumping_lemma
#check Language.IsRegular
#check Language.IsRegular_compl
#check Language.IsRegular.add
#check Language.IsRegular.inf
#check NFA
#check NFA.toDFA_correct
#check DFA.toNFA_correct
#check εNFA
#check εNFA.toNFA_correct
#check NFA.toεNFA_correct
#check RegularExpression
#check RegularExpression.matches'
#check RegularExpression.rmatch_iff_matches'
#check Language.leftQuotient
#check Language.isRegular_iff_finite_range_leftQuotient
