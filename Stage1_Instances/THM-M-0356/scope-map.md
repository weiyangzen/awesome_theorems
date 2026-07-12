# Scope map

## Provisional included claim

- A mother wavelet on the real line, with the source-selected real or complex scalar field.
- Compact support in the source-selected pointwise, essential, or topological-support sense.
- Integer translates and dyadic dilates, with the exact normalization fixed from a source.
- Orthonormality and completeness of that family in the selected `L^2(R)` model.
- If the source claim is the parameterized Daubechies construction, the exact filter-length,
  vanishing-moment, and regularity parameters and their bounds.

## Decisions required at statement freeze

An immutable source passage must decide whether the theorem is existential or supplies an explicit
filter family; whether it asserts one wavelet or one for every admissible order; the scalar field;
the `L^2` and almost-everywhere model; the dilation convention (`2^(j/2)` versus its inverse under
the alternate argument convention); and whether "orthogonal wavelet" includes normalization and
completeness. It must distinguish compact support of a representative from essential support of an
`L^2` class.

Boundary analysis must cover the lowest admissible order, zero or invalid filter lengths, negative
dilation indices, endpoints of support, equality almost everywhere, and any claimed number of
vanishing moments or regularity exponent. Ordered binders must prevent parameter side conditions
from being hidden in a conveniently chosen witness.

## Explicit exclusions

- Haar wavelets, Meyer wavelets, arbitrary abstract Hilbert bases, or generic compactly supported
  functions as substitutes for the Daubechies construction.
- A finite orthogonal filter without the refinement equation, quadrature-mirror conditions, and
  the checked route to an `L^2` wavelet basis required by the selected source.
- Orthogonality without unit norms and completeness, or compact support without the wavelet-basis
  conclusion.
- Biorthogonal, frame, multidimensional, lifting-scheme, and boundary-adapted interval wavelets
  unless the exact source explicitly selects them.
- Treating the repository label `已验证` as human-source or kernel evidence.

No canonical Lean proposition is frozen at intake. General analysis APIs do not close the theorem.
