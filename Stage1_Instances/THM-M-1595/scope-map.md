# Scope map

## Preserved repository scope

The mathematical catalog fixes only `Polar码`, Erdal Arikan, 2009, and the gloss
`达到香农限的码`. A parallel computer-science Stage0 record says `达到容量的Polar码` and marks
the result merely `可验证`. Together these records identify Arikan's capacity-achieving polar-code
family, but they do not select one exact theorem or formalization.

The inspected 2009 primary paper narrows the family to binary-input discrete memoryless channels,
channel polarization, polar codes based on the Arikan transform, and successive-cancellation
decoding. That source lead does not authorize choosing one of its materially different theorem
roots on the catalog's behalf.

## Proposition-changing decisions

An approved statement run must select and crosswalk all of the following from an immutable,
independently reviewed source:

- an arbitrary binary-input discrete memoryless channel or the symmetric subclass;
- symmetric capacity under uniform input or Shannon capacity, and whether their equality for a
  symmetric channel is part of the target, an assumption, or a dependency;
- the binary input type, finite/countable/arbitrary discrete output alphabet, channel transition
  law, memorylessness, positivity, and normalization conventions;
- the `2 x 2` kernel, Kronecker power, bit-reversal convention, synthesized bit-channels, and
  whether the root is channel polarization or coding performance;
- block length `N = 2^n`, information set, frozen set and frozen values, encoder, polar-code
  selection rule, successive-cancellation decoder, and tie-breaking convention;
- code rate as `K/N`, `floor (N R)/N`, or a lower bound, together with the exact quantifier order
  over channel, target rate, block length, information/frozen sets, and error tolerance;
- block error versus bit error, average over frozen vectors versus fixed frozen values, average
  versus maximal message error, and any symmetry transport between these notions;
- the conclusion: fractions of near-perfect/near-useless synthesized channels, existence of good
  information sets, asymptotic vanishing error, a finite big-O rate, or encoder/decoder complexity;
- the exact asymptotic statement, including powers-of-two indexing, `R < I(W)`, constants hidden by
  big-O, an exponent such as the paper's `1/4`, or a later `beta < 1/2` refinement; and
- every boundary case and the foundation, computation, and cost-model profiles.

These choices change the proposition. They form a resolution ledger, not an asserted theorem.

## Candidate roots not credited

- Arikan 2009, Theorem 1: polarization of synthesized-channel symmetric capacities for any fixed
  threshold `delta`.
- Theorem 2: existence, for `R < I(W)`, of sufficiently many synthesized channels with small
  Bhattacharyya parameters.
- Theorem 3: the averaged block-error big-O bound for the paper's polar-coding rule on a B-DMC.
- Theorem 4: the fixed-frozen-vector block-error bound for symmetric B-DMCs; here symmetric
  capacity equals Shannon capacity.
- Theorem 5: `O(N log N)` encoding and successive-cancellation decoding complexity for the wider
  class of `G_N` coset codes.
- Later strengthened polarization exponents, nonbinary kernels, source polarization, list decoding,
  finite-length scaling, or construction algorithms.

No candidate is selected, conjoined, asserted, or credited at intake. In particular, a channel-
polarization theorem is not automatically the catalog's code theorem, and Theorem 5 does not claim
low-complexity construction of the information set.

## Neighbor and duplicate boundaries

- `THM-M-1579` separately owns channel capacity and `THM-M-1580` separately owns Shannon's noisy-
  channel coding theorem. Neither supplies an inherited definition, statement, or proof.
- `THM-M-1593` owns LDPC codes and `THM-M-1594` owns turbo codes. Their proximity to a channel
  limit is not evidence for this target.
- Stage0 record `THM-C-0386` repeats the polar-code family in a computer-science projection. It is
  outside the 1546-target rev-5.6 manifest and grants no shared state or proof credit.
- Generic PMFs, Markov kernels, binary entropy, Hamming distance, binary matrices, Kronecker
  products, or an assumed decoder-reliability structure are substrate rather than the requested
  capacity-achieving theorem.
- Simulation, floating-point density evolution, finite test vectors, or a decoder oracle cannot
  replace universal asymptotic proof.

## Boundary cases

The statement phase must decide empty or singleton output alphabets; invalid or zero-mass channel
rows; zero- and unit-capacity channels; deterministic, completely noisy, nonsymmetric, and symmetric
channels; `n = 0`, `N = 1`, and non-powers of two; `K = 0` and `K = N`; empty information or frozen
sets; `R < 0`, `R = 0`, `R = I(W)`, and `R > I(W)`; `I(W) = 0`; threshold endpoints; arbitrary
frozen bits; decoder ties; zero and unit error probabilities; logarithm base; and big-O constants
and indexing ranges.

## Formal boundary

No canonical Lean expression is frozen. At pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, the probe authenticates probability mass functions,
Markov kernels, binary entropy, Hamming distance, binary matrices, and Kronecker powers. A bounded
exact-topic search found no polar-code, channel-polarization, mutual-information, or channel-
capacity declaration in pinned mathlib or repository-local Lean. This is discovery evidence only,
not the exhaustive downstream anchor audit or proof of global absence.
