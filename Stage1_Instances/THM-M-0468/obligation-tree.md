# THM-M-0468 frozen obligation architecture

Item: `S56-M-0468-OBLIGATION_TREE`.

The registry freezes 20 semantic obligations before proof execution. It uses
the Ullmo--Zhang equidistribution/stabilizer route for the difficult direction
and torsion density for the converse. These are architectural commitments, not
proof claims. Primary-source pinpoint and errata review remain open.

## Typed proof route

```text
M0468-ROOT exact canonical equivalence
`-- M0468-T-ASSEMBLE checked conditional composition
    |-- M0468-B-FORWARD dense small points imply special
    |   |-- M0468-N-BASECHANGE geometric base normalization
    |   |-- M0468-N-HEIGHT canonical-height package
    |   |-- M0468-C-GENERIC generic small sequence
    |   |-- M0468-L-EQUIDISTRIBUTION equidistribution
    |   |-- M0468-C-DIFFERENCE difference morphism
    |   |-- M0468-L-MEASURE canonical-measure comparison
    |   `-- M0468-L-STABILIZER stabilizer descent/classification
    `-- M0468-B-CONVERSE special implies dense small points
        |-- M0468-N-BASECHANGE geometric base normalization
        |-- M0468-N-HEIGHT canonical-height package
        |-- M0468-C-TORSION torsion-translate subset
        |-- M0468-L-TORSION-HEIGHT height zero on torsion
        `-- M0468-L-TORSION-DENSE torsion density
```

Statement definitions, domain interpretation, boundary cases, foundation
policy, sources, trust, documentation, and workflow live in separate typed
graphs and cannot be counted as proof premises.

## Node ledger

### m0468-root
Exact elaborated Ullmo--Zhang target. `[H1, M4, R3]`; no inhabitant exists.

### m0468-s-definitions
Checked typed definitions for small points and specialness. `[H1, M0-L, R3]`.

### m0468-s-domains
Open interpretation of the semantic carrier by actual number-field abelian
geometry. `[H1, M4, R3]`.

### m0468-s-boundary
Open checks for `X=A`, zero-dimensional integral `X`, and all positive
thresholds. `[H1, M4, R3]`.

### m0468-s-foundation
Pending classical, quotient, algebraic-closure, TCB, and no-oracle profile.
`[H1, M4, R3]`.

### m0468-n-basechange
Base-change compatibility for points, subvarieties, density, height, and
specialness. `[H1, M4, R3]`.

### m0468-n-height
Neron--Tate nonnegativity, functoriality, and torsion invariance. `[H1, M4, R3]`.

### m0468-b-forward
The dense-small-points-to-special implication. `[H1, M4, R3]`.

### m0468-c-generic
Construct a generic sequence of small points with density-detecting Galois
orbits. `[H1, M4, R3]`.

### m0468-l-equidistribution
Equidistribution of that sequence for the canonical measure. `[H1, M4, R3]`.

### m0468-c-difference
Difference-map construction and generic-finiteness control. `[H1, M4, R3]`.

### m0468-l-measure
Canonical-measure comparison yielding the degeneracy contradiction.
`[H1, M4, R3]`.

### m0468-l-stabilizer
Stabilizer quotient/descent and torsion-translate classification. `[H1, M4, R3]`.

### m0468-b-converse
The special-to-dense-small-points implication. `[H1, M4, R3]`.

### m0468-c-torsion
Construct torsion translates inside `X=t+B`. `[H1, M4, R3]`.

### m0468-l-torsion-height
Prove those points have canonical height zero. `[H1, M4, R3]`.

### m0468-l-torsion-dense
Prove torsion points are Zariski dense in the abelian subvariety. `[H1, M4, R3]`.

### m0468-t-assemble
Kernel-checked composition from both directions to the exact root. Its
premises are explicit and open. `[H1, M0-L, R3]`.

### m0468-x-source
Pending theorem/page/assumption/errata map for every material node. `[H1, M4, R3]`.

### m0468-x-provenance
Pending body, import, axiom, TCB, and replay inventory. `[H1, M4, R3]`.

## Freeze boundary

The immediate open root cut is `M0468-B-FORWARD` plus
`M0468-B-CONVERSE`. The conditional assembly proves neither premise. This
phase supplies no H0, root closure, audit completion, or theorem completion.
Any correction, split, merge, exclusion, or eligibility change requires a new
registry version and append-only delta.
