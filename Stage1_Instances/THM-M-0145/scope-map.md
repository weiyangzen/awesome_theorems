# Scope map

## Included subject

- Algebraic cubic surfaces and a rationality-related conclusion attributed to Yuri Manin.
- The ground field, smoothness/geometric-integrality assumptions, and meaning of rationality must
  be taken verbatim from the selected primary theorem.

## Decisions required before statement freeze

- Identify the 1963 work, edition, theorem/page, original language, and any corrections.
- Decide whether the actual conclusion is rationality or unirationality, and whether a rational
  point, rational line, or another configuration is assumed.
- Freeze whether rationality is over the base field, after extension, or geometric rationality.
- Freeze characteristic/perfectness hypotheses and all exceptional/degenerate cases.
- Map schemes, projective space, smoothness, cubic hypersurfaces, and rational maps to concrete
  mathlib APIs; record an explicit API blocker where absent.

## Exclusions

- Replacing a cubic surface theorem by a theorem about cubic curves or higher-dimensional cubics.
- Treating unirationality as rationality, or geometric rationality as rationality over the base.
- Encoding the desired conclusion as an assumed field of a structure.
- Using the repository's untrusted `已验证` label as source or kernel evidence.

