# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md` records `岩泽主猜想`, attributes it to Kenkichi Iwasawa in
1969, and gives only the phrase "the relation between cyclotomic-field `p`-adic L-functions and
class groups". `Docs/Stage0_Blueprint.md` repeats that phrase while leaving exact definitions,
hypotheses, proof path, dependencies, foundations, and machine artifact open. The manifest's
`已验证` value is explicitly `source_status_untrusted` and supplies no proof credit.

The repository also contains a separate analytic-number-theory record, `THM-M-0517`, with nearly
the same name and a legacy Stage1 discovery module. That duplication confirms the theorem family
but does not authorize sharing accepted state, receipts, or an exact statement between IDs.

## Primary-source candidates

- K. Iwasawa, *On Z_l-extensions of algebraic number fields*, Annals of Mathematics (2) 98
  (1973), 246-326, DOI `10.2307/1970910`: candidate for the original cyclotomic formulation and
  conventions.
- B. Mazur and A. Wiles, *Class fields of abelian extensions of Q*, Inventiones Mathematicae 76
  (1984), 179-330, DOI `10.1007/BF01388599`: candidate primary proof source for the cyclotomic
  theorem over abelian extensions of `Q`.

These bibliographic records are discovery anchors, not `H0` receipts. Intake did not inspect an
immutable edition or accept a theorem/page pinpoint, definitions, assumptions, corrections,
errata, or independent review.

## Component crosswalk

| Source/repository component | Required mathematical object | Required Lean surface | Intake status |
|---|---|---|---|
| "cyclotomic fields" | cyclotomic `Z_p`-extension and finite layers | cyclotomic fields, embeddings/tower maps, rings of integers | adjacent pinned APIs probed; exact tower open |
| "class groups" | norm-compatible inverse limit of `p`-primary ideal class groups | class groups, norm transition maps, inverse limit and module action | class groups available; terminal tower/module open |
| Iwasawa algebra | completed coefficient/group algebra acting on the inverse limit | concrete topological completed algebra | no source-selected construction |
| algebraic invariant | characteristic ideal/power series of a torsion module | torsion proof and characteristic-ideal theory | exact definition and hypotheses open |
| "`p`-adic L-function" | cyclotomic function with fixed interpolation normalization | `p`-adic measure/function in the same completed algebra | complex Dirichlet L-function APIs are only adjacent infrastructure |
| "relation" | equality of algebraic and analytic ideals | exact typed equality or checked equivalent transport | metadata underspecified; no Lean expression |
| `已验证` | untrusted inventory status | no formal proposition | rejected as source or machine evidence |

## Lean boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, `IntakeProbe.lean`
checks concrete APIs for cyclotomic fields, ideal class groups, `p`-adic numbers, cyclotomic
characters, and completed complex Dirichlet L-functions. These are encoding ingredients only. The
legacy `S1_M_257.lean` explicitly models missing tower, completed-algebra, characteristic-ideal,
and `p`-adic-L-function surfaces as abstract boundaries; its `StatementShape` is not the root
theorem.

Before `H0`, an immutable source edition must be hashed and mapped theorem/page and definition by
definition to all Lean binders, hypotheses, boundary cases, and the conclusion, with errata review
and independent approval. Before statement credit, every row must map to an elaborated expression
without moving the missing semantics into assumptions.
