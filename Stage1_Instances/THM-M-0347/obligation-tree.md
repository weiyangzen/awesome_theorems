# Frozen obligation tree

This is registry version 1 for `THM-M-0347`. It freezes the classical Fejer-kernel
approximate-identity architecture before proof work. All analytic nodes remain open unless explicitly
identified as a checked interface. Nothing here proves Fejer's theorem.

## M0347-ROOT

Exact target: uniform convergence, in the continuous-map topology, of the `n + 1` arithmetic means
of symmetric Fourier partial sums for every continuous complex-valued function on every positive-period
`AddCircle T`. The root requires the frozen statement interface and final assembly node.

## M0347-S-INTERFACE

The elaborated definitions in `Statement.lean` fix the frequencies `[-n,n]`, inclusion of `S_0`,
normalization by `n + 1`, arbitrary `T > 0`, and continuous-map convergence. This interface is checked,
but it gives no analytic proof.

## M0347-N-CONVOLUTION

Rewrite the finite Fourier/Cesaro expression as convolution with the period-dependent Fejer kernel.
This node owns all coefficient rearrangement, Haar normalization, sign, and scalar factors.

## M0347-C-KERNEL

Construct the finite Fejer kernel and prove its weighted Fourier-series and squared-geometric-sum
representations. These identities feed the convolution, positivity, mass, and concentration nodes.

## M0347-L-POSITIVITY

Derive pointwise nonnegativity from the squared representation, including the value at the identity.

## M0347-L-MASS

Integrate the finite Fourier representation using character orthogonality and prove normalized mass one.

## M0347-L-CONCENTRATION

For every neighborhood of zero, prove that the normalized kernel mass outside it tends to zero. The
denominator estimate away from zero and its uniformity are substantive parts of this node.

## M0347-L-UNIFORM-CONTINUITY

Use compactness of `AddCircle T` and continuity of `f` to make translations of `f` uniformly close
to `f` near the identity.

## M0347-L-ESTIMATE

Split the convolution error into a near and far region. Positivity and unit mass bound the near part
by uniform continuity; concentration and boundedness control the far part. Output the exact epsilon
sup-distance statement `UniformFejerEstimate`.

## M0347-T-ASSEMBLE

`root_of_uniformFejerEstimate` is a kernel-checked conditional composition from the exact epsilon
estimate to `FejerTheoremTarget`. Its estimate argument is deliberately open, so it provides no root
proof credit.

## M0347-X-SOURCE

Primary theorem passage, assumptions, normalization, and per-node transition mapping remain required.

## M0347-X-FOUNDATION

The transitive axiom, quotient, integration, imported-declaration, executable, and no-oracle audit remains
required for release.

## M0347-X-PROVENANCE

Terminal bodies and imports must be bound to immutable origins, dependency closures, licenses, and receipts.

## M0347-X-READABLE

A unique anchored reconstruction and independent review remain required; this architecture is not `R0`.

## M0347-X-WORKFLOW

Proof, validation, and release tasks remain ordered and independently receipted. Master acceptance is the
only authority that may promote this provisional obligation-tree phase.
