# THM-M-0387 rev-5.6 statement

This directory is the new rev-5.6 `planned` instance for Fermat's Last Theorem. It does not inherit
proof credit or accepted state from the legacy `THM-M-0387/` dossier.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | `FermatLastTheorem`, over nonzero naturals and every `n > 2` | Elaboration and expression fingerprint belong to the dependent statement phase |
| Statement layer | fixed-exponent form, natural/integer/rational transports, primitive/coprime form | All transports are candidates, not credited evidence |
| Reduction | exponent divisibility, prime-exponent reduction, recomposition | Architecture only; no closure claimed |
| Special branches | exponents 3 and 4, divisible-by-4 derivatives, regular odd primes | Legacy checks are discovery inputs only |
| General branch | every remaining odd prime through Frey, modularity, level lowering, contradiction | Open machine frontier |
| Foundations | Lean 4 kernel plus an accepted, versioned classical/choice/quotient policy | Profile and dependency fingerprint remain open |

The mandatory minimum proof-tree scope is section 12.2 of the authoritative blueprint: `M0387-S`,
`M0387-R`, `M0387-B3`, `M0387-B4`, `M0387-RP`, and `M0387-WTW`. None is collapsed or excluded here.
The canonical human claim and intake scope remain in `intake.json`. `Statement.lean` now elaborates
the exact natural-number proposition with only `Init`, checks it against the direct unfolding of
the pinned mathlib source shape, and supplies executable mutation fixtures. The expression and
environment fingerprints are in `statement.json`; exact commands are in `statement-validation.md`.

## Statement verdict

Lifecycle remains `planned`, and the theorem is not complete. The exact target elaborates and the
statement mutation suite passes, pending master acceptance. No proof body is introduced. Known
integer, rational, and primitive alternate encodings are not recredited because this worker's
materialized pinned cache lacks the mathlib FLT oleans needed to recheck them without a prohibited
dependency build or fetch.

## Validation

On base revision `a8d6489fd935cd71fa4499f2f3f5b051998203f4`, the worker ran the commands recorded in
`validation.md`. They establish manifest membership, repository-standard consistency, JSON syntax,
and dossier-local reference integrity only.
