# Machine-checked audit

The machine root is `boxdotConjecture_audit_root`, with local closure level
`M0-L`. Its body introduces an arbitrary formula/member proof, applies
translation closure, and eliminates the forward direction of faithfulness.
The companion declarations split those two proof edges and prove both
directions of the set/elementwise transport.

Worker checks reject `sorry`, `admit`, axioms, unsafe declarations, opaque
oracles, local semantic definitions, aliases, parser substitutions, and
source-symbol shadowing. The observed claim-owned axiom census is empty and the
machine cut set is empty. The pinned source theorem's `sorryAx` is explicitly
outside the proof closure.

Because this generation is forbidden to invoke Lean/Lake/Elan, cold offline
trust-zero compilation, exact elaborated-expression equality, object read
traces, and semantic-substitution mutations are mandatory canonical-Master
recomputations. The worker evidence records that boundary rather than claiming
that a text hash is kernel evidence.
