# THM-M-0107 frozen obligation architecture

## Freeze boundary

Registry version 1 freezes 29 canonical obligations for `S56-M-0107-OBLIGATION_TREE`.
Twenty-five are root-relevant machine and human-source obligations; four `X*` records are typed
provenance or trust overlays. All 29 require readable coverage. Eligibility follows the exact
statement and finite-envelope architecture, not the availability of a convenient library theorem.
The ordered denominator and canonical digest in `obligation-registry.json` are authoritative.

The root fingerprint is inherited from `statement.json`. Other signatures are explicitly planned
and remain `M3` interfaces until later proof work elaborates their exact targets. Any split, merge,
exclusion, or eligibility change requires a new registry version and append-only delta.

## Typed proof route

```text
M0107-ROOT  exact existential Zariski factorization [open M3]
|-- M0107-S  exact definitions, context, boundary, transport, and foundation policy
|-- M0107-N  canonical relative normalization, maps, and reduction
|-- M0107-B  affine-local finiteness, overlap compatibility, global recomposition
|-- M0107-C  finite-envelope construction, well-definedness, comparison, openness
|-- M0107-L  open factor, finite factor, and factorization equation
|   `-- M0107-L-FINITE
|       `-- M0107-L-INTEGRAL-TO-FINITE  [principal open bridge]
`-- M0107-T  exact conditional assembly
```

Proof/refinement edges reach every required obligation and are acyclic. Provenance, evidence,
trust, documentation, and workflow edges are stored separately, so an imported name or audit link
cannot become proof credit. Nonleaves are `split-required`; leaf-shaped planned interfaces carry
short semantic ledgers and must be split again if formalization exposes hidden work.

## Composition boundary

`ObligationTree.lean` checks a conditional composition that consumes open immersion, finiteness,
and composition equality for the normalization maps and produces the exact existential shape.
It proves none of those premises. The anchor audit supports candidates for the open factor and
equation, but this phase closes no obligation. The finite envelope and the integral-to-finite
bridge remain the explicit root cut set. No `AUDIT-Z`, `THEOREM-Z`, H0, R0, proof closure, release
trust, or master acceptance is claimed.
