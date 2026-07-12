# Scope map

| Surface | Included at intake | Boundary to resolve |
|---|---|---|
| Repository identity | `THM-M-0179`, differential geometry, Yau, 1978 | Distinct from the 1975 PDE duplicate `THM-M-1319` |
| Human claim | A lower-bound estimate for a first eigenvalue | Metadata does not determine a formula |
| Operator | An eigenvalue-bearing geometric operator is intended | Laplace-Beltrami or another operator; sign and scaling open |
| Spectral index | A "first eigenvalue" | Bottom versus first positive value; multiplicity convention open |
| Geometric setting | A differential-geometric space | Closed/noncompact/domain setting, dimension, boundary, and regularity open |
| Hypotheses | Geometric controls used by the selected source | Curvature, diameter, volume, connectedness, and normalization open |
| Conclusion | A numerical lower bound | Constant, strictness, dependence on inputs, and equality cases open |
| Lean surface | Lean 4 with repository-pinned mathlib | Module, definitions, binders, imports, and expression hash open |

## Explicit exclusions

- The 1975 PDE entry `THM-M-1319` is not merged into this target merely because its Chinese title
  and short gloss are nearly identical.
- The Li-Yau estimate, Zhong-Yang estimate, Cheng eigenvalue comparison, Yau conjecture, and the
  adjacent Cheng-Yau maximum principle are not substituted without a pinpoint source crosswalk.
- A generic real inequality, an assumed spectrum API, or strengthened hypotheses chosen only to
  make formalization convenient cannot stand in for the scheduled theorem.
- The metadata label `已验证` is discovery input and supplies neither human-source nor Lean credit.

The statement phase must first identify an immutable primary-source edition and freeze the exact
operator, geometric domain, ordered hypotheses, normalization, bound, and boundary cases. Until
then an honest canonical Lean expression cannot be selected.
