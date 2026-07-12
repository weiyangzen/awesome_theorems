# Frozen obligation tree

Item: `S56-M-0319-OBLIGATION_TREE`

The version-1 denominator contains 12 root-relevant obligations. It was frozen against the exact
statement and immutable anchor audit before any proof-phase closure decision. The proof route is
the one actually exposed by the audited Lean 4 candidate: reduce a nonempty compact convex set to
the unit cube, prove the cube fixed-point lemma, assemble the general subtype theorem, then apply
the checked subtype-to-ambient adapter.

| ID | Role | Current boundary |
|---|---|---|
| `M0319-ROOT` | exact canonical proposition | `M3`, open |
| `M0319-S-DEFINITIONS` | exact encodings | locally elaborated |
| `M0319-S-BOUNDARY` | dimension zero and degenerate cases | dimension zero locally checked |
| `M0319-S-FOUNDATION` | axioms, imports, TCB, no-oracle policy | open |
| `M0319-T-SUBTYPE` | subtype-to-ambient composition | conditional adapter locally checked |
| `M0319-N-FINITE-DIM` | Euclidean finite-dimensional instance | locally elaborated |
| `M0319-R-CONVEX-CUBE` | compact-convex cube reduction | external body only; local proof open |
| `M0319-L-UNIT-CUBE` | unit-cube fixed point | external body only; local proof open |
| `M0319-T-EXTERNAL` | exact audited general theorem body | `E3/M3`, dependency closure absent |
| `M0319-X-INTEGRATION` | immutable import and kernel receipt | open |
| `M0319-X-SOURCE` | primary-source node map | open |
| `M0319-X-PROVENANCE` | terminal bodies and replay provenance | open informational overlay |

The proof graph has reciprocal `proof_requires` and `composes` edges. Separate refinement,
provenance, evidence, trust, documentation, and workflow graphs prevent source or workflow facts
from being counted as proof closure. Every node has a semantic ledger and a budget of 40 steps,
below the rev-5.6 split threshold of 100.

The minimal observed open root cut is `M0319-T-EXTERNAL`: supplying that exact proposition to the
locally checked adapter closes the formal root, but the immutable external body cannot be credited
until it is in an approved pinned dependency closure with kernel, axiom, and provenance receipts.
This architecture freeze proves neither Brouwer's theorem nor theorem completion.
