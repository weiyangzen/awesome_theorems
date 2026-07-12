# THM-M-0669 frozen obligation architecture

Item `S56-M-0669-OBLIGATION_TREE` freezes registry version 1 against the exact
`Statement.lean` and `anchor-audit.json` hashes recorded in
`obligation-registry.json`. The 14-ID inventory is the denominator for later
machine, human-source, and readable coverage. Any ID, eligibility, or
decomposition change requires a versioned delta; later proof discovery cannot
silently shrink the denominator.

## Proof architecture

The selected architecture separates logical recursion from the algebraic core.
Atomic formulas are normalized to polynomial conditions, Boolean closure is
proved independently, and the main bridge eliminates one existential variable
from an arbitrary quantifier-free formula. That bridge reduces to finite sign
conditions, real-closed polynomial root and cell behavior, a parameter-only
projection construction, and a checked transport back to mathlib formula
semantics. Formula induction then eliminates nested quantifiers and preserves
the original free-variable index type.

The proof graph contains reciprocal `proof_requires` and `composes` edges.
Refinement, provenance, evidence, trust, documentation, and workflow graphs are
separate so that citations and receipts cannot be mistaken for proof edges.
Every semantic node has a substantive ledger and a step budget no greater than
100. The polynomial and semantic bridges remain distinct even if a future proof
invokes a deep library theorem in one line.

## Boundary

Only the statement/theory interface and the identity root boundary in
`ObligationTree.lean` have scoped elaboration evidence. `root_of_elimination`
assumes the exact root and returns it unchanged; it checks the output type but
supplies no proof or composition credit. All substantive algebraic elimination
and formula-recursion nodes remain open. The root stays `M3`, primary-source
mapping and foundation audit remain open, and the theorem is incomplete.

The first open cut is atomic normalization, Boolean closure, one-variable
elimination, primary-source mapping, and foundation audit. The proof phase must
replace planned interfaces with exact Lean declarations and demonstrate checked
child-to-parent composition before any root closure can be claimed.
