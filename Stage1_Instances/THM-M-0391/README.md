# THM-M-0391 rev-5.6 intake

This directory is the `planned` intake dossier for Mihailescu's theorem, formerly Catalan's
conjecture. The exact root is the positive natural-number statement frozen in `instance.json`:
the sole solution of `x^a = y^b + 1` with both bases and exponents greater than one is
`3^2 = 2^3 + 1`.

The legacy `S1_M_005.lean` statement shape agrees syntactically with this scope, but rev-5.6 grants
it no inherited statement or proof credit. Elaboration, expression identity, transports, mutation
tests, dependency pinning, and kernel closure belong to later dependent nodes.

## Intake verdict

Manifest membership and repository structural gates pass. Lifecycle is `planned`, the provisional
debt vector is `[H1, M4, R4]`, and `theorem_complete` is false. H1 records that the theorem is a
published human result while the exact primary-source theorem/page/errata crosswalk still needs an
independent source audit. M4 records that no terminal Lean proof is credited.

See `scope-map.md`, `source-statement-crosswalk.md`, and `validation.md` for the boundaries and
self-test evidence.
