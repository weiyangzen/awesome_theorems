# Scope map

## Included topic boundary

- Boolean functions on finitely many input bits.
- A source-specified Boolean circuit syntax and semantics, including gate basis and fan-in.
- A precise depth measure and any accompanying size bound.
- A source-selected function or function family and an exact depth lower-bound proposition.
- Uniformity, monotonicity, randomness, and asymptotic conventions only when required by that source.

## Ambiguities to resolve at statement freeze

The repository record does not choose among materially different readings:

1. `PARITY` cannot be computed by polynomial-size constant-depth `AC^0` circuit families.
2. A bounded-fan-in circuit computing a function such as parity needs logarithmic depth.
3. A size-depth tradeoff for a named function under a specified gate basis.
4. A depth-hierarchy or lower-bound result for formulas, monotone circuits, threshold circuits, or
   another restricted class.

Even after a result is chosen, the source must fix circuit grammar, semantics, constants, gate
basis, fan-in, size accounting, depth convention, uniformity, function family, quantified
parameters, and the exact inequality. These choices are not interchangeable.

## Explicit exclusions

- Treating "depth-bounded circuits" or "circuit depth lower bounds" as a proposition.
- Selecting a convenient `AC^0`, bounded-fan-in, monotone, formula, or threshold result without a
  checked source crosswalk.
- Substituting a circuit-size lower bound for a depth lower bound.
- Proving only that finite Boolean functions or a depth measure can be defined.
- Graph-theoretic circuits, electrical circuits, arithmetic circuits, and proof circuits.
- An unrestricted gate basis in which the target Boolean function can be a primitive gate.
- Crediting the metadata label `已验证` as human-source or machine-proof evidence.

No canonical Lean target is frozen at intake because no unique source proposition is available.
