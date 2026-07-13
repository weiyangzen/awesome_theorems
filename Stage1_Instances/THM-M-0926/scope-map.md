# Scope map

## Preserved identity family

`THM-M-0926` preserves the repository identity "Cassini's identity for Fibonacci numbers." The
recognizable conventional formula family is

```text
F_(n-1) * F_(n+1) - F_n^2 = (-1)^n.
```

This display records a scope candidate, not the canonical root. The catalog contains only the
identity name and the gloss "an identity of the Fibonacci sequence." Its importance and
`已验证` fields are metadata, not source or kernel evidence.

## Decisions required before statement freeze

1. Preserve and independently review one immutable primary or approved authoritative source with
   an exact formula, proof boundary, assumptions, attribution, corrections, and errata status.
2. Freeze the Fibonacci sequence definition and indexing convention: zero-based or one-based,
   natural indices only or an integer extension, and the value carrier and coercions.
3. Freeze the ordered index binder and its domain or lower-bound hypothesis. A predecessor formula
   over naturals needs a decision at zero; mathlib's pinned theorem instead quantifies over all
   integers and uses `Int.fib`.
4. Freeze equation orientation and sign convention. Common rearrangements and index shifts change
   whether the right side appears as `(-1)^n`, `(-1)^(n+1)`, or an equality with an added term.
5. Decide how an integer exponent is represented. The pinned theorem uses `(-1) ^ n.natAbs`, while
   the source candidate writes `(-1)^n` without fixing the domain.
6. Resolve `n = 0`, the first positive index, negative indices, and every zero-/one-based shift.
7. Check transports for every credited natural, integer, shifted, sign-reversed, or rearranged form
   and mutation-test the domain, binder scope, sign, and boundary cases.
8. Select foundation, accepted-axiom, TCB, computation, freshness, and reviewer profiles only after
   the exact target and minimal import surface are frozen.

## Candidate formulations not credited

- The usual positive- or natural-index formula
  `F_(n-1) * F_(n+1) - F_n^2 = (-1)^n` under a source-selected lower bound.
- Pinned mathlib's all-integer theorem
  `Int.fib_succ_mul_fib_pred_sub_fib_sq`, whose right side uses `n.natAbs`.
- The pinned natural-cast auxiliary with integer-valued Fibonacci terms and a natural exponent.
- The rearranged form `F_(n-1) * F_(n+1) = F_n^2 + (-1)^n`.
- Shifted forms such as `F_n * F_(n+2) - F_(n+1)^2 = (-1)^(n+1)`.
- The geometric dissection interpretation and the Catalan-identity generalization.

These are related candidates, not interchangeable roots at intake.

## Explicit exclusions

- `THM-M-0925` (the Fibonacci sequence), `THM-M-0924` (Lucas numbers), or `THM-M-0927` (Binet's
  formula) used as this target's root.
- Catalan's identity, d'Ocagne's identity, determinant identities, a matrix-power identity, or a
  finite table substituted for Cassini's identity.
- A recurrence structure, custom axiom, hypothesis, or definition that stores the desired
  conclusion and is then presented as an independent proof.
- Mathlib's theorem name, documentation, elaboration, or the catalog label treated as primary
  source fidelity or accepted theorem completion.

Statement review must close these choices before obligation-tree construction. Intake freezes no
canonical expression fingerprint, obligation registry, discovery protocol, graph, or proof state.
