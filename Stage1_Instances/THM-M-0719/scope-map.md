# Scope map

## Included discovery boundary

- Formal computation models and their input/output encodings.
- Resource measures such as time or space and the input-size convention used by the measure.
- Resource-bounded computation predicates and complexity classes.
- Simulation, composition, hierarchy, separation, reduction, or completeness results only if an
  immutable source is later selected that states that exact result.

These are candidate surfaces for source disambiguation, not parts of a frozen root theorem.

## Ambiguities blocking statement freeze

The repository record does not determine:

1. deterministic, nondeterministic, alternating, circuit, RAM, lambda-calculus, or another model;
2. time, space, randomness, queries, communication, circuit size/depth, or another resource;
3. worst-case, average-case, amortized, parameterized, or exact complexity;
4. exact bounds versus asymptotic classes, and the encoding-dependent input-size function;
5. a definition, invariance result, speedup theorem, hierarchy theorem, closure theorem, separation,
   reduction, completeness theorem, or lower bound;
6. the quantified languages/functions/machines and the actual conclusion.

These choices alter the domain, ordered binders, hypotheses, boundary cases, and conclusion. A
predicate saying that some supplied machine meets some supplied bound would not resolve which
mathematical theorem this target denotes.

## Explicit exclusions

- `THM-M-0720` (P versus NP), an explicitly open adjacent problem.
- `THM-M-0721` (NP-completeness), `THM-M-0722` (Karp's 21 problems), and the separately catalogued
  polynomial-hierarchy target as silent replacements.
- The existence of mathlib structures for time-bounded or polynomial-time computation as proof of
  an unspecified complexity-theory theorem.
- A hand-chosen identity-function example, tautological wrapper, definition-only artifact, assumed
  predicate, or weakened special case as the canonical root.
- The untrusted inventory label `verified` as evidence of human or kernel closure.

No domains, universes, quantifiers, hypotheses, conclusion, alternate encoding, or degenerate cases
are frozen because the source metadata supplies no proposition.

