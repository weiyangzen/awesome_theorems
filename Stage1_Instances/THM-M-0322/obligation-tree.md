# THM-M-0322 frozen obligation architecture

Item `S56-M-0322-OBLIGATION_TREE` freezes registry version 1 against the exact
`Statement.lean` and `anchor-audit.json` content hashes. The 19 obligation IDs
are the denominator for later machine, human-source, and readable coverage.
Later discovery cannot shrink the denominator; any correction, split, merge,
or eligibility change requires a versioned append-only delta.

## Proof route

The exact equality is assembled from two inclusions. The forward inclusion is
checked locally by convex-hull minimality and compact closedness. For the
reverse inclusion, assume an outside point, strictly separate it from the
closed convex hull, maximize the separating functional on the compact set,
and form the exposed maximizing face. The extreme-point lemma supplies an
extreme point of that face; face extremality transfers it to an extreme point
of the original set, contradicting strict separation.

The extreme-point lemma is not treated as a one-line primitive. Its obligations
record Zorn minimality for nonempty closed extreme subsets, the nonsingleton
branch, point-to-point geometric Hahn-Banach separation, and construction of a
proper exposed face contradicting minimality. Both geometric Hahn-Banach calls
remain explicit bridge boundaries. Every semantic node has a ledger and a
step budget no greater than 100.

The proof graph uses reciprocal `proof_requires` and `composes` edges. Separate
refinement, provenance, evidence, trust, documentation, and workflow graphs
prevent a citation, wrapper, or receipt from acquiring proof credit.

## Status boundary

`ObligationTree.lean` checks the easy inclusion, exact two-inclusion
composition, and a conditional exact-root harness. The reverse inclusion is an
explicit premise in that harness. Although the anchor audit identifies a pinned
mathlib proof of the whole theorem, this phase does not award it node closure:
complete transitive provenance, trust, source mapping, validation, and master
acceptance remain later gates. The root stays `M3`; `H2` and `R4` remain; no
accepted receipt, audit completion, or theorem completion is claimed.
