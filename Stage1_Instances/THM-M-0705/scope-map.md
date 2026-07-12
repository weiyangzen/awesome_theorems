# Scope map

## Included mathematical boundary

- Untyped lambda terms under a source-confirmed representation of variables, binding, and
  capture-avoiding substitution.
- The source-selected one-step beta-reduction relation and its reflexive-transitive closure.
- The confluence diamond from two finite reductions with a common source to a common reduct.
- Open terms unless the inspected source explicitly restricts the theorem.
- Zero-step branches, including the cases where either reduct is the source or the two reducts are
  already equal.

## Decisions required at statement freeze

1. Whether raw terms are quotiented by alpha-equivalence or encoded so alpha-equivalent terms are
   definitionally represented together, for example with de Bruijn indices.
2. Whether reduction is compatible closure of beta contraction, parallel beta reduction, or a
   source-specific auxiliary relation; an auxiliary relation may support the proof but cannot
   replace the final beta-reduction theorem.
3. Whether the historical result selected is beta confluence, beta-eta confluence, or the
   conversion formulation saying convertible terms have a common reduct.
4. The orientation and exact closure operators used for one-step, many-step, conversion, and join.
5. Whether all terms or only closed terms are quantified, and all substitution side conditions.

## Explicit exclusions

- Confluence of an arbitrary abstract relation as a substitute for confluence of lambda reduction.
- The local/weak diamond condition alone; without the required termination hypothesis it is not
  interchangeable with global confluence.
- Strong normalization, uniqueness of normal forms, subject reduction, or typed-lambda results as
  substitutes for the Church-Rosser theorem.
- Beta-eta confluence when the selected source target is beta-only, or conversely.
- A structure or hypothesis that assumes the desired confluence and then projects it.
- The repository label `已验证` or mathlib's generic theorem name as human or machine proof credit.

The provisional claim identifies the intended theorem family, but no canonical Lean expression is
frozen during intake.
