# Machine-checked audit boundary

The three Lean artifacts contain no placeholder, axiom, unsafe declaration,
opaque oracle, local semantic definition, notation, macro, coercion, namespace
alias, or active provider import.  They use only theorem declarations over
`Mathlib`, with `ring` and `norm_num` certificates.

The worker is expressly restricted to `--no-lean`, so “machine closure” in the
worker handoff means a complete, content-addressed replay prescription and a
candidate declaration graph.  It is not a claim that the worker ran Lean.  The
canonical Master must independently perform cold from-source trust-zero
compilation, inspect declaration types/bodies/dependencies/axioms, recompute the
source and target elaborated expressions, and run semantic-substitution
mutations before acceptance.

The source `sorryAx` is excluded from proof closure: the provider theorem is
referenced only in a provenance comment and no source proof body is consumed.
