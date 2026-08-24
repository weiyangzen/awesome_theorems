# Proof outline — S5-CLM-00003506

## A-root — exact logical root

For the complete source right-hand side `P`, the answer-marked proposition
`False ↔ P` is equivalent to the ordinary negative claim `¬ P`. The two
directions below account for every connective in this normalization.

## A-forward — source to target

Assume `h : False ↔ P` and `hP : P`. The reverse implication `h.mpr` sends
`hP` to `False`; hence `P` is impossible and `¬ P` follows. This fragment uses
both hypotheses, produces the target negation, and is consumed by `A-root`.

## A-reverse — target to source

Assume `h : ¬ P`. To construct `False ↔ P`, map a false premise to `P` by
false elimination, and map `hP : P` back to `False` with `h`. This fragment
produces the source answer surface and is consumed by `A-root`.

## A-composition — bidirectional closure

Pair `A-forward` and `A-reverse` with biconditional introduction. The output
is exactly `(False ↔ P) ↔ ¬ P`. The provider declaration is used only to bind
the meaning of the parameter `P`; its proof body contributes no inference.
