# Machine-checked audit — S5-CLM-00003567

The proposed root is classified `M0-L`: the target owns the proof surface, imports only `Mathlib`, contains no placeholder, unsafe declaration, opaque declaration, target-specific axiom, local semantic definition, notation, macro, coercion, instance, or namespace alias, and reports an empty observed-axiom set.

The source theorem and its upper-bound variant are not proof dependencies. Their exact module and qualified declaration survive only as frozen provenance strings. The structured declaration census and dependency edges live in `machine-closure.json`; prose does not duplicate them.

This worker has run only the required semantic/evidence preflight. The canonical Master must cold-build each Lean file offline at trust zero, recompute every type/body/dependency/axiom hash, compare the unconditional root expression with the frozen source expression, and rerun semantic-substitution mutations before acceptance.
