# THM-M-0490 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for Zhang's bounded-prime-gap theorem.
The repository catalog says only that there are infinitely many pairs of primes whose difference
is less than seventy million. The primary paper proves the sharper, source-identifying assertion

```text
lim inf as n tends to infinity of (p_(n+1) - p_n) < 7 * 10^7,
```

where `p_n` is the nth prime. Its Theorem 1 first proves an admissible-tuple result and then states
this consecutive-prime consequence. Thus "consecutive" and the strict inequality are material,
while the admissible-tuple theorem is a stronger proof source rather than a substitute root.

The intake preserves that published consequence as the intended theorem family, but does not
freeze a canonical statement. A later statement phase must independently review the source and
choose a precise equivalence between the paper's real-valued liminf notation and a Lean encoding,
such as infinitely often small gaps in the zero-indexed sequence `Nat.nth Nat.Prime`. It must also
fix the infinitude predicate, indexing, casts, subtraction, and boundary mutations. Choosing those
silently here would overstate the intake phase.

Pinned mathlib supplies prime enumeration and monotonicity APIs in
`Mathlib.NumberTheory.PrimeCounting`; a bounded search located no Zhang or bounded-gap theorem.
`IntakeProbe.lean` authenticates the adjacent APIs and elaborates a prospective proposition type.
It declares no theorem or proof and earns no proof credit.

The provisional vector is `[H1, M4, R4]`: the primary publication and exact published consequence
are identified, but source-to-catalog semantics, equivalent encodings, proof-node crosswalk,
correction status, and independent review remain open; no usable exact Lean proof artifact was
located; and no readable proof reconstruction exists. All six downstream phases remain open. This
self-tested worker proposal claims neither accepted state, audit completion, theorem completion,
nor master acceptance.
