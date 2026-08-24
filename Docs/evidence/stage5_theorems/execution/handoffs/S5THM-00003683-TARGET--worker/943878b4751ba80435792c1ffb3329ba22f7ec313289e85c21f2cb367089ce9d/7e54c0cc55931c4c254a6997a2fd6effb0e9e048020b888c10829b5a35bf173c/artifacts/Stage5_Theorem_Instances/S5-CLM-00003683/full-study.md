# Full study

## Statement

The frozen provider claim asserts that every odd natural number strictly between `1` and `2^50` is a squarefree natural plus a power of two. The order and content of all four binders are preserved.

## Construction

Because the domain is finite, a complete certificate may map each admissible `n : Fin (2^50)` to bounded witnesses `k : Fin (2^50)` and `l : Fin 50`. The output already contains `Squarefree k.1` and the exact equality, so reconstruction is elimination of finite subtypes only. The bound on `k` follows automatically from the equality and positivity of `2^l`; recording it in the certificate makes the data finite. An exponent at least `50` would make `2^l ≥ 2^50 > n`, so `Fin 50` loses no valid witness.

## Trust boundary

The pinned FormalConjectures file establishes statement provenance only. Its `sorryAx` body is excluded. The claim-owned proof consumes an explicit certificate parameter and adds no declaration capable of shadowing `Odd`, `Squarefree`, natural powers, equality, or the provider namespace. Master compilation must replay all three Lean files from source with trust zero and independently census their transitive constants.

## Mutation obligations

Validation must reject changing `2^50`, removing `Odd n`, weakening `1 < n`, replacing `Squarefree`, swapping addition for another operation, using the provider proof body, introducing a semantic alias, or deleting either witness/equality component. It must also reject an empty readability map, a noninjective anchor map, or a release receipt whose trace does not bind current bytes.

## Downstream use

The resulting theorem package binds Stage5 claim `S5-CLM-00003683` to Stage6 claim `S6-CLM-00003101`, variant `S6-VAR-00007359`, without counting the provider declaration or the three proof variants as additional mathematical completions.
