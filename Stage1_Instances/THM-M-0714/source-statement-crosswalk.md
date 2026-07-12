# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records `MRDP定理`, attributes it to
Matiyasevich/Robinson/Davis/Putnam, dates it to 1970, and gives the sole mathematical gloss
`递归可枚举集是丢番图集` ("recursively enumerable sets are Diophantine sets"). Stage0 repeats
this metadata. The rev-5.6 manifest preserves `已验证` only as `source_status_untrusted`.

The record identifies the standard forward implication but supplies no primary-source edition,
theorem/page, definition of recursive enumerability, arity, coefficient/witness domains, proof
boundary, assumptions, or errata. It therefore cannot support `H0` or an exact formal expression.

## Candidate source work

The pinned mathlib module cites Mario Carneiro, *A Lean formalization of Matiyasevic's theorem*, and
Martin Davis, *Hilbert's tenth problem is unsolvable*. These are candidate locators only at intake;
no edition and exact passage has yet been independently cross-checked against the repository claim.
The source audit must record the exact statement and definitions, page/theorem location,
assumptions, proof boundary, errata search, and independent review.

## Crosswalk

| Repository phrase | Mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "set" | subset of a finite power of `Nat` | `Set (Fin n -> Nat)` or checked equivalent | arity/coding open |
| "recursively enumerable" | domain/range recognized by partial computation | `Nat.Partrec`, `Partrec`, and a frozen predicate encoding | APIs probed; bridge open |
| "Diophantine" | existential witnesses satisfying an integer polynomial equation | mathlib `Dioph` and `Poly` | definition probed; transport open |
| "is" | forward implication for every eligible set | exact quantified Lean proposition | absent pending source freeze |
| MRDP | general closure from r.e. sets, not only exponentiation | proof architecture connecting computation codes to `Dioph` | not present in intake |
| `已验证` | untrusted inventory label | no proposition or proof credit | explicitly rejected |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded probe imports
`Mathlib.Computability.Partrec` and `Mathlib.NumberTheory.Dioph`. It checks `Nat.Partrec`, generic
`Partrec`, `Dioph`, `Dioph.DiophPFun`, `Dioph.DiophFn`, `Dioph.dom_dioph`, and
`Dioph.pow_dioph`.

The header of `Mathlib.NumberTheory.Dioph` describes `pow_dioph` as a version of Matiyasevich's
theorem and its TODO explicitly says "Finish the solution of Hilbert's tenth problem." Thus the
checked substrate must not be promoted to a full MRDP anchor. A later anchor audit must inspect the
complete pinned declaration inventory and any immutable external candidates.
