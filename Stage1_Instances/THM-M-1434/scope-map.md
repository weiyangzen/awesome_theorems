# Scope map

## Received scope

The repository fixes the title `Sullivan无游荡域定理`, Dennis Sullivan, 1985, and only the gloss
`有理函数的无游荡域` ("no wandering domains for rational functions"). It supplies no
bibliography, definitions, ordered binders, hypotheses, conclusion, exception policy, proof, or
formal artifact. The metadata status `已验证` is untrusted under rev-5.6.

## Leading candidate family

Sullivan's 1985 Annals paper is the leading source candidate. A source-faithful statement is
expected to require decisions about all of the following:

- the complex Riemann sphere and a total self-map represented by a rational function;
- the exact degree or nonconstancy hypothesis on that rational map;
- iteration on the sphere, including poles and the point at infinity;
- the Fatou set defined through normality of the family of iterates in the spherical topology;
- connected components of the Fatou set and the induced forward action on those components; and
- eventual periodicity of every Fatou component, or an exactly equivalent no-wandering predicate.

These bullets delimit a candidate theorem family. They do not transcribe, select, or assert the
canonical root.

## Decisions required at statement freeze

1. Inspect an immutable copy of the primary paper and pinpoint its exact theorem, definitions,
   assumptions, conclusion, and proof boundary; check corrections and errata and obtain independent
   source review.
2. Fix whether the domain is the analytic Riemann sphere, complex projective line, or an explicitly
   proved equivalent one-point compactification of `Complex`.
3. Fix how a rational function becomes a total sphere-valued map, especially at finite poles and
   infinity, and state the exact degree/nonconstancy restriction.
4. Formalize normality of the iterate family and verify that the resulting Fatou set agrees with
   the selected source convention. Equicontinuity or local normality may not replace it without a
   checked theorem under all needed hypotheses.
5. Define a Fatou component and prove that its image lies in one well-defined Fatou component before
   using a component-level dynamical map.
6. Decide whether eventual periodicity is expressed as equality of pointwise set images, equality
   of containing connected components, or periodicity in a quotient/type of components.
7. Fix iteration indices and require a genuine positive period, such as witnesses `m < n`, rather
   than an equality made trivial by taking the same iterate twice.
8. Resolve constant and degree-one maps, empty or whole-sphere Fatou sets, components containing
   infinity, and period/minimal-period conventions.
9. Freeze checked transports for any negative "no wandering" formulation, preperiodicity
   formulation, or alternative sphere/component encoding that receives credit.

## Explicit exclusions

- A polynomial-only no-wandering theorem or a result for a selected family of rational maps.
- Julia-set invariance, density of periodic points, classification of periodic Fatou components,
  hyperbolicity, structural stability, or the Mandelbrot-set results neighboring this catalog item.
- An algebraic `RatFunc` theorem that does not supply a total analytic self-map of the Riemann
  sphere and the normal-family Fatou set.
- A result whose structure assumes the requested no-wandering or eventual-periodicity conclusion.
- Pairwise nonintersection of point orbits substituted for nonwandering of connected Fatou
  components.
- Generic connected-component, one-point-compactification, meromorphic, iterate, or periodic-point
  APIs presented as evidence for the complex-dynamics statement or proof.
- The catalog label `已验证`, the title of a famous paper, or a passing API probe treated as H0 or
  kernel closure.

No canonical Lean target is frozen at intake. The source lead is precise enough to guide the
dependent statement phase, but its public bibliography page alone cannot settle the proposition.
