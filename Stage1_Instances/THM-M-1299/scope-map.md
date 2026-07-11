# Scope map

## Included subject

- Besov spaces with all ambient domain, scalar field, smoothness `s`, integrability indices `p` and
  `q`, and homogeneous versus inhomogeneous convention made explicit.
- A theorem that does mathematical work, such as an embedding, extension, trace, interpolation, or
  equivalence between two independently defined Besov norms.
- Boundary and degenerate regimes (`p` or `q` infinite, negative smoothness, quotient by
  polynomials, and domain regularity) only when the selected source theorem includes them.

## Statement-phase decisions

The next phase must select one exact theorem from an inspected primary source. It must then freeze
the ambient domain (`R^n`, torus, or a specified domain), real or complex scalars, distributions or
functions, dyadic decomposition or difference-quotient definition, index ranges, equality versus
continuous embedding, constants, and endpoint cases. These choices are mathematically material and
cannot be inferred from the name "Besov spaces."

## Explicit exclusions

- Treating the definition or nonemptiness of a structure called `BesovSpace` as the target theorem.
- Substituting a Sobolev, Holder, Triebel-Lizorkin, or generic normed-space theorem.
- Choosing a convenient embedding without a source crosswalk.
- Assuming a Littlewood-Paley decomposition, extension operator, or norm equivalence as a field of
  an abstract package and then crediting projection from that package as proof.

The formal target remains intentionally unset until the source-selection blocker is resolved.
