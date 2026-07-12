# Scope map

## Included topic boundary

- Boolean functions on finitely many input bits.
- A source-specified Boolean circuit syntax and semantics, including its gate basis and fan-in.
- A source-specified resource measure such as size or depth.
- A precise lower-bound proposition for a selected function or quantified family of functions.
- Uniformity, monotonicity, randomness, and asymptotic conventions only when required by that source.

## Ambiguities to resolve at statement freeze

The record does not decide among materially different results already named by the repository:

1. Shannon counting: most Boolean functions require circuits of exponential size.
2. `PARITY` is not computed by polynomial-size constant-depth `AC^0` circuit families.
3. Monotone circuits for `CLIQUE` require large size.
4. Modular or majority functions have lower bounds against classes such as `AC^0[q]`.
5. Another size, depth, formula, monotone, threshold, or bounded-fan-in lower bound.

Even after choosing a result, the source must fix the circuit grammar, semantics, gate basis,
fan-in, constants, size/depth measure, function family, uniformity, quantified parameters, and exact
bound. These choices are not definitionally interchangeable.

## Explicit exclusions

- Treating "circuit complexity" itself as a proposition.
- Replacing the unspecified lower bound with any convenient result from the repository's nearby
  list, including Shannon, Furst-Saxe-Sipser, Razborov, Smolensky, or Håstad.
- Proving merely that Boolean functions, finite circuits, or a complexity measure can be defined.
- Using graph-theoretic circuits, electrical circuits, arithmetic circuits, or proof circuits.
- Assuming an unrestricted circuit model, where arbitrary Boolean functions could be primitive
  gates and invalidate ordinary gate-count lower-bound readings.
- Crediting the metadata label `已验证` as human-source or machine-proof evidence.

No canonical Lean target is frozen at intake because no unique source proposition is available.
