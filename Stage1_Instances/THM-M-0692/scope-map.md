# Scope map

## Included topic boundary

- A source-selected sequent calculus and its exact formula and sequent syntax.
- Its derivation rules, including the precise cut rule and all logical, structural, quantifier,
  equality, and freshness conditions that the source uses.
- A source-selected cut-elimination conclusion: cut admissibility or a transformation from every
  derivation to a cut-free derivation of the same end-sequent.
- Any induction measures and preservation properties needed by that exact theorem.

## Ambiguities to resolve at statement freeze

The repository record does not decide among materially different targets:

1. Gentzen's classical multiple-conclusion `LK` or intuitionistic single-conclusion `LJ`.
2. Propositional logic or first-order logic, with or without equality.
3. One-sided or two-sided sequents and list, multiset, or set contexts.
4. Primitive or admissible weakening, contraction, and exchange.
5. Mere cut admissibility, existence of a cut-free derivation, an explicit normalization function,
   or a quantitative height/size bound.

The statement phase must inspect an immutable source, identify one theorem, and freeze ordered
binders, derivability and cut-free predicates, preservation of the end-sequent, eigenvariable
conditions, structural conventions, and all boundary cases. It must not silently combine variants.

## Explicit exclusions

- Normalization for natural deduction or lambda calculus as a substitute for sequent-calculus cut
  elimination.
- Resolution completeness, consistency, subformula property, decidability, or interpolation alone.
- A theorem for a toy propositional calculus substituted for an unspecified first-order claim.
- A `CutFree` field bundled into assumed data, followed by a tautological projection.
- The adjacent Craig-interpolation dossier's planned cut-elimination obligation as proof evidence.
- The repository label `已验证` as evidence of a human proof or kernel closure.

No canonical Lean target is frozen at intake because the repository source record does not identify
a unique calculus or proposition.

