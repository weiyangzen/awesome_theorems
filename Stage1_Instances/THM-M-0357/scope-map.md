# Scope map

## Provisional included boundary

- The Hilbert space `L^2(Real)` (with scalar and Haar/Lebesgue measure conventions selected from
  the source).
- An integer-indexed family of closed subspaces `V_j` with nesting.
- Compatibility of adjacent scales with dyadic dilation and integer translation invariance at the
  reference scale.
- Density of the union of `V_j` and triviality of their intersection.
- A scaling function whose integer translates form an orthonormal basis or Riesz basis for `V_0`,
  only if that is an assumption or conclusion of the selected theorem.
- Detail spaces `W_j` and a mother wavelet whose dyadic translates/dilates form a complete
  orthonormal basis, only if selected by the exact source.

## Decisions required at statement freeze

The exact source must decide whether the target is a definition/axiomatization, the construction
of an MRA from a scaling function, the existence of a wavelet from an MRA, or the basis theorem.
It must also freeze real versus complex scalars, `L^2(Real)` measure normalization, whether
`V_j \subseteq V_{j+1}` or the reverse indexing is used, the signs and square-root factors in
translation/dilation, orthonormal versus Riesz bases, the topology used for union density and
intersection, and all regularity, Fourier, refinement-filter, or quadrature-mirror hypotheses.

Boundary cases include the zero and top subspaces, constant families, zero scaling functions,
almost-everywhere representatives, negative scales, nonseparable ambient spaces, and failures of
density or trivial intersection.

## Explicit exclusions

- Haar, Meyer, or Daubechies wavelet construction alone as a substitute; these are adjacent,
  separately scheduled targets.
- A generic Hilbert-space orthogonal decomposition without dyadic translation/dilation content.
- Continuous wavelet transforms, frames, filter banks, or signal-processing algorithms unless the
  selected source theorem explicitly states them.
- A structure that assumes the requested basis or decomposition as a field and then projects it.
- The repository label `已验证` as source fidelity or kernel proof evidence.

No canonical Lean target is frozen at intake because the source record does not select one of the
materially different claims above.
