# Proof outline — S5-CLM-00003625

## N-SOURCE — frozen mathematical source

Hypotheses: the exact source module, revision, file digest, declaration digest,
and declaration-type digest are fixed by the workset.  Inference: resolve the
qualified provider declaration in that environment.  Output: the eventual
claim that `carmichaelCounting x` is larger than `x^(2/7)` for sufficiently
large real `x`.  Formal anchor: `Erdos1057.erdos_1057.variants.agp_lower_bound`.
Downstream uses: semantic binding and the machine root.  Exceptional cases:
no substituted import or unqualified local symbol is admitted.  Trust
boundary: provider bytes are statement authority while dependency closure is
independently audited.

## N-SEMANTIC — exact proposition binding

Hypotheses: the pinned source declaration and the fully qualified target
header.  Inference: elaborate both headers in the same imported environment
and compare their root expressions.  Output: a single expression digest and a
transitive semantic-constant census.  Formal anchor: `Statement.target_statement`.
Downstream uses: both transports.  Exceptional cases: local shadowing,
notation, macros, aliases, coercions, and import substitution are rejected.
Trust boundary: the Lean elaborator and kernel run at trust zero, followed by
Master recomputation.

## N-FORWARD — source-to-target transport

Hypotheses: a proof of the elaborated source proposition.  Inference: because
the source and target expressions are identical, pass that proof unchanged.
Output: a proof of the target proposition.  Formal anchor:
`Statement.source_to_target`.  Downstream uses: exact root composition.
Exceptional cases: no rewriting or semantic conversion is hidden.  Trust
boundary: the identity function is kernel checked.

## N-REVERSE — target-to-source transport

Hypotheses: a proof of the elaborated target proposition.  Inference: apply
the inverse identity transport.  Output: a proof of the source proposition.
Formal anchor: `Statement.target_to_source`.  Downstream uses: semantic audit.
Exceptional cases: the reverse direction is separately declared rather than
inferred from prose.  Trust boundary: the identity function is kernel checked.

## N-ROOT — exact machine root

Hypotheses: the pinned provider declaration in the bound semantic environment
and the forward transport.  Inference: instantiate the forward transport at
the provider proof.  Output: the unconditional target lower bound.  Formal
anchor: `Proof.agp_lower_bound_machine_closure`.  Downstream uses: validation
and release.  Exceptional cases: no extra assumptions, weaker conclusion, or
alternate exponent is permitted.  Trust boundary: trust-zero kernel replay
plus the transitive dependency and axiom audit.

## N-AUDIT — replay and adversarial validation

Hypotheses: both transports, the exact root, all content-addressed anchors,
and the frozen validation command.  Inference: perform cold replay and reject
semantic substitutions or deletion of any readable field.  Output: empty
human, machine, and readability cut sets and a current validation trace.
Formal anchor: `Audit.semantic_identity_audit`.  Downstream uses: provisional
release and independent Master validation.  Exceptional cases: stale object
files and shadowed symbols fail closed.  Trust boundary: the worker may only
propose; the canonical Master alone accepts and advances state.
