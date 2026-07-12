# THM-M-0653 frozen obligation architecture

Item `S56-M-0653-OBLIGATION_TREE` freezes registry version 1 against the exact
`Statement.lean` and `anchor-audit.json` hashes recorded in
`obligation-registry.json`. The 14-ID inventory is the denominator for later
machine, human-source, and readable coverage. Changing an ID, eligibility, or
decomposition requires a versioned delta; later proof discovery cannot silently
shrink this denominator.

## Proof architecture

The exact root is assembled from an elementary explicit-to-implicit direction
and the nontrivial Beth direction. The Beth branch uses the conventional
two-copy architecture: build two renamed relation copies, turn implicit
uniqueness into inconsistency of a disagreement theory, extract finite
fragments by compactness, apply Craig interpolation, prove the vocabulary and
free-variable restriction, and transport the interpolant back to an
`L.Formula (Fin n)` realized in reducts. Each semantic bridge remains a
separate obligation even when its eventual Lean proof is a short invocation.

The proof graph records reciprocal `proof_requires` and `composes` edges.
Separate refinement, provenance, evidence, trust, documentation, and workflow
graphs prevent source citations or workflow receipts from being counted as
proof edges. Every node has a semantic ledger and a budget of at most 100
steps.

## Boundary

Only the statement interface and the identity root boundary in
`ObligationTree.lean` have scoped elaboration evidence. The directional
interfaces and every substantive Beth bridge are planned, not proved.
`root_of_directions` consumes the exact root itself and returns it unchanged;
it tests the canonical output type but supplies no composition or theorem
credit. The root stays `M3`, the theorem is incomplete, primary-source mapping
is open, and there is no accepted receipt.

The current first open cut contains the explicit-to-implicit direction, the
two-copy construction, the implicit-uniqueness inconsistency reduction, the
primary-source map, and the foundation audit. The downstream proof phase must
implement typed directional interfaces before it can claim checked child-to-
parent composition.
