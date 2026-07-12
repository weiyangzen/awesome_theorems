# Scope map

Target: `THM-M-0159` / item `S56-M-0159-INTAKE`.

## Included mathematical claim

- A smooth two-dimensional manifold `M` is smoothly immersed in oriented Euclidean `R^3`.
- The immersion induces a Riemannian metric `g` (the first fundamental form).
- A compatible local choice of unit normal determines the symmetric second fundamental form `h`.
- The Riemann curvature tensor of `g` satisfies the Gauss equation
  `R(X,Y,Z,W) = h(X,W) h(Y,Z) - h(X,Z) h(Y,W)`, subject to the selected curvature and
  second-form sign conventions.
- The Levi-Civita covariant derivative of `h` satisfies the Codazzi-Mainardi symmetry
  `(nabla_X h)(Y,Z) = (nabla_Y h)(X,Z)`.

This is a human-scope freeze, not a Lean statement. The displayed Gauss signs are provisional:
the statement phase must copy one inspected source's definitions and either adopt its convention or
supply a checked sign transport.

## Boundary and binder decisions

- The root is local where a unit normal is chosen, so it does not assume global orientability of the
  immersed surface. A globally oriented formulation is an alternate encoding.
- Immersions, including self-intersections, are intended; embeddings are not required.
- Connectedness, compactness, and boundarylessness are not mathematical prerequisites for the
  local equations and must not be added merely for convenience.
- Tangent-vector quantification, tensor slot order, curvature sign, shape-operator sign, regularity,
  universes, and treatment of manifolds with boundary must be frozen in the exact statement.
- Degenerate non-immersions and non-unit or incompatible normal fields are excluded.

## Explicit non-substitutions

- Gaussian curvature alone expressed as the product of principal curvatures;
- only the Gauss equation or only the Codazzi equation;
- the converse realization theorem for an abstract pair `(g,h)`;
- a structure carrying the two desired identities as fields;
- a coordinate calculation for one graph or parametrized patch without a checked transport to the
  invariant root;
- higher-codimension Gauss-Codazzi-Ricci or pseudo-Riemannian equations without specialization.

The later statement and obligation phases must separate induced geometry, normal choice, the Gauss
formula, tangential/normal projections, curvature comparison, and covariant-derivative symmetry.
This anticipated architecture carries no proof or coverage credit at intake.
