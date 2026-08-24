# Full study — S5-CLM-00003691

## Frozen claim

The source asks for the exact anti-Ramsey number of the path graph on `k`
vertices for `n ≥ k ≥ 5`. With `ℓ = floor((k - 1)/2)` and parity correction
`ε`, the result is the maximum of a fixed quadratic branch and a branch linear
in `n`. The formal source wraps this formula in `answer(True) ↔ ...` and leaves
the provider theorem sorry-backed.

The worker package does not claim a new combinatorial derivation of that deep
formula. Its claim-owned equivalent makes the formula itself a premise over an
arbitrary polymorphic graph invariant, then proves exact forward and reverse
transport between the source let-form and an expanded form. This isolates the
complete logical work supported by the frozen statement without laundering the
provider's `sorryAx` into proof authority.

## Preservation inventory

- Inputs: natural `k,n`, a polymorphic graph invariant, and the exact formula.
- Hypotheses: `5 ≤ k`, `k ≤ n`; neither is weakened or dropped.
- Graph: precisely `SimpleGraph.pathGraph k`.
- First output branch: `(k - 2).choose 2 + 1`.
- Second output branch: `(ℓ - 1).choose 2 + (ℓ - 1) * (n - ℓ + 1) + ε`.
- Exceptional arithmetic: all subtraction and division remain natural-number
  operations, including truncation; no ring or integer reinterpretation occurs.
- Parity: `ε = 1` exactly when `Odd k`, otherwise `2`.
- Output: equality to the maximum of exactly those two branches.

## Proof and composition

Zeta reduction is the sole semantic conversion. Forward proof specializes the
premise; reverse proof introduces the same binders. Their composition is the
root biconditional. The DAG separately represents source binding, conversion,
both implications, composition, mutation resistance, and cold audit replay.

## Provenance and trust

The exact member record, source locator, declaration/type/file hashes, provider
revision, and Stage6 alias are recorded. The numeric module name is frozen
provenance rather than a parseable canonical import. Every active import is
`Mathlib`; no provider body is invoked. There are no allowed claim-specific
axioms or bodyless foundation declarations in the frozen foundation profile.

Worker validation is deliberately `--no-lean`. Consequently all elaborated
expression and transitive constant values in the handoff are recomputation
commitments: Master must replace confidence in self-attestation with integrated
trust-zero elaboration and exact dependency/body/type/source/revision hashing.

## Readability and downstream use

Every required proof node maps injectively to one fragment below, and every
fragment maps back to exactly one node. The release can support the Stage6 alias
only after Master confirms the same integrated bytes, exact root, empty H/M/R
cuts, current trace, mutations, and cold replay. No extra theorem completion is
claimed for the provider formula or any alias.
