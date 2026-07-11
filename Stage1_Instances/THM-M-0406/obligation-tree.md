# THM-M-0406 obligation tree

Item `S56-M-0406-OBLIGATION_TREE` freezes registry
`THM-M-0406-OBLIGATIONS-v1` before assigning proof credit. The route follows
the source architecture identified by the anchor audit. It is a typed plan,
not a reconstruction or proof of Corvaja--Zannier Theorem 1.

## Frozen route

```text
M0406-ROOT
`-- M0406-T-ROOT-ADAPTER (checked interface)
    `-- M0406-T-ENGINE
        |-- M0406-N-BOUNDARY
        |-- M0406-N-INTEGRAL
        |-- M0406-C-AUXILIARY
        |-- M0406-L-HEIGHT-INEQUALITY
        |-- M0406-X-SUBSPACE
        |-- M0406-B-EXCEPTIONAL
        |-- M0406-L-DIMENSION-DROP
        `-- M0406-C-CURVE-UNION
```

`ObligationTree.lean` checks that `SurfaceDegeneracyEngine` is definitionally
the canonical root and checks both transport directions. Its engine argument
is an open premise, so this is composition-interface evidence only.

## Node boundaries

### m0406-root

The exact frozen Corvaja--Zannier proposition. `[H1, M4, R3]`.

### m0406-s-definitions

Audits the abstract interfaces for the surface, affine open, boundary
divisors, intersection numbers, rational/S-integral points, and proper curves.
These interfaces elaborate but do not imply the result. `[H1, M4, R4]`.

### m0406-s-foundation

Requires the eventual proof's transitive constants, axioms, dependencies,
computations, and TCB report. It cannot close before proof bodies exist.
`[H1, M4, R3]`.

### m0406-n-boundary

Normalizes the finite weighted boundary family while preserving distinctness,
the no-triple-point condition, positivity, and every common-intersection
identity. `[H1, M4, R4]`.

### m0406-n-integral

Converts S-integrality into uniform local-height or valuation bounds outside
the finite place set. This is a material arithmetic bridge. `[H1, M4, R4]`.

### m0406-c-auxiliary

Constructs sections or rational functions with prescribed boundary orders and
proves their pole, independence, and dimension properties. The `100`-step
budget is a future split threshold, not proof evidence. `[H1, M4, R4]`.

### m0406-l-height-inequality

Combines auxiliary sections, local estimates, and the product formula into the
global inequality needed by the Subspace Theorem. `[H1, M4, R4]`.

### m0406-x-subspace

The central external bridge: a quantitative Schmidt Subspace Theorem over the
number field yields finitely many proper exceptional linear subspaces. No
pinned Lean candidate was found, so it remains formalization debt. `[H1, M4,
R3]`.

### m0406-b-exceptional

Treats each exceptional linear relation, excludes identically vanishing
pullbacks, constructs proper zero loci, and recombines the finite cases.
`[H1, M4, R4]`.

### m0406-l-dimension-drop

Uses the surface hypotheses to turn proper exceptional loci into
curve-dimensional components. `[H1, M4, R4]`.

### m0406-c-curve-union

Forms one finite union of exceptional curve components on the affine open and
proves curvehood, properness, and containment of every selected point.
`[H1, M4, R4]`.

### m0406-t-engine

Composes every arithmetic and geometric child into the exact
`SurfaceDegeneracyEngine`. It is the minimal mathematical root cut, but all of
its premises remain open. `[H1, M4, R3]`.

### m0406-t-root-adapter

`corvajaZannierTheoremOne_of_engine` is a kernel-checked child-to-root
interface. Its engine premise is open, so the node remains `M4` and gets no
terminal proof-body credit. `[H1, M4, R3]`.

### m0406-x-provenance

Requires content-addressed proof-body origins, dependency and axiom closure,
computation records, and receipts after implementation. `[H1, M4, R3]`.

## Frozen boundary

There are 14 canonical root-relevant machine obligations; 11 require
human-source crosswalks and all 14 require readable treatment. No obligation
is closed. Closing `M0406-T-ENGINE` would still require the checked adapter,
trust, provenance, review, and validation gates before root completion.
`audit_complete=false` and `theorem_complete=false`.
