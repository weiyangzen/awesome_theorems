# THM-M-0387 Scope Map

## Frozen claim candidate

The intake claim is Fermat's Last Theorem in its positive-integer form: for every natural exponent
`n > 2`, there are no positive integers `x`, `y`, and `z` satisfying
`x ^ n + y ^ n = z ^ n`. The planned Lean boundary uses nonzero naturals instead of positive
integers, with the intended candidate declaration `FermatLastTheorem`. Exact elaboration and every
transport remain statement-phase work; intake records the candidate without taking proof credit.

The binder order is exponent, then the three bases. The intended hypotheses are `2 < n` and
nonzeroness of all three bases. The intended conclusion is the inequality
`x ^ n + y ^ n != z ^ n`. The statement phase must resolve whether the pinned mathlib root is
presented as `n >= 3` rather than `2 < n` and bind the checked equivalence before acceptance.

## In scope

- The exact all-exponent root over positive integers/nonzero naturals, not only selected exponents.
- Fixed-exponent formulations used to decompose the root.
- Natural, integer, rational, and primitive/coprime encodings only after checked two-way transports.
- Boundary probes at exponents `0`, `1`, and `2`, which protect the `n > 2` scope but do not prove
  an FLT instance.
- The standard exponent reduction, the `n = 3` and `n = 4` branches, regular-prime results, and the
  remaining all-odd-prime Wiles/Taylor-Wiles and Frey/Ribet chain as downstream audit/proof work.
- Lean 4 kernel, pinned mathlib, and any separately pinned external package only under the rev-5.6
  foundation, provenance, trust, validation, and consumer-acceptance rules.

## Out of scope

- Replacing the root with only `n = 3`, `n = 4`, exponents divisible by `4`, a finite exponent
  interval, or regular primes.
- Treating the conditional theorem from all odd-prime cases to the root as an unconditional proof.
- Treating an integer, rational, primitive, or coprime version as the root without a checked return
  transport to the frozen claim.
- Positive characteristic, polynomial-ring, or other generalized FLT-like statements that do not
  specialize back to the exact natural-number root.
- Numerical searches, bounded verification, historical source labels, URLs, theorem names, or
  declarations with transitive proof gaps as proof evidence.
- Importing acceptance, receipts, checkbox state, or proof credit from `THM-M-0133` or any shared
  module group. Shared groups are weak discovery hints only.

## Intake boundary

This map fixes scope for `S56-M-0387-INTAKE`. It does not claim an accepted exact statement,
accepted transport, source fidelity `H0`, kernel proof, audit completion, or theorem completion.
