# THM-M-1082 obligation tree

This registry freezes the constructor/projection architecture. Checked interfaces remain provisional and no theorem-completion claim follows.

## M1082-ROOT

The exact finite-dimensional-law characterization of a Gaussian process.

Formal target: `ProbabilityTheory.IsGaussianProcess X P <-> forall I : Finset T, ProbabilityTheory.HasGaussianLaw (fun omega => I.restrict (X . omega)) P`

Output: The frozen canonical proposition.

Semantic ledger:

1. Premises: Only the exact context and incoming proof_requires conclusions.
2. Inference: The exact finite-dimensional-law characterization of a Gaussian process.
3. Output: The frozen canonical proposition.
4. Outgoing use: Only the declared typed edge may consume this output.

Boundary: Architecture or checked conditional interface only; no master acceptance, H0, release, or theorem completion.

## M1082-S-CONTEXT

Freeze universes, measurable spaces, topology, additive monoid, real module, process, and measure in their exact binder order.

Formal target: `Statement.lean binder context`

Output: The exact context shared by both directions.

Semantic ledger:

1. Premises: Only the exact context and incoming proof_requires conclusions.
2. Inference: Freeze universes, measurable spaces, topology, additive monoid, real module, process, and measure in their exact binder order.
3. Output: The exact context shared by both directions.
4. Outgoing use: Only the declared typed edge may consume this output.

Boundary: Architecture or checked conditional interface only; no master acceptance, H0, release, or theorem completion.

## M1082-S-BOUNDARY

Retain the empty Finset and allow degenerate, noncentered Gaussian laws; add no continuity, covariance, or independence premise.

Formal target: `forall I : Finset T (including empty), HasGaussianLaw ...`

Output: The statement boundary with no strengthened or weakened side condition.

Semantic ledger:

1. Premises: Only the exact context and incoming proof_requires conclusions.
2. Inference: Retain the empty Finset and allow degenerate, noncentered Gaussian laws; add no continuity, covariance, or independence premise.
3. Output: The statement boundary with no strengthened or weakened side condition.
4. Outgoing use: Only the declared typed edge may consume this output.

Boundary: Architecture or checked conditional interface only; no master acceptance, H0, release, or theorem completion.

## M1082-S-FOUNDATION

Bind the proof to Lean 4.29.0, pinned mathlib, and the audited classical quotient/extensionality trust profile.

Formal target: `foundation/trust certificate for the imported definition and local composition`

Output: The trust boundary required by later validation.

Semantic ledger:

1. Premises: Only the exact context and incoming proof_requires conclusions.
2. Inference: Bind the proof to Lean 4.29.0, pinned mathlib, and the audited classical quotient/extensionality trust profile.
3. Output: The trust boundary required by later validation.
4. Outgoing use: Only the declared typed edge may consume this output.

Boundary: Architecture or checked conditional interface only; no master acceptance, H0, release, or theorem completion.

## M1082-X-DEFINITION

Audit the imported IsGaussianProcess structure as exactly one field with the frozen finite-dimensional type.

Formal target: `ProbabilityTheory.IsGaussianProcess and .hasGaussianLaw`

Output: A pinned exact-definition interface, not a theorem-name analogy.

Semantic ledger:

1. Premises: Only the exact context and incoming proof_requires conclusions.
2. Inference: Audit the imported IsGaussianProcess structure as exactly one field with the frozen finite-dimensional type.
3. Output: A pinned exact-definition interface, not a theorem-name analogy.
4. Outgoing use: Only the declared typed edge may consume this output.

Boundary: Architecture or checked conditional interface only; no master acceptance, H0, release, or theorem completion.

## M1082-T-FORWARD

Project the finite-dimensional Gaussian-law family from an IsGaussianProcess witness.

Formal target: `ObligationTree.forward_from_projection`

Output: The forward implication at the exact context.

Semantic ledger:

1. Premises: Only the exact context and incoming proof_requires conclusions.
2. Inference: Project the finite-dimensional Gaussian-law family from an IsGaussianProcess witness.
3. Output: The forward implication at the exact context.
4. Outgoing use: Only the declared typed edge may consume this output.

Boundary: Architecture or checked conditional interface only; no master acceptance, H0, release, or theorem completion.

## M1082-T-REVERSE

Construct an IsGaussianProcess witness from the complete finite-dimensional Gaussian-law family.

Formal target: `ObligationTree.reverse_from_constructor`

Output: The reverse implication at the exact context.

Semantic ledger:

1. Premises: Only the exact context and incoming proof_requires conclusions.
2. Inference: Construct an IsGaussianProcess witness from the complete finite-dimensional Gaussian-law family.
3. Output: The reverse implication at the exact context.
4. Outgoing use: Only the declared typed edge may consume this output.

Boundary: Architecture or checked conditional interface only; no master acceptance, H0, release, or theorem completion.

## M1082-T-COMPOSE

Consume both directional conclusions and form the exact iff without an undeclared premise.

Formal target: `ObligationTree.root_of_directions`

Output: The exact root conditional on both registered directions.

Semantic ledger:

1. Premises: Only the exact context and incoming proof_requires conclusions.
2. Inference: Consume both directional conclusions and form the exact iff without an undeclared premise.
3. Output: The exact root conditional on both registered directions.
4. Outgoing use: Only the declared typed edge may consume this output.

Boundary: Architecture or checked conditional interface only; no master acceptance, H0, release, or theorem completion.

## M1082-X-SOURCE

Map the characterization and boundary conventions to pinpoint human sources.

Formal target: `node-specific human-source crosswalk`

Output: Human-source coverage only; no machine proof credit.

Semantic ledger:

1. Premises: Only the exact context and incoming proof_requires conclusions.
2. Inference: Map the characterization and boundary conventions to pinpoint human sources.
3. Output: Human-source coverage only; no machine proof credit.
4. Outgoing use: Only the declared typed edge may consume this output.

Boundary: Architecture or checked conditional interface only; no master acceptance, H0, release, or theorem completion.

## M1082-X-PROVENANCE

Record imported definition, local bodies, axioms, toolchain, and replay evidence.

Formal target: `terminal proof-body and transitive provenance record`

Output: Release provenance only; no mathematical proof credit.

Semantic ledger:

1. Premises: Only the exact context and incoming proof_requires conclusions.
2. Inference: Record imported definition, local bodies, axioms, toolchain, and replay evidence.
3. Output: Release provenance only; no mathematical proof credit.
4. Outgoing use: Only the declared typed edge may consume this output.

Boundary: Architecture or checked conditional interface only; no master acceptance, H0, release, or theorem completion.
