# Exact-statement gate: blocked

Item: `S56-M-0604-STATEMENT`  
Theorem: `THM-M-0604`  
Base revision: `162f31e26f99fc08e308d576b8fb1b6f18a338c6`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
The complete record is the title "bordism ring structure" and the gloss "algebraic structure of
the bordism ring". It supplies no exact source theorem or page and, as the accepted intake records,
does not select unoriented, oriented, framed, spin, or another tangential bordism theory.

Those alternatives are not interchangeable. They change the equivalence classes, additive inverse,
coefficient ring, and whether factor exchange is ordinary or signed graded commutativity. The record
also leaves open the representative model, boundary and corner convention, direct-sum or bundled
grading, and the precise zero and unit. Choosing any of these solely to obtain a Lean proposition
would narrow or substitute the received claim. An abstract type already carrying a graded-ring
instance would merely assume the requested structure and is therefore not an admissible encoding.

The first failed gate is exact source-statement identity. Consequently there is no canonical Lean
expression, honest minimal-import claim for that expression, checked alternate transport, expression
fingerprint, or meaningful removed-hypothesis, changed-domain, binder-scope, and boundary mutation
suite. Machine state remains `M4`; no statement or theorem-completion credit is claimed.

## Pinned Lean boundary checked

`StatementProbe.lean` uses the sole direct import `Mathlib.Geometry.Manifold.Bordism`. In pinned
mathlib it elaborates `SingularManifold` and the representative-level operations `empty`, `toPUnit`,
`sum`, and `prod`. This is real candidate-surface validation only.

The imported module describes itself as the beginnings of unoriented bordism theory and explicitly
lists as future work the bordism relation, proof that it is an equivalence relation, the quotient
bordism groups, and multiplication with the bordism-ring laws. Thus the pinned API cannot currently
express the geometric quotient-ring claim without introducing new formalization or circularly
postulating the missing structure. The precursor operations receive neither exact-statement nor
proof credit.

## Retry condition

An accountable source review must preserve an immutable primary source and select an exact numbered
theorem or definition-plus-laws, including the tangential structure, representative category,
boundary/corner rules, grading, commutativity signs, identities, and degenerate cases. A later run
must then implement or pin the matching bordism relation and quotient vocabulary, elaborate the
literal target with minimized imports, check any alternate encoding transport, and execute all
required statement mutations.

The assigned phase is not genuinely self-tested to completion, so
`.stage1-worker-selftest.json` is intentionally absent.
