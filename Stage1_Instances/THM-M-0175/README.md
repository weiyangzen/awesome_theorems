# THM-M-0175 rev-5.6 intake

Status: `planned`; intake only. The manifest gloss is "the divisor dimension formula on an algebraic
curve." This dossier freezes that as the classical divisor form of Riemann-Roch. No exact Lean
expression, source acceptance, or proof closure is claimed.

## Scope map

| Surface | In scope | Intake boundary |
|---|---|---|
| Base and curve | field `k`; smooth, projective, geometrically integral curve `X/k` | concrete scheme predicates and universes remain open |
| Divisor data | arbitrary divisor `D` and canonical divisor `K_X` | Cartier/Weil representation and canonical-sheaf bridge remain open |
| Invariants | `l(E) = dim_k H^0(X, O_X(E))`, degree, genus | finiteness proofs and integer/natural coercions remain open |
| Root equality | `l(D)-l(K_X-D)=deg(D)+1-g(X)` | must be elaborated and mutation-tested in `STATEMENT` |
| Exclusions | singular, nonproper, disconnected, non-geometrically-integral, or higher-dimensional schemes | variants receive no root credit |
| Trust | Lean 4 kernel and repository-pinned mathlib | exact toolchain, dependency, axiom, and TCB fingerprints remain open |

`THM-M-0105` has materially overlapping legacy wording. It is discovery input only: this target has
its own identity and cannot inherit that dossier's statement, evidence, or acceptance.

## Open task DAG

`S56-M-0175-STATEMENT -> ANCHOR_AUDIT -> OBLIGATION_TREE -> PROOF -> VALIDATION -> RELEASE`.
The statement phase must choose concrete Lean objects, freeze the expression/environment hashes,
and test assumptions and boundary mutations. The audit must independently verify the primary source
and search pinned Lean candidates. Only then may the obligation registry be frozen.

## Intake verdict

The provisional root vector is `[H5, M5, R4]`. The first failed theorem gate is the exact statement
gate. All dependent phases and master acceptance remain open; the theorem is not complete.

Exact validation commands and results are recorded in `validation.md`.
