# Scope map

## Preserved repository scope

The repository identifies the Cooley-Tukey fast-Fourier-transform family: compute a discrete
Fourier transform by exploiting a factorization of the transform length rather than evaluating the
dense DFT sum directly. This family description is preserved without selecting a proposition.

Candidate results that require separate source decisions include:

- the algebraic decomposition of a length-`N1 * N2` DFT into smaller DFTs, twiddle factors, and an
  explicit input/output permutation;
- correctness and termination of a radix-2 recursive algorithm for lengths `2^m`;
- a mixed-radix, decimation-in-time, or decimation-in-frequency program theorem;
- an exact count of complex additions and multiplications; and
- an asymptotic `O(N log N)` bound in a specified arithmetic or machine cost model.

None is the canonical target at intake.

## Decisions required at statement freeze

1. Admit and independently review an immutable source edition and select one exact result or
   algorithm specification, including every incorporated formula and proof boundary.
2. Fix the input/output carrier, usually complex-valued data, and whether indices use `Fin N`,
   `ZMod N`, arrays, lists, vectors, matrices, or another checked equivalent.
3. Fix the DFT exponential sign, primitive-root convention, normalization, transform direction,
   and equality orientation.
4. Fix the permitted lengths: arbitrary positive `N`, composite `N = N1 * N2`, powers of two, or a
   source-specific factorization tree, including the order and positivity of factors.
5. Fix the algorithm: decimation in time or frequency, recursion base, subtransform order, twiddle
   factors, index bijections, stride/layout, and in-place or out-of-place semantics.
6. Fix the correctness conclusion: pointwise equality with the dense DFT, an inverse theorem, a
   permutation-adjusted equality, termination, or their exact conjunction.
7. If speed is part of the root, define the operation cost model, which operations count, recurrence,
   exact or asymptotic bound, logarithm base, constants, input-size encoding, and machine model.
8. Freeze ordered binders, hypotheses, degenerate cases, foundation/TCB/computation profiles,
   minimal imports, expression/environment fingerprints, checked transports, and required
   mutations.

## Degenerate and boundary cases

Source review must decide `N = 0` and `N = 1`; empty and singleton inputs; factors equal to zero or
one; prime lengths; an empty factorization tree; non-power-of-two input to radix-2 code; repeated or
noncoprime factors; zero and constant signals; invalid array lengths; exponent overflow in an
implementation; normalization at inverse transform; permutation direction; and whether a stated
complex-operation count includes root generation, indexing, memory access, bit reversal, or only
arithmetic butterflies.

No case is excluded at intake. A structure or hypothesis that stores the desired DFT equality or
complexity result is circular rather than an FFT theorem.

## Neighbor and substitution exclusions

- `THM-M-0341` owns Fourier transform inversion, not fast DFT evaluation.
- `THM-M-0358` owns the Fourier multiplier theorem, not an FFT algorithm.
- `THM-M-1261` owns Fourier integral operators, a continuous analytic topic.
- The physics-catalog quantum Fourier transform `THM-P-1065` is outside this classical
  numerical-algorithm target and the rev-5.6 mathematical target set; a quantum circuit theorem
  cannot substitute for Cooley-Tukey FFT.
- `ZMod.dft`, its dense sum formula, DFT inversion, roots of unity, finite-character bases, and
  continuous Fourier transforms are mathematical substrate only.
- A fixed-size computation, benchmark, numerical residual, floating-point experiment, or program
  that is not connected to the mathematical DFT by a kernel-checked proof supplies no closure.
- The catalog's `已验证` label and this discovery probe supply no H or M credit.

## Formal boundary and handoff

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` defines `ZMod.dft` as a
linear equivalence, gives its dense sum formula in `ZMod.dft_apply` and `ZMod.dft_def`, and proves
the inversion identity `ZMod.dft_dft`. Finite additive characters and complex character bases are
also available. A bounded search found no FFT-named recursive algorithm, Cooley-Tukey
factorization, program-correctness bridge, or complexity theorem. This is intake discovery only,
not an exhaustive anchor audit or a global absence proof.

The statement phase must first replace the catalog method label with an accepted truth-valued
source proposition. Only later phases may freeze formal candidates, obligations, typed graphs,
proof bodies, composition, trust closure, or theorem completion.
