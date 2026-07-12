# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` names Ivan Vinogradov, dates the result to 1937, and states
`充分大的奇数可表为三素数之和` ("every sufficiently large odd number can be represented as a
sum of three primes"). `Docs/Stage0_Blueprint.md` repeats that sentence but marks the exact
definitions, proof route, dependencies, axioms, and machine artifact as open. The rev-5.6 manifest
retains `已验证` only as `source_status_untrusted`; it grants no H or M credit.

## Historical discovery anchor

I. M. Vinogradov, *Representation of an odd number as a sum of three primes*, Doklady Akademii
Nauk SSSR 15 (1937), 291-294, is a candidate primary historical locator commonly associated with
this result. This intake has not bound an immutable scan, verified the bibliographic translation,
pinpointed the exact formula or corollary, mapped its notation and premises, searched corrections,
or obtained independent review. It is therefore discovery metadata, not `H0` evidence.

## Crosswalk

| Repository phrase | Intended mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "sufficiently large" | one threshold uniform over later inputs | `Exists fun N : Nat => forall n, N <= n -> ...`, or checked `Filter.Eventually` equivalent | shape frozen; exact encoding open |
| "odd number" | an input satisfying odd parity | `Odd n` or `n % 2 = 1` with a checked equivalence | pinned APIs available; source domain open |
| "three primes" | witnesses `p`, `q`, `r`, each prime | `Nat.Prime p`, `Nat.Prime q`, `Nat.Prime r` | pinned predicate available; repetition convention open |
| "represented as a sum" | exact equality `n = p + q + r` | natural addition and equality | shape frozen; binder/order conventions open |
| 1937 / Vinogradov | historical provenance | no Lean proposition | primary-source verification open |
| `已验证` | untrusted inventory label | no proof object | explicitly rejected as evidence |

## Fidelity boundary

The repository sentence distinguishes the eventual three-prime theorem from both binary Goldbach
and an almost-all result, but does not provide a reviewable source locator or the precise stronger
asymptotic statement often used in proofs. A later source audit must hash a stable edition or scan,
pinpoint the statement and all assumptions, determine prime/repetition/domain conventions, map any
representation-count formula to existence, check errata, and obtain qualified review. Until that
work is accepted, the source status is `H1`, not `H0`.

The intake Lean probe checks statement ingredients only. It does not claim that pinned mathlib
contains Vinogradov's theorem or that any formal proof has been located.
