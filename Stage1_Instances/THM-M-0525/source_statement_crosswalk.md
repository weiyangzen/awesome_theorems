# Source-statement crosswalk

The repository source says `拓扑空间的道路同伦类群`, literally "the group of path-homotopy
classes of a topological space." A group requires a chosen object: the faithful standard reading
is the homotopy classes, relative to endpoints, of loops at a basepoint. Classes of paths between
varying endpoints instead form a groupoid. This disambiguation narrows the source phrase; it does
not add connectedness or a computation for any particular space.

| Claim component | Human source anchor | Lean candidate at intake | Assessment |
|---|---|---|---|
| Repository claim | `Docs/researches/math_theorems.md`, lines 3897-3902: name, Poincare/1895 attribution, and the quoted phrase | Whole target | Exact repository provenance, but its `已验证` label is untrusted metadata and supplies no proof credit |
| Historical fundamental-group construction | H. Poincare, *Analysis situs*, Journal de l'Ecole Polytechnique (2), cahier 1 (1895), 1-121 | `FundamentalGroup` | Primary historical work identified; exact section/page, terminology correspondence, edition image/hash, and correction history are not audited, so no `H0` claim |
| Based loops modulo endpoint-fixed homotopy | Standard mathematical expansion of the terse source phrase; primary pinpoint remains open | `Path.Homotopic.Quotient x x`; `FundamentalGroup X x` | Candidate carrier alignment; exact definitional unfolding and equivalence are deferred to statement work |
| Multiplication | Concatenation of based loops | category composition / `Path.Homotopic.Quotient.trans` | Direction and representative-independence must be checked from pinned source before credit |
| Identity | Constant loop at the basepoint | category identity / class of `Path.refl x` | Candidate only |
| Inverse | Path reversal | groupoid inverse / quotient of the symmetric path | Candidate only |
| Group laws | Homotopies for associativity, units, and reversal/concatenation | pinned `Groupoid (FundamentalGroupoid X)` instance inducing `Group (FundamentalGroup X x)` | Existing API located, but terminal bodies, axioms, provenance, and composition are not audited at intake |

Pinned Lean discovery surface:

- mathlib commit `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `Mathlib/AlgebraicTopology/FundamentalGroupoid/Basic.lean` defines the path-homotopy quotient
  groupoid and its composition, identity, and inverse.
- `Mathlib/AlgebraicTopology/FundamentalGroupoid/FundamentalGroup.lean` defines
  `FundamentalGroup X x` as `End (FundamentalGroupoid.mk x)` and provides its group instance.

These file and declaration locators are candidate anchors, not an anchor-audit receipt. The source
phase still owes a fixed primary edition, theorem/definition/page pinpoints, assumption mapping,
errata search, and independent review. The statement and anchor-audit phases owe exact Lean types,
normalized expression and environment fingerprints, checked transports, terminal-body provenance,
and transitive trust closure. Current source status is therefore `H1`, not `H0`.
