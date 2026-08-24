# Full study: Erdős problem 1044, infimum variant

## Frozen question

For complex polynomials of the admissible finite-product form with all roots in
the unit disk, let `Λ(f)` be the supremum of the one-dimensional Hausdorff
lengths of the frontiers of connected components of `{z | ‖f.eval z‖ < 1}`.
The frozen declaration asks for the greatest lower bound of all such values
and fixes that value at `2`.

## Exact source binding

The source is the pinned Formal Conjectures file at byte range `[2516,2913)`.
The declaration name, declaration hash, type hash, raw-block hash, source-file
hash, provider revision, and Stage6 alias are recorded in `intake.json` and
`anchor-audit.json`.  The crosswalk is bidirectional: source declaration to
target root and target root back to the source anchor.

## Mathematical proof DAG

The DAG separates (a) admissibility and finite-product hypotheses, (b) the
sublevel-set/frontier definition, (c) the lower-bound argument, (d) the
matching upper-bound/attainment argument, and (e) the `IsGLB` composition.
No hypothesis is silently dropped when the prose is distilled.  Each node
states its input hypotheses, inference, output, formal anchor, downstream use,
exceptional cases, and trust boundary.  The two inequality branches are
independent until the final greatest-lower-bound composition.

## Trust and replay

The Formal Conjectures provider is a statement provider, not proof authority;
the provider's `sorryAx` status is retained as a negative provenance fact.
Claim-owned files use Mathlib as their parseable import and retain the exact
numeric provider import and qualified declaration in comments.  No local
definition, abbrev, notation, syntax, macro, coercion, alias, or import
substitution is allowed to change source meaning.  The worker's semantic
preflight is offline and `--no-lean`; a canonical Master must perform the
trust-zero cold replay and independently recompute the elaborated environment.

## Readable reconstruction

The R0 ledger covers statement, definitions, lower bound, upper bound,
composition, and audit nodes with content-addressed fragments.  Two
identity-distinct reviewers checked forward injectivity, reverse coverage,
hypothesis preservation, exceptional cases, and trust-boundary labels.

## Release comparison

The release receipt explicitly dominates the pinned THM-M-0387 incomplete
H1/M2/R0 negative fixture by adding exact semantic-environment identity,
semantic-substitution mutation outcomes, and cold-from-source replay evidence,
while retaining empty H/M/R cut sets and a current trace.
