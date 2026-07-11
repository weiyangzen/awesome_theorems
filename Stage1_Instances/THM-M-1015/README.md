# THM-M-1015 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for Slutsky's theorem. Historical slot
`S1-M-294` is discovery material only and supplies no accepted proof or statement credit.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | If `X_n` converges in distribution to `X` and `Y_n` converges in probability to a constant `c`, then the pair, sum, and product converge to their corresponding limits; if `c != 0`, the quotient converges to `X / c` | Exact Lean elaboration and fingerprint belong to the statement phase |
| Domains | Real-valued random variables; one common source probability space for `X_n,Y_n`, with the limit variable allowed on another probability space | General topological/algebraic variants are excluded from the canonical root |
| Preconditions | probability measures, the relevant measurability conditions, convergence in distribution, convergence in probability, and `c != 0` only for division | Minimality and API-imposed measurability must be checked later |
| Conclusions | joint pair, addition, multiplication, and nonzero-denominator division | None may be silently dropped; the legacy wrapper omits division |
| Degenerate cases | `c = 0` remains valid for pair/sum/product but is excluded from the quotient branch | Boundary mutations remain open |
| Foundations | Lean 4 kernel and pinned mathlib | Exact toolchain, imports, trust assumptions, and dependency closure remain open |

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M3, R3]`. The source wording is frozen,
but primary-source pinpoint/errata review, canonical Lean expression, checked transports, mutation
tests, and environment fingerprint are not. The historical `StatementShape` is not adopted because
it omits the standard quotient conclusion. The first failed theorem gate is the exact statement
gate. This intake is self-tested but the theorem is not complete.

## Files

The structured scope is in `intake.json`, the source and legacy-statement relationship is in
`source_statement_crosswalk.md`, and exact commands and results are in `validation.md`.
