# Source-statement crosswalk

| Claim component | Primary-source discovery anchor | Lean surface | Intake assessment |
|---|---|---|---|
| General global correspondence for `GL_n` over a function field | Laurent Lafforgue, *Chtoucas de Drinfeld et correspondance de Langlands*, Inventiones Mathematicae 147 (2002), 1-241, DOI `10.1007/s002220100174` | No concrete repo-local declaration | Leading root reading; theorem/page, edition hash, assumptions, and errata still require audit |
| Rank-two historical case | V. G. Drinfeld, *Langlands' conjecture for GL(2) over functional fields*, Proceedings of the ICM Helsinki (1978), 565-574 | No concrete repo-local declaration | Strictly narrower candidate; cannot substitute for a selected `GL_n` root |
| Global function-field substrate | Same sources' curve/function-field setting | `FunctionField Fq F` and related mathlib APIs | Reusable substrate, not correspondence evidence |
| Galois side | Irreducible l-adic representations, with determinant restriction in the standard formulation | Legacy `LanglandsParameter` structure | The local structure is an abstract discovery model and lacks continuity, Galois action, coefficients, equivalence, and ramification |
| Automorphic side | Cuspidal automorphic representations of `GL_n` over the adele ring, with central-character restriction | Legacy `CuspidalAutomorphicRepresentation` structure | Abstract discovery model; it does not define adeles, `GL_n`, automorphicity, or representation equivalence |
| Local compatibility | Unramified Frobenius data matched with Hecke/Satake data | `LocalLanglandsCompatibility` | Existing rank equality is materially weaker and receives no statement or proof credit |
| Bijection and uniqueness | Correspondence on isomorphism classes | Legacy `StatementShape` has only `forall rho, exists pi` | One direction without uniqueness; not equivalent to a correspondence |

The Stage1 queue prose says only "function-field Langlands correspondence" while adjacent
`THM-M-0433` says "function-field `GL_n` Langlands correspondence". That collision is an explicit
source-identity blocker, not permission to select whichever theorem is easiest. The statement phase
must record an immutable primary-source copy, exact theorem/page and assumptions, correction/errata
search, and an independently reviewed choice of root.

Discovery links (not immutable evidence receipts):

- Laurent Lafforgue: <https://doi.org/10.1007/s002220100174>
- Drinfeld bibliographic record: <https://www.mathunion.org/fileadmin/ICM/Proceedings/ICM1978.1/ICM1978.1.ocr.pdf>

No `H0` claim is made. The provisional wording in `intake.json` is deliberately broader than the
legacy Lean scaffold and may not be used as an exact target until the ambiguity is resolved.
