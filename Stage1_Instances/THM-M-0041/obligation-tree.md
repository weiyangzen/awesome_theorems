# THM-M-0041 obligation tree

Item: `S56-M-0041-OBLIGATION_TREE`

Registry v1 freezes 17 canonical obligations before any accepted closure credit. Its exact root is
the statement-gate proposition over every commutative ring and every finite decidable square index
type, including empty dimensions and the zero ring. The pinned candidate is
`Matrix.aeval_self_charpoly`; its wrapper, the LinearMap formulation, and downstream uses share one
terminal body identity rather than receiving duplicate coverage.

## Proof route

The machine proof spine requires both the determinant-to-`Matrix.charpoly` transport and the exact
matrix Cayley-Hamilton anchor. The central imported body is not treated as a one-line leaf. It is
expanded into the adjugate construction, `matPolyEquiv` representation normalization, evaluation of
the right factor `X - C A`, scalar/evaluation conversion, and checked recomposition. Support edges
for source, provenance, trust, documentation, and workflow remain separate from proof closure.

### m0041-root

`M0041-ROOT` is `Stage1Instances.THM_M_0041.CayleyHamiltonTarget`. It remains `H1/M3/R3` and open.

### m0041-s-interface

`M0041-S-INTERFACE` freezes universes, ordered binders, typeclasses, matrix algebra evaluation, and
the zero-matrix conclusion.

### m0041-s-charpoly

`M0041-S-CHARPOLY` freezes `det (X I - A.map C)` as the canonical characteristic polynomial.

### m0041-s-boundary

`M0041-S-BOUNDARY` retains empty index types and zero rings. No stronger field, nontriviality,
nonemptiness, invertibility, or diagonalizability premise may enter the proof.

### m0041-s-foundation

`M0041-S-FOUNDATION` owns the proof-specific foundation and TCB audit. The provisional candidate
reports `propext`, `Classical.choice`, and `Quot.sound`; transitive acceptance remains downstream.

### m0041-t-charpoly

`M0041-T-CHARPOLY` requires the exact definitional equality between the expanded local definition
and `Matrix.charpoly`. `ObligationTree.lean` freezes its conditional interface.

### m0041-a-mathlib-anchor

`M0041-A-MATHLIB-ANCHOR` is the exact universal matrix statement ending at the single terminal body
`Matrix.aeval_self_charpoly` in pinned mathlib. It is a provisional M0-W route, not accepted M0-W.

### m0041-c-adjugate

`M0041-C-ADJUGATE` constructs `adjugate (charmatrix A)` and applies `Matrix.adjugate_mul` to obtain
the characteristic-polynomial scalar identity.

### m0041-n-matpoly

`M0041-N-MATPOLY` crosses from matrices of polynomials to polynomials of matrices with
`matPolyEquiv`, normalizing `charmatrix A` to `X - C A`.

### m0041-l-right-factor

`M0041-L-RIGHT-FACTOR` evaluates at `A` and uses `Polynomial.eval_mul_X_sub_C`. This is substantive:
polynomial evaluation into a noncommutative matrix ring is not generally multiplicative.

### m0041-t-scalar-eval

`M0041-T-SCALAR-EVAL` uses `matPolyEquiv_smul_one` and `Polynomial.eval_map` to recover
`Polynomial.aeval A A.charpoly = 0`.

### m0041-t-body-assemble

`M0041-T-BODY-ASSEMBLE` conditionally consumes all four internal engines. The checked declaration
does not prove those premises and therefore supplies no accepted body or root closure.

### m0041-x-source

`M0041-X-SOURCE` keeps the primary-source theorem, proof, assumptions, definitions, attribution,
errata, and node mapping open for independent review.

### m0041-x-provenance

`M0041-X-PROVENANCE` must close wrapper-to-terminal-body identity, transitive declarations, source
blobs, revisions, imports, and licenses without alias multiplication.

### m0041-x-trust

`M0041-X-TRUST` owns the exact terminal object's transitive axiom, compiled-artifact, executable,
unsafe/oracle, supply-chain, and replay boundary.

### m0041-x-readable

`M0041-X-READABLE` requires an independently reviewed node-by-node reconstruction. This page is a
phase-boundary architecture record, not R0.

### m0041-x-workflow

`M0041-X-WORKFLOW` binds proof, validation, review, freshness, revocation, independent verification,
and release acceptance. A worker self-test cannot close it.

## Boundary

The obligation phase freezes scope, denominators, typed edges, and conditional composition only.
No obligation is accepted closed. H0/R0, release-grade E1, full provenance and trust, hermetic and
independent validation, `AUDIT-Z`, and theorem completion remain open.
