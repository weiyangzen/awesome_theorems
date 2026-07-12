# Scope map

## Included topic boundary

- Finite Boolean inputs encoding graphs or another source-selected combinatorial object.
- A source-selected family of monotone Boolean functions, plausibly the CLIQUE functions.
- Monotone circuits over a precisely specified positive gate basis.
- A precise circuit resource measure and a quantified lower bound in a frozen parameter regime.
- The combinatorial approximation lemmas and probability/counting estimates required by the source.

## Ambiguities to resolve at statement freeze

The repository record does not decide among materially different claims:

1. Razborov's 1985 lower bound for a parameterized CLIQUE function.
2. A later strengthened exponential monotone-size lower bound for CLIQUE.
3. A lower bound for a different monotone Boolean function or for monotone circuit depth.
4. A concrete finite inequality versus an asymptotic family statement.

The statement phase must freeze the input index type (edges of an `n`-vertex graph or another
encoding), clique predicate and clique parameter, accepted AND/OR fan-in, whether constants and
DAG sharing are allowed, circuit size, the exact lower-bound function, thresholds on parameters,
and the order of all quantifiers. It must distinguish a circuit computing the function exactly from
one-sided approximation.

## Explicit exclusions

- General unrestricted Boolean-circuit lower bounds as a substitute.
- Monotonicity of the CLIQUE property alone; it is not a circuit-size lower bound.
- AC0 depth lower bounds, monotone depth lower bounds, formula lower bounds, communication
  complexity, or proof-complexity lower bounds unless the primary statement explicitly says so.
- Later Alon-Boppana or other strengthened bounds silently attributed to the 1985 result.
- An abstract `Monotone` function assumed together with its desired lower bound.
- The labels `已验证` or "Razborov lower bound" as proof or exact-statement evidence.

No canonical Lean target is frozen at intake because the repository evidence does not determine
the proposition and pinned mathlib does not supply the required circuit-complexity interface.
