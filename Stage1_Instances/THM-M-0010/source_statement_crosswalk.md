# Source-statement crosswalk

| Claim component | Human source anchor | Planned Lean component | Intake assessment |
|---|---|---|---|
| Noetherian ring, ideal, finite module, submodule | M. F. Atiyah and I. G. Macdonald, *Introduction to Commutative Algebra* (Addison-Wesley, 1969), Proposition 10.9, commonly titled the Artin-Rees lemma | `CommRing R`, `IsNoetherianRing R`, `Ideal R`, `Module.Finite R M`, `Submodule R M` | Primary textbook anchor identified; scan hash, exact page locator, errata, and reviewer are not accepted: `H1` |
| Eventual equality | Proposition 10.9: for some `k`, `I^n M ∩ M' = I^(n-k)(I^k M ∩ M')` for `n >= k` | existential `k`, universal `n`, submodule equality | This is the canonical intended root; notation and binder order require exact source and Lean inspection |
| Rees construction proof | Proof following Proposition 10.9 uses the graded/Rees module and its finite generation | future proof-architecture nodes only | A proof route, not proof evidence or a frozen obligation tree |
| Eventual containment corollary | Standard consequence `I^n M ∩ N ⊆ I^(n-k)N` | submodule order statement | Not substituted for the stronger canonical equality |
| Filtration formulation | Induced `I`-adic filtration on `N` agrees eventually with the shifted intrinsic filtration | prospective filtration API | Equivalence is unverified and receives no statement credit |

The source wording uses `M'` where this dossier uses `N`. The equality is intended literally as an
equality of submodules, with ideal powers acting on submodules; it is not merely an elementwise
membership claim or an eventual containment. The statement phase must verify the exact source
edition and assumptions, choose the actual mathlib operations, elaborate the ordered binders, and
mutation-test Noetherianity, finite generation, the `n >= k` guard, and boundary cases.

No `H0` or machine-closure claim is made. Immutable source hashes, pinpoint page, correction/errata
status, theorem-to-premise mapping, and independent source review remain required.
