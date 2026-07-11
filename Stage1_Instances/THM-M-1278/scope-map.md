# Scope map

## Included claim

- The standard round unit sphere `S^2`, with its Riemannian area measure of total mass `4*pi`.
- A real-valued function `u` in the regularity class ultimately fixed by the primary source.
- The sharp inequality
  `log ((1/(4*pi)) * integral exp(u)) <= (1/(4*pi)) * integral u + (1/(16*pi)) * integral |grad u|^2`.
- Equality and sharpness are downstream scope only if the selected source theorem includes them.

## Statement-phase decisions

The primary text must fix whether the domain is smooth functions or a Sobolev space, whether the
inequality is first stated under zero mean, the exact area and Laplacian conventions, and whether
the exponential is `exp u` or an equivalent rescaled form. The formal encoding must also decide
the concrete sphere subtype/manifold, volume measure, weak versus classical gradient, integrability
hypotheses, and extended-real versus real-valued integrals.

## Explicit exclusions

- A generic Moser-Trudinger inequality with a non-sharp or unspecified constant.
- A Euclidean bounded-domain inequality substituted for the spherical theorem.
- Assuming the desired estimate as a hypothesis or structure field.
- An equality-case classification substituted for the inequality itself.
- Treating the metadata label `已验证` as machine or source evidence.
