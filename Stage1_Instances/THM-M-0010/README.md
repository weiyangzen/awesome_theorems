# THM-M-0010 rev-5.6 intake

This directory is the `planned` rev-5.6 instance for the Artin-Rees lemma. The historical source
label and Stage1 queue entry are discovery inputs only and confer no proof credit.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | Artin-Rees equality for a submodule of a finite module over a commutative Noetherian ring | The proposed Lean signature has not been elaborated |
| Algebraic objects | ring `R`, ideal `I`, finite module `M`, submodule `N`, powers and ideal action on submodules | Exact mathlib typeclasses and notation remain to be selected |
| Quantifier order | data first, then `exists k`, then every `n >= k` | Binder and universe mutation tests remain open |
| Equality | `I^n M ∩ N = I^(n-k)(I^k M ∩ N)` | Both inclusions and subtraction normalization belong to later phases |
| Boundary cases | zero/unit ideals, zero/full submodules, trivial module, and `n = k` | Retained rather than silently excluded; checks remain open |
| Human source | Atiyah-Macdonald, Proposition 10.9, with the Rees-module proof context | Edition/hash, assumptions, errata, and independent review remain open |
| Machine surface | Lean 4 plus pinned mathlib | Module, declaration candidates, toolchain fingerprint, and kernel check remain open |

The open task chain is statement elaboration, immutable anchor audit, frozen obligation graphs,
proof or pinned integration, validation, and release reconciliation. No later node is credited here.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M4, R3]`. The first failed theorem gate is
the exact statement gate: there is no elaborated expression, environment fingerprint, checked
transport, or mutation result. The theorem is not complete.

## Validation

The exact intake-only checks and results are recorded in `validation.md`. They validate repository
membership and dossier structure, not the mathematical statement or a Lean proof.
