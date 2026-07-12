# Scope map

## Intended mathematical boundary

- Languages over a source-selected finite alphabet with an explicit encoding and input-length
  convention.
- `IP`: languages accepted by an interactive protocol between an unbounded prover and a
  probabilistic polynomial-time verifier, with source-aligned round, randomness, completeness,
  soundness, and uniformity conventions.
- `PSPACE`: languages decided by a deterministic polynomial-space machine under a source-aligned
  machine, halting, work-tape, and polynomial-bound convention.
- Both inclusions needed for equality. The routine simulation `IP subseteq PSPACE` and the deep
  arithmetization/sum-check direction `PSPACE subseteq IP` must remain separately visible.

This boundary identifies the theorem family, not an exact Lean proposition.

## Decisions required before statement freeze

The statement phase must independently inspect an immutable primary edition and fix:

1. whether `IP` uses private coins and polynomially many rounds, and how messages and verifier
   configurations are encoded;
2. whether completeness/soundness use fixed constants, strict inequalities, negligible error, or
   a parameterized gap, plus the amplification bridge;
3. the quantifier order over languages, inputs, prover strategies, verifier randomness, and
   polynomial bounds;
4. whether provers are functions of transcript histories and whether verifier/prover behavior is
   total on malformed transcripts;
5. the deterministic machine and measured-space convention defining `PSPACE`;
6. whether class equality is represented as equality of sets of languages or two inclusions, with
   checked transports between any alternate definitions.

Public-coin protocols, perfect completeness, different error constants, alternating polynomial
time, quantified Boolean formulas, and particular complete problems may support the proof only
through explicit equivalence or reduction obligations.

## Explicit exclusions

- `IP subseteq PSPACE`, `PSPACE subseteq IP`, or a single PSPACE-complete language as a substitute
  for the equality root.
- `AM`, `MIP`, `PCP`, Fiat-Shamir, zero knowledge, or the existence/definition of interactive
  proofs as replacement theorems.
- A protocol structure carrying completeness, soundness, or the equality as assumed fields.
- A finite toy protocol, an assumed class equivalence, a definitional tautology, or a weakened
  special case as the canonical claim.
- The manifest's untrusted `verified` label or the existence of generic computability APIs as
  human-source or kernel evidence.

No Lean declaration is selected at intake. Missing pinned interactive-proof and polynomial-space
interfaces must be recorded as implementation work, not bypassed by broadening the theorem.
