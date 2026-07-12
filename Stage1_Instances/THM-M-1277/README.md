# THM-M-1277 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the two-dimensional sharp
Moser-Trudinger inequality. It does not inherit proof credit from the untrusted
Stage0 label `已验证`.

The canonical human claim is the bounded-domain, zero-boundary-value form: for
every nonempty bounded open `Omega` in `R^2`, the exponential integral of every
`u in W_0^{1,2}(Omega)` whose weak-gradient `L^2` norm is at most one is bounded
uniformly at exponent `4*pi`. For every exponent larger than `4*pi`, that
uniform bound fails. The structured statement and deliberate intake-level
formal target are in `intake.json`; `scope-map.md` fixes inclusions and
exclusions; `source-statement-crosswalk.md` records the source relationship.

## Statement verdict

Lifecycle remains `planned`; provisional root vector is `[H1, M3, R3]`.
`Statement.lean` elaborates the exact selected target, including an explicit
completion encoding of `W₀¹,²`, a selected weak gradient, an extended-valued
integral, the endpoint bound, and supercritical sharpness. Nonemptiness is
explicit because the sharpness conjunct is false on the empty domain. This is
statement evidence only: no theorem, proof, mathlib anchor, or machine closure
is credited here.

## Open task DAG

`INTAKE -> STATEMENT -> ANCHOR_AUDIT -> OBLIGATION_TREE -> PROOF -> VALIDATION -> RELEASE`.
Only `INTAKE` is addressed by this dossier, subject to master acceptance.
