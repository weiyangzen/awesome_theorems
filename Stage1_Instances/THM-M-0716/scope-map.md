# Scope map

## Included topic boundary

- Primitive recursive total functions and partial recursive functions.
- A source-specified domain, codomain, arity convention, and partial-function representation.
- The exact source-specified relation or theorem involving those classes.
- The initial functions and closure operations needed by that theorem, including whether unbounded
  minimization is part of the conclusion or only a definition.

## Ambiguities to resolve at statement freeze

The repository record does not decide among these non-interchangeable readings:

1. Every primitive recursive function on natural numbers is partial recursive after coercion to a
   partial function.
2. Every primitive recursive function between `Primcodable` types is computable.
3. Partial recursive functions are the closure of primitive-recursion operations plus unbounded
   minimization.
4. Primitive recursive total functions form a proper subclass of total computable functions.
5. A coding or normal-form characterization of one or both classes.

The statement phase must inspect an immutable source and freeze one proposition, ordered binders,
exact definitions, hypotheses, conclusion, and treatment of divergence. It must also decide whether
"partial recursive" means a partial function class or the older use of "general recursive" for a
total function, and whether finite arities are encoded into unary functions.

## Explicit exclusions

- Selecting `Primrec.to_comp` merely because it is convenient and available in pinned mathlib.
- Replacing partial recursive functions with Turing-computable functions without a checked source
  crosswalk and equivalence transport.
- Replacing an inclusion claim with strictness, representation, closure, or decidability.
- Treating definitions of `Primrec`, `Partrec`, or `Computable` as the requested theorem.
- Packaging a desired relationship as a hypothesis and proving a tautological projection.
- Crediting the repository label `已验证` as human-source or machine-proof evidence.

No canonical Lean target is frozen at intake because the source record does not state a proposition.
