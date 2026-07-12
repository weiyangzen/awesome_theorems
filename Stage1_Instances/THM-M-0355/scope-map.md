# Scope map

## Provisional included claim

- A source-specified Meyer construction on the real line, beginning with a smooth cutoff or
  frequency window satisfying the required transition and partition identities.
- The resulting mother wavelet, with the exact inverse-Fourier, phase, scalar, and normalization
  conventions chosen by the source.
- The claimed smoothness/decay and Fourier-support properties of that witness.
- The dyadic dilation and integer translation family, and the source's exact orthonormality and
  completeness assertion in real or complex `L^2(R)`.

This boundary is provisional. The repository phrase does not by itself establish that all four
components occur in the intended theorem.

## Decisions required at statement freeze

An immutable source passage must fix the cutoff formula and identities; `C^infinity`, Schwartz, or
other regularity; closed versus essential Fourier support and its numerical interval bounds; the
Fourier transform convention; real versus complex values; Lebesgue measure normalization; dilation
and translation order, signs, and factors; the index set; and whether the conclusion is an
orthonormal basis, a Parseval identity, dense span, a frame, or only construction of one function.

Boundary analysis must cover endpoints of frequency windows, values at zero, overlap of adjacent
dyadic bands, negative frequencies, integer scales, almost-everywhere representatives, and whether
the scaling function is part of the theorem. Checked transports are required for every credited
alternate convention.

## Explicit exclusions

- Haar, Shannon, Daubechies, Morlet, or an arbitrary smooth wavelet as a substitute.
- A generic smooth bump-function existence theorem without the Meyer partition identities.
- A compactly supported time-domain wavelet claim; the classical Meyer construction is instead
  frequency localized, but the exact selected source must set the boundary.
- Orthogonality without normalization and completeness, when the selected source asserts a basis.
- Existence of some abstract `HilbertBasis` without the explicit Meyer family.
- Higher-dimensional tensor products, wavelet packets, biorthogonal systems, frames, Besov-space
  characterizations, or multiresolution results not required by the exact source theorem.
- Treating the manifest label `已验证` or an API probe as human-source or kernel proof evidence.

No canonical Lean proposition is frozen at intake. The statement phase must not turn this
provisional family description into a convenient weaker theorem.
