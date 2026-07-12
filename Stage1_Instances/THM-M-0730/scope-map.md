# Scope map

## Included topic boundary

- Dinur's combinatorial, gap-amplification route to the PCP theorem.
- Finite constraint graphs or equivalent finite CSP instances, their assignments, and their value.
- The transformation parameters actually quantified by the selected theorem: size blowup, degree,
  alphabet, completeness, soundness/gap, randomness, and query complexity.
- A uniform effective construction when the source conclusion is an algorithmic transformation.

## Ambiguities to resolve at statement freeze

The repository record does not select among materially different roots:

1. A gap-amplification lemma transforming a constraint graph of small unsatisfied fraction into
   one with a constant gap while controlling size, degree, and alphabet.
2. A bounded-degree or regular constraint-graph normal form used inside that amplification proof.
3. The resulting PCP theorem, commonly expressed through `NP` and a verifier with logarithmic
   randomness and constant queries, with exact completeness and soundness conventions.
4. A corollary such as hardness of approximating a particular constraint problem.

The statement phase must inspect an immutable edition of the intended article and select one
numbered proposition. It must freeze whether constraints are directed or undirected, whether loops
or parallel constraints occur, how value and size are normalized, the alphabet convention, all
constants and asymptotic quantifiers, encoding/effectivity requirements, and the precise PCP class
notation if that is the root.

## Explicit exclusions

- The ordinary PCP theorem as a substitute merely because Dinur's argument proves it.
- Post's correspondence problem, which shares the acronym PCP but is unrelated.
- A prose claim that a proof is "combinatorial" without a quantified mathematical conclusion.
- A graph-expansion theorem, expander construction, or powering lemma alone unless the selected
  source explicitly makes it the repository root.
- An assumed structure containing the desired amplifier or verifier as data.
- The repository label `已验证` as human-proof or machine-proof evidence.

No canonical Lean target is frozen during intake.

