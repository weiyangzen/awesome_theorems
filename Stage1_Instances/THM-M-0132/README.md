# THM-M-0132 rev-5.6 intake

This is the `planned` dossier for the modularity theorem (historically the Taniyama-Shimura-Weil
conjecture): every elliptic curve over `Q` is modular. Historical files are discovery inputs and
carry no rev-5.6 proof credit.

## Scope map

| Surface | In scope | Intake boundary |
|---|---|---|
| Exact root | Every elliptic curve over `Q` is modular | The concrete newform/conductor/compatibility encoding is not frozen |
| Curve side | Elliptic curves over `Q`, provisionally represented by elliptic Weierstrass curves | Representation equivalence and isomorphism invariance remain open |
| Modular side | A normalized cuspidal eigenform of weight 2 and the appropriate level/conductor | The legacy `CuspForm` witness lacks normalization, eigenform, coefficient, and level-matching data |
| Compatibility | L-series equality, Frobenius-trace coefficients, or compatible Galois representations | One exact formulation and checked transports must be selected later |
| Historical branch | Semistable elliptic curves (Wiles/Taylor-Wiles) | This branch cannot replace the unrestricted root proved by later work |
| Foundations | Lean 4 kernel and pinned mathlib | Environment, imports, axioms, and TCB fingerprint remain open |

The source-to-claim mapping is recorded in `source_statement_crosswalk.md`. Later phases must not
broaden "over `Q`" to another base, weaken "every" to semistable curves, or treat an arbitrary
inhabited `Prop` field as mathematical modularity.

## Intake verdict

Lifecycle is `planned`, with provisional vector `[H1, M3, R3]`. The first failed theorem gate is
the exact statement gate: there is no accepted normalized expression hash, environment fingerprint,
concrete modularity relation, checked transport, or mutation suite. The theorem is not complete.

## Validation

`validation.md` records the exact intake checks and their results. They validate membership,
repository structure, JSON syntax, and dossier consistency only; no Lean theorem closure is claimed.
