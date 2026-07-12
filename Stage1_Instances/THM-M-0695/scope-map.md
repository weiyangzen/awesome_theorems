# Scope map

## Included topic boundary

- A source-selected formal logic and its derivation system.
- A source-selected typed term calculus and typing judgments.
- Explicit translations between propositions and types, contexts and typing contexts, and proofs
  and terms.
- The exact claimed preservation, reflection, equivalence, or operational property.
- Equality, reduction, structural-rule, universe, and quotient conventions needed by that property.

## Ambiguities to resolve at statement freeze

The repository wording does not decide among materially different theorem families:

1. **Judgmental correspondence:** derivations of a proposition correspond to typing derivations or
   inhabitants of its translated type.
2. **Connective/type-former correspondence:** implication/product/sum/falsehood/quantification map
   to function/product/sum/empty/dependent types, with introduction and elimination rules aligned.
3. **Operational correspondence:** proof normalization or cut elimination corresponds to term
   reduction, with preservation and possibly reflection.
4. **Categorical or dependent extensions:** intuitionistic logic, simply typed lambda calculus,
   dependent type theory, linear logic, and classical calculi yield different statements.

The statement phase must inspect immutable source passages and freeze one exact metatheorem,
ordered parameters, inductive syntax, judgments, translations, equivalence relation, hypotheses,
and conclusion. It must decide whether correspondence means a raw bijection, an equivalence modulo
proof/term equality, an iff of inhabitation, or preservation/reflection of steps.

## Explicit exclusions

- Treating Lean's use of propositions as types as, by itself, a proved metatheorem about two
  independently specified calculi.
- A few tautologies or type-checking examples substituted for the full correspondence.
- Soundness, completeness, normalization, cut elimination, canonicity, or type safety unless the
  selected source explicitly makes it part of the target.
- Classical Curry-Howard variants, linear logic, categorical semantics, or System F substituted
  for an unspecified base correspondence.
- The duplicate Stage0 computer-science record as an additional theorem or as source validation.
- The repository label `已验证` as human-source or machine-proof evidence.

No canonical Lean target is frozen at intake because the source record identifies only the family
and slogan, not the formal systems and theorem.
