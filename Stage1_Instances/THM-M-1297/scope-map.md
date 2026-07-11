# Scope map

## Included subject

- Interpolation between members of a Sobolev-type regularity scale.
- The catalog's explicit association with Besov and Triebel-Lizorkin spaces.
- Normed or quasi-normed function spaces, interpolation parameters, and the continuous embeddings
  or space identifications actually stated by the source eventually selected.

## Statement decisions still open

The source must determine whether interpolation is real or complex; whether the endpoints are
inhomogeneous or homogeneous Sobolev/Bessel-potential spaces; whether the result is an equality of
spaces with equivalent norms or only an embedding; and whether the intermediate space is Sobolev,
Besov, or Triebel-Lizorkin. It must also fix the ambient domain (`R^n`, a bounded domain, or another
space), scalar field, smoothness and integrability parameters, `q`, endpoint exclusions, negative
smoothness, and any extension-domain hypotheses.

## Explicit exclusions

- Choosing the familiar Hilbert-space log-convex norm inequality merely because it is easy to
  formalize.
- Replacing Besov/Triebel-Lizorkin interpolation with interpolation of finite-dimensional sequence
  norms or plain `L^p` spaces.
- Treating the catalog status "verified" as source or kernel evidence.
- Defining an abstract interpolation package with the desired conclusion as a field.

Degenerate and boundary cases (equal endpoint smoothness, interpolation parameter `0` or `1`,
infinite exponents, zero functions, and homogeneous-space quotient conventions) must be copied
from the selected theorem rather than silently generalized.
