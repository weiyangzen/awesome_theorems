# THM-M-0447 rev-5.6 intake

This is the `planned` rev-5.6 instance for the Taylor-Wiles method. The broad source label does not
identify a unique theorem. Intake selects the classical minimal, two-dimensional, odd modularity-
lifting setting over `Q`, while explicitly leaving the exact primary-source theorem and concrete
Lean encoding to the dependent statement phase.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | minimal `R = T` result and its modularity-lifting consequence over `Q` | Whether `R = T` or modularity is canonical root awaits source pinning |
| Global side | continuous odd two-dimensional Galois representations of `G_Q` | The legacy module uses an abstract carrier, not a concrete absolute Galois API |
| Residual side | odd, absolutely irreducible, modular residual representation | Exact determinant and auxiliary restrictions remain unfrozen |
| Local side | minimal ramification away from `p`; selected ordinary/finite-flat behavior at `p` | Prime, level, and local deformation functors require exact source mapping |
| Automorphic side | weight-two modular forms and the relevant Hecke algebra | Eigenvalue compatibility and localization are only abstract predicates in the legacy candidate |
| Patching side | auxiliary Taylor-Wiles primes, numerical criterion, patched module, `R = T` | No terminal Taylor-Wiles Lean theorem is credited |
| Excluded families | nonminimal, ordinary-family, Hilbert/totally-real, and modern automorphy-lifting variants | A later scope change invalidates this intake |

The initial proof-package map is: `TW-S` exact statement; `TW-D` deformation problem and universal
ring; `TW-H` Hecke algebra and Galois-to-Hecke map; `TW-Q` auxiliary-prime systems; `TW-P` patching
and freeness/faithfulness; `TW-N` numerical criterion; `TW-RT` exact isomorphism; `TW-MOD`
modularity corollary. These are architecture seeds, not a frozen obligation registry and carry no
proof credit.

## Intake verdict

Lifecycle is `planned`, with provisional vector `[H1, M3, R3]`. The first failed theorem gate is the
exact-statement gate: the primary theorem/premises, concrete Lean object model, normalized expression
hash, environment fingerprint, transports, and mutation tests are absent. The theorem is not complete.

## Validation

The exact commands and results are recorded in `validation.md`. They validate manifest membership,
repository standard consistency, JSON syntax, and dossier-local references only.
