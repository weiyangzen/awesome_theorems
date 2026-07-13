# Scope map

## Preserved repository scope

The repository fixes only target `THM-M-1582`, the title `Kolmogorov复杂度`, attribution to Andrey
Kolmogorov, the year 1963, and the gloss `对象的最小描述长度`. Importance `high` and status
`已验证` are catalog metadata, not human-source or kernel evidence.

This identifies the shortest-effective-description subject family. It does not identify a theorem.
The intake preserves that family without turning a definition, historical precursor, or neighboring
algorithmic-information result into an invented root proposition.

## Candidate roots not credited

1. Kolmogorov's 1965 optimal-description theorem: there is a partial recursive method `A` such
   that, for every partial recursive method `phi`, some constant `C_phi` satisfies
   `K_A(y | x) <= K_phi(y | x) + C_phi` for all objects `x` and `y`.
2. The invariance corollary that complexities induced by two optimal description methods differ by
   at most an additive constant independent of the described object and condition.
3. A bare definition of conditional or unconditional complexity as the minimum program length.
4. Noncomputability or upper-semicomputability of complexity for a fixed universal machine.
5. The incompressibility counting statement that most length-`n` strings have complexity near `n`.
6. A prefix-free, plain, monotone, process, resource-bounded, or machine-specific complexity
   theorem.

These have different logical forms and proof obligations. None is selected or asserted at intake.

## Proposition-changing decisions

An approved source correction and statement run must freeze:

- definition versus theorem, and the exact source theorem, page, incorporated definitions, proof
  boundary, translation, corrections, and errata;
- plain versus prefix-free or another complexity convention, and conditional versus unconditional
  complexity;
- Kolmogorov's numbered object domain, finite binary strings, natural numbers, syntax codes, or a
  typed family of encodable objects;
- program alphabet and length, pairing, encoding/decoding, description method, interpreter, and
  partiality semantics;
- partial recursive functions, a Turing-machine model, or another accepted computation model, plus
  the checked equivalence required for any alternate model;
- the optimality/universality condition and exact quantifier order over methods, objects, programs,
  and additive constants;
- whether constants may depend on a compiler, machine, encoding, or fixed condition, but not on the
  described object;
- equality, one-sided inequality, or absolute-difference conclusion and the natural-number
  subtraction/inequality convention; and
- all empty-program, empty-string, nonhalting, undefined-output, unrepresentable-object, duplicate-
  program, zero-length, and no-description boundary cases.

These choices change the proposition. They are a resolution ledger, not a theorem statement.

## Explicit exclusions

- `THM-M-1583` algorithmic information theory or `THM-M-1584` Chaitin's uncomputable number used
  as inherited scope or evidence.
- `THM-M-0715` computability theory, `THM-M-0716` recursive functions, `THM-M-0717` Turing
  machines, or `THM-M-0718` universal Turing machines presented as the target rather than substrate.
- Stage0-only `THM-C-0392` Kolmogorov complexity or `THM-C-0393` incompressibility treated as a
  second accepted Stage1 target or shared proof credit.
- A definitional equality proved by unfolding a locally chosen complexity definition.
- A structure or hypothesis that stores optimality, universality, the desired bound, or a shortest
  description as assumed data.
- Compression software, empirical compressed length, runtime measurements, random testing,
  numerical estimates, or the untrusted catalog label used as theorem evidence.

## Formal boundary

Pinned mathlib provides `Computability.Encoding`, `Computability.FinEncoding`, binary encodings of
natural numbers, `Nat.Partrec.Code`, its evaluator and universality theorem, and bundled finite
Turing-machine semantics. It does not thereby select a description language or define Kolmogorov
complexity. The bounded intake search found no terminal Kolmogorov-complexity declaration. Exact
target selection, model transports, proof-body discovery, and absence claims remain downstream.
