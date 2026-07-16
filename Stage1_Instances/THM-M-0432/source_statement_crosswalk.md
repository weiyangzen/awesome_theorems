# Source-statement crosswalk

## Repository identity boundary

`Docs/researches/math_theorems.md:3158-3163` supplies only the Chinese label "function-field
Langlands correspondence", Vladimir Drinfeld, 1974, the same phrase as a gloss, importance, and an
untrusted verified label. The neighboring entry `THM-M-0433` separately names Laurent Lafforgue and
the function-field `GL_n` correspondence. That adjacency makes Drinfeld's rank-two result the
historical candidate here, but it does not select an exact theorem, page, direction, or
normalization. The provisional general-`GL_n` wording in `intake.json` is therefore not a frozen
source claim.

## Discovery candidates

- V. G. Drinfeld, *Langlands' conjecture for GL(2) over functional fields*, Proceedings of the ICM
  Helsinki (1978), pages 565-574. This is the leading historical source candidate. No immutable
  source copy, exact theorem label, or independently reviewed transcription is admitted in the
  dossier.
- Laurent Lafforgue, *Chtoucas de Drinfeld et correspondance de Langlands*, Inventiones
  Mathematicae 147 (2002), 1-241, DOI `10.1007/s002220100174`. This is the general `GL_n` result and
  belongs to neighboring `THM-M-0433`; it is not a substitute for a missing exact Drinfeld target.

These are discovery anchors, not immutable evidence receipts and not an `H0` claim.

## Claim crosswalk

| Claim component | Source information still required | Pinned Lean surface | Statement disposition |
|---|---|---|---|
| Global base | Exact curve/global function field, constant field, and chosen place | `FunctionField`; `FunctionField.classNumber` | Adjacent substrate only; binders unfrozen |
| Rank-two Galois side | Coefficient prime/field, continuity, irreducibility, determinant condition, ramification, and isomorphism relation | `Field.absoluteGaloisGroup`; `Representation` | Object model incomplete; no canonical domain |
| Automorphic side | Cuspidal representations of `GL_2` over the full function-field adele ring, central character, and isomorphism relation | `Matrix.GeneralLinearGroup` only | Function-field adeles and automorphic representations absent |
| Direction or bijection | Exact source clause, injectivity/surjectivity, and any fixed-place condition | No terminal declaration | Unfrozen conclusion |
| Local compatibility | Exceptional places and geometric/arithmetic Frobenius, Hecke/Satake polynomial, and normalization conventions | `AlgHom.IsArithFrobAt` is only an arithmetic-Frobenius primitive | No checked transport to a local compatibility claim |
| General `GL_n` form | Lafforgue's later theorem | No terminal declaration | Excluded as neighboring theorem, not used to broaden this target |

## Existing Lean boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_060.lean` is discovery input only. Its
`StatementShape` takes caller-supplied parameter and automorphic types, conversion functions, and an
unconstrained `corresponds` predicate. Its original compatibility predicate is rank equality and its
conclusion is one-way existence without uniqueness. The file itself records
`terminalCorrespondenceStatement := false`. It cannot be transported to Drinfeld's theorem without
assuming away the correspondence.

The target-owned `Statement.lean` therefore checks only six nearby pinned interfaces and declares no
canonical target. Before the positive statement gate can run, an accountable review must admit an
immutable source theorem/page, incorporate all referenced definitions, reconcile corrections and
errata, select the exact direction and quotient sets, and approve the premise/conclusion crosswalk.
