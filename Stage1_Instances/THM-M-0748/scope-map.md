# Scope map

## Preserved theorem family

The repository identity is Post's problem, not the unrelated theorem sometimes called Post's
theorem. The intended classical family asks for an intermediate computably enumerable Turing
degree. A later statement phase may freeze a positive-existence proposition only after primary
source and solution-source review settles every material choice below.

Prospective mathematical components are:

- a set of natural numbers, or an approved equivalent partial-function representative;
- computable enumerability of that representative;
- noncomputability, equivalently strictness above the computable Turing degree;
- Turing-incompleteness among c.e. sets, equivalently strictness below the halting degree `0'`;
- an existential conclusion producing an intermediate c.e. Turing degree; and
- an explicit map from the question posed by Post to the positive solution theorem.

These components describe the source family only. They are not a frozen statement or proof plan.

## Decisions required at statement freeze

1. Inspect and preserve an immutable copy of Post's 1944 passage, with page, original terminology,
   domain, reducibility notion, question boundary, surrounding assumptions, and correction history.
2. Inspect independently the Friedberg and Muchnik solution sources and decide whether the
   canonical target is direct intermediate-degree existence or the stronger construction of two
   incomparable c.e. Turing degrees followed by checked consequences.
3. Fix the meaning of `degree`: Turing degree rather than many-one, truth-table, weak truth-table,
   enumeration, or another reducibility degree.
4. Fix `computable` and `complete` as the bottom c.e. Turing degree and the c.e.-complete halting
   degree `0'`, including representatives and all checked quotient transports.
5. Select the c.e. model: set/predicate enumeration, domain or range of a partial recursive
   function, characteristic-function oracle, or another source-mapped encoding.
6. Freeze ordered binders, hypotheses, strict-order expansion, set/function and degree/representative
   transports, extensionality, and universe/typeclass data.
7. Resolve boundary cases: empty and universal sets, constant partial functions, duplicate degree
   representatives, computable witnesses, complete witnesses, and incomparable-versus-intermediate
   consequences.
8. Set the accepted foundation and trust policies for classical logic, quotient reasoning, choice,
   computability coding, and any priority-construction infrastructure.

## Explicit exclusions

- `ComputablePred.computable_iff_re_compl_re`, which is called Post's theorem in mathlib comments
  but is not Post's problem.
- Merely defining Turing reducibility, Turing equivalence, or `TuringDegree`.
- An intermediate degree for an unspecified reducibility relation or without the c.e. restriction.
- An intermediate many-one degree furnished by simple sets.
- Existence of a noncomputable c.e. set without Turing-incompleteness.
- Existence of an incomplete degree without strict noncomputability.
- The Friedberg-Muchnik incomparability theorem used without checked implications to the selected
  direct existence statement.
- A structure or hypothesis that assumes the desired intermediate witness.
- A finite computation, search trace, experiment, generated assertion, or unchecked certificate.
- The catalog label `已解决`, a theorem name, citation, or API import used as H or M evidence.

No canonical Lean target, statement fingerprint, checked alternate encoding, obligation registry,
discovery protocol, proof state, audit completion, or theorem completion is frozen at intake.
