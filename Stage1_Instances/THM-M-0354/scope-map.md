# Scope map

## Provisional included claim

- The unit interval `[0,1]` with Lebesgue measure, represented by a source-compatible Lean model.
- The constant scaling function together with normalized Haar functions indexed by dyadic scale and
  translation.
- Pairwise orthonormality and completeness in the real or complex `L^2` space, expressed as one
  Hilbert/orthonormal basis claim or as orthonormality plus dense closed span.

## Decisions required at statement freeze

The exact source must fix real versus complex scalars; the subtype, restricted-measure, or supported
function model of `L^2[0,1]`; whether the constant function is a separate index; the ranges for scale
and translation; the factor `2^(j/2)`; half-open interval conventions; and whether completeness is
stated by expansion, Parseval, dense span, or a Hilbert basis. Checked transports are required for
alternate encodings.

Boundary analysis must include the scale-zero term, endpoints `0` and `1`, dyadic breakpoints,
almost-everywhere equivalence, and the empty translation range. Ordered binders and index types must
prevent invalid pairs `(j,k)` rather than silently assigning them zero functions.

## Explicit exclusions

- Haar systems on the real line, higher-dimensional cubes, or general measure spaces as substitutes.
- Merely proving orthogonality without normalized norms and completeness.
- Any abstract existence theorem for some orthonormal basis that does not identify Haar functions.
- Schauder or unconditional basis results in `L^p` for `p != 2`, wavelet convergence claims, and
  multiresolution-analysis packages beyond what the exact basis theorem requires.
- Treating endpoint changes as definitional equality instead of proving almost-everywhere equality.
- Treating the repository label `已验证` as source or kernel evidence.

No canonical Lean proposition is frozen at intake. General basis APIs do not close the theorem.
