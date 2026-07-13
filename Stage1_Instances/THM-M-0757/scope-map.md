# Scope map

## Preserved catalog scope

The repository fixes target `THM-M-0757`, the title `可容许序数` (admissible ordinals), Gerald
Sacks, the year 1966, and the gloss `alpha-recursion theory`. Importance "high" and status
`已验证` are catalog metadata, not source or kernel evidence. Intake preserves the admissible-
ordinal and generalized-recursion subject boundary without converting a field label into a
theorem.

## Proposition-changing decisions

An approved target correction and source crosswalk must select one truth-valued root and freeze:

- the definition of an admissible ordinal, including whether it uses equation-calculus closure,
  a constructible level satisfying an exact fragment such as Kripke-Platek set theory, or another
  source-mapped equivalent;
- the ordinal domain and universe, including countable versus arbitrary ordinals, recursive
  ordinals, the role of the Church-Kleene ordinal, limit/successor conventions, and required
  nonzero or closure hypotheses;
- the precise alpha-recursion model: finite equation systems, partial functions over an ordinal,
  alpha-recursively enumerable sets, definability over a set-theoretic structure, or another
  explicitly sourced coding;
- all parameters and oracle conventions, encodings of tuples and finite sequences, enumerability
  and totality notions, reducibilities, degree equivalences, and regularity assumptions;
- the desired conclusion, such as a definition/characterization theorem, closure theorem,
  existence of a bounded enumerable nonrecursive set, Post-problem solution, degree result, or
  another pinpointed result; and
- every ordered binder, hypothesis, dependency, equivalent formulation, degenerate case,
  foundation choice, and proof boundary.

These decisions yield distinct propositions. They are a resolution ledger, not a canonical claim.

## Candidate families not credited

- Equivalence between a selected closure definition of admissibility and a selected model-theoretic
  or constructible-hierarchy formulation.
- Development of alpha-recursive and alpha-recursively enumerable functions or sets at an
  admissible ordinal.
- The metarecursive specialization at the Church-Kleene ordinal.
- Existence of bounded metarecursively enumerable nonrecursive sets.
- A Post-problem, incomparable-degree, jump, regularity, or reducibility theorem over an admissible
  ordinal.
- Closure, hierarchy, basis, enumeration, or degree-structure results from alpha-recursion theory.

No family in this list is selected, asserted, or credited at intake.

## Neighboring-target boundary

The surrounding catalog separately owns jump operators (`THM-M-0752`), jump inversion
(`THM-M-0753`), the arithmetical and analytic hierarchies (`THM-M-0754`, `THM-M-0755`),
hyperarithmetic theory (`THM-M-0756`), and computably enumerable degrees (`THM-M-0758`). This
target may eventually depend on accepted nodes from those dossiers, but it cannot absorb their
statements or inherit their source or proof credit.

## Explicit exclusions

An ordinal type or proof that a set-theoretic object is an ordinal is not an admissibility theorem.
Ordinary natural-number partial recursiveness or oracle computability is not alpha-recursion without
a checked source-faithful bridge. A definition or structure that assumes admissibility or the desired
existence result as a field cannot serve as its proof. Generic ordinal arithmetic, recursive-
ordinal, hyperarithmetic, hierarchy, jump, and c.e.-degree results are not substitutes. Neither a
Sacks bibliography entry nor the catalog word `已验证` supplies theorem evidence.

## Formal boundary

No canonical Lean expression is frozen. Pinned mathlib supplies generic `Ordinal`, `ZFSet.IsOrdinal`,
and natural-number `RecursiveIn` infrastructure. A bounded exact-topic search found no declaration
for admissible ordinals, alpha-recursion, metarecursion, Kripke-Platek, or the constructible hierarchy
in repo-local Lean or pinned mathlib. This is intake discovery only, not an exhaustive anchor audit
or a global absence claim.
