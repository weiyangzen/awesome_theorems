# THM-M-1277 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the two-dimensional sharp
Moser-Trudinger inequality. It does not inherit proof credit from the untrusted
Stage0 label `已验证`.

The canonical human claim is the bounded-domain, zero-boundary-value form: for
every bounded open `Omega` in `R^2`, the exponential integral of every
`u in W_0^{1,2}(Omega)` whose weak-gradient `L^2` norm is at most one is bounded
uniformly at exponent `4*pi`. For every exponent larger than `4*pi`, that
uniform bound fails. The structured statement and deliberate intake-level
formal target are in `intake.json`; `scope-map.md` fixes inclusions and
exclusions; `source-statement-crosswalk.md` records the source relationship.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M4, R3]`. The exact
Lean encoding is intentionally not claimed: choices of Sobolev zero trace,
weak gradient, extended integral, and the sharpness quantifiers must be
elaborated and mutation-tested in the dependent statement phase. No theorem,
proof, mathlib anchor, or machine closure is credited here.

## Open task DAG

`INTAKE -> STATEMENT -> ANCHOR_AUDIT -> OBLIGATION_TREE -> PROOF -> VALIDATION -> RELEASE`.
Only `INTAKE` is addressed by this dossier, subject to master acceptance.

