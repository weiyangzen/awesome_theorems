# THM-M-0010 rev-5.6 dossier

This directory is the `planned` rev-5.6 instance for the Artin-Rees lemma. The historical source
label and Stage1 queue entry are discovery inputs only and confer no proof credit.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | Artin-Rees equality for a submodule of a finite module over a commutative Noetherian ring | Elaborated as `Stage1Instances.THM_M_0010.ArtinReesTarget`; master acceptance remains pending |
| Algebraic objects | ring `R`, ideal `I`, finite module `M`, submodule `N`, powers and ideal action on submodules | Selected from pinned `Mathlib.RingTheory.Filtration` |
| Quantifier order | data first, then `exists k`, then every `n >= k` | Frozen with separate ring/module universes and mutation-tested guard |
| Equality | `I^n M ∩ N = I^(n-k)(I^k M ∩ N)` | Both inclusions and subtraction normalization belong to later phases |
| Boundary cases | zero/unit ideals, zero/full submodules, trivial module, and `n = k` | Retained; zero/unit ideal, zero submodule, and `n = k` expressions elaborate |
| Human source | Atiyah-Macdonald, Proposition 10.9, with the Rees-module proof context | Edition/hash, assumptions, errata, and independent review remain open |
| Machine surface | Lean 4 plus pinned mathlib | Statement elaborates on Lean 4.29.0 against mathlib `8a1783...a95`; proof and later gates remain open |

The remaining task chain is immutable anchor audit, frozen obligation graphs, proof or pinned
integration, validation, and release reconciliation. No later node is credited here.

## Intake verdict

Lifecycle remains `planned`; the statement node is self-tested pending master acceptance. The exact
expression, environment fingerprint, checked transport, four mutations, and boundary expressions
are in `statement.json`, `Statement.lean`, and `statement-validation.md`. Human-source review,
proof closure, and all dependent gates remain open. The theorem is not complete.

## Validation

Intake checks remain in `validation.md`; statement checks are in `statement-validation.md`. The
latter validate elaboration of the exact target, not an Artin-Rees proof.
