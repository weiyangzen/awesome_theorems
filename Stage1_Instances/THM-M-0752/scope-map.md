# Scope map

## Preserved theorem family

The intake preserves the recursion-theoretic Turing-jump family. The catalog fixes the title
`跳跃算子`, Stephen Kleene/Emil Post, 1954, and the gloss `图灵度的跳跃`; it supplies no formula,
definition, theorem locator, premises, or conclusion. The wording points to an operation on Turing
degrees, but an operation by itself is not a proposition.

The conventional construction begins at set level. For an oracle set `A` and a fixed acceptable
numbering of oracle computations, its jump is the relativized diagonal halting set
`A' = {e | Phi_e^A(e) halts}`. One then seeks a well-defined degree map by assigning the degree of
`A'` to the degree of `A`. This description is a family locator, not a frozen target.

## Proposition candidates not credited

- **Definition and well-definedness:** equivalent representatives `A` and `B` have equivalent
  jumps, so the set-level construction descends to Turing degrees.
- **Relative halting theorem:** `A'` is computably enumerable relative to `A` but is not computable
  relative to `A`.
- **Strict increase:** the degree of `A` is strictly below the degree of `A'`.
- **Monotonicity:** `A <=_T B` implies `A' <=_T B'`.
- **Relative completeness/maximality:** every set computably enumerable relative to `A` is Turing
  reducible to `A'`.
- **Finite iteration:** repeated jumping produces a strictly increasing sequence of degrees.

These claims have different binders, dependencies, conclusions, and proof obligations. A statement
phase cannot combine them into a stronger package merely because a secondary source presents them
together.

## Decisions required at statement freeze

1. Pinpoint and independently review an immutable primary or authoritative theorem passage,
   incorporated definitions, proof boundary, corrections, and errata.
2. Choose exactly which proposition the catalog owns: well-definedness, relative noncomputability,
   strictness, monotonicity, relative completeness, a specified conjunction, or another
   source-selected claim.
3. Fix the object model: sets or predicates on natural numbers, total characteristic functions, or
   partial functions; and map it to mathlib's current partial-function Turing-degree encoding.
4. Fix an acceptable oracle-program numbering, universal evaluator, halting convention, diagonal
   input, and whether the jump is represented as a set, predicate, characteristic function, or
   partial function.
5. Specify Turing reducibility/equivalence and computable enumerability relative to an oracle,
   including all conversions required between set and partial-function formulations.
6. Freeze universes, ordered binders, hypotheses, conclusion, coercions, extensionality convention,
   and logical/foundation assumptions.
7. Decide the empty oracle, computable oracle, partial or undefined oracle values, malformed codes,
   choice of representative, and zero/finite iteration cases.
8. Separate the root from any dependency or consequence owned by the neighboring degree, join,
   inversion, hierarchy, or halting-problem targets.

## Neighbor boundaries

- `THM-M-0750` owns the Turing-degree topic; its definitions may be substrate, not proof of a jump
  property.
- `THM-M-0751` owns the supremum/join of Turing degrees, not the jump.
- `THM-M-0753` owns jump inversion/the image of the jump operator. Inversion cannot be substituted
  for definition, well-definedness, strictness, monotonicity, or completeness.
- `THM-M-0741` owns the halting problem. Its unrelativized diagonal argument may be a dependency,
  but does not prove the uniform oracle-relative result.
- `THM-M-0754` owns the arithmetical hierarchy. Finite jump iterations may characterize levels,
  but that hierarchy is not silently included here.

## Explicit exclusions

This target is not a programming-language control-flow jump, a dynamical jump process, the
Friedberg jump-inversion theorem, Post's problem, or the existence of incomparable degrees. A
definition that stores the desired properties, an assumed oracle-halting decider, a theorem about
only the empty oracle, or the untrusted `已验证` label cannot supply root proof credit.

## Formal boundary

At the pinned mathlib revision, `RecursiveIn`, `TuringReducible`, `TuringEquivalent`, and
`TuringDegree` provide adjacent vocabulary and order structure. The inspected computability modules
contain no Turing-jump construction or theorem. The probe records elaboration of this substrate
only. Exact imports, source-identical expression, environment and expression fingerprints,
alternate transports, semantic mutations, and candidate provenance belong to downstream phases.
