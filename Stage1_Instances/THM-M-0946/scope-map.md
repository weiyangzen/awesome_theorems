# Scope map

## Preserved theorem family

The intake preserves the catalog title, Green/Tao/Ziegler attribution, year 2006, and the subject
of solutions to systems of linear equations in primes. It does not silently equate that sparse
record with one remembered theorem.

The closest 2006 source lead is Green and Tao's *Linear Equations in Primes*. Its published version
contains a conditional main theorem for systems of affine-linear forms of finite complexity,
Corollary 1.7 for complexity at most two, Theorem 1.8 for matrix equations in prime variables, and
Corollary 1.9 for qualitative existence. Later work of Green, Tao, and Ziegler proves the general
inverse-Gowers input that helps make the finite-complexity result unconditional. These are related
but not statement-identical roots.

## Decisions required at statement freeze

1. Select the exact immutable source edition and root: the conditional 2006 theorem, its
   complexity-at-most-two corollary, Theorem 1.8, Corollary 1.9, or a later unconditional theorem
   assembled from Green-Tao and Green-Tao-Ziegler results.
2. Fix whether the input is a tuple of affine-linear forms or an integer matrix equation, including
   the coefficient domain, dimensions, ranks, and all boundedness and nondegeneracy conditions.
3. Define finite/Cauchy-Schwarz complexity, affine dependence, and the distinction between finite-
   complexity systems and binary or infinite-complexity problems.
4. Fix the convex set or cone, scaling box, lattice-point convention, positivity condition, and
   whether boundary points or repeated parametrizations are counted.
5. Fix prime versus prime-power weights, the integer-domain convention for the von Mangoldt
   function, local factors, singular product, archimedean density, normalization, and convergence.
6. Fix the exact asymptotic regime, uniform parameters, error term, qualitative-versus-quantitative
   conclusion, and whether a zero local factor makes the claim vacuous.
7. Decide whether inverse Gowers-norm and Mobius-nilsequence statements are hypotheses, proved
   dependencies, or outside the selected root, and audit the later source revisions and errata.
8. Freeze ordered binders, coercions, universes, hypotheses, conclusion, alternate encodings,
   checked transports, foundation/TCB/computation profiles, and every boundary case.

These choices change the proposition or proof boundary. Intake leaves them open.

## Boundary cases to resolve

- zero dimensions or no forms, constant forms, duplicate forms, and rationally or affinely
  dependent pairs;
- rank-deficient matrices, inconsistent `Ax = b`, empty convex bodies, lower-dimensional bodies,
  open versus closed boundaries, and repeated parametrizations;
- negative, zero, one, prime-power, and prime values of the forms, including the source convention
  that the von Mangoldt weight vanishes on nonpositive integers;
- local obstructions and zero singular products, divergent or conditionally interpreted products,
  and normalization of local averages;
- fixed versus growing coefficient bounds and system dimensions, uniform versus pointwise error
  terms, and the order in which parameters and the scale tend to infinity; and
- complexity zero, one, two, arbitrary finite complexity, and infinite-complexity binary systems.

No boundary case is excluded before a proposition is selected.

## Explicit non-substitutions

- `THM-M-0945`, the Green-Tao theorem on arbitrarily long arithmetic progressions in the primes.
- The full Hardy-Littlewood/Dickson prime-tuples conjecture, twin primes, Goldbach, or any other
  infinite-complexity binary problem.
- One fixed affine-linear system, one progression length, or one matrix selected as the general
  theorem without a source-approved specialization decision.
- Corollary 1.7's unconditional complexity-at-most-two statement presented as the later arbitrary
  finite-complexity conclusion.
- The conditional 2006 main theorem with its GI/MN premises silently removed, or the later theorem
  with those proved dependencies added as root hypotheses.
- Generic prime-counting, von Mangoldt, affine-map, primes-in-progressions, Gowers-norm, or
  nilsequence infrastructure alone.
- A finite computation, numerical asymptotic experiment, URL, catalog label, or the discovery
  probe as statement or proof evidence.

## Prospective proof boundary

A later audit may need separate nodes for source definitions, affine-linear reductions, the
`W`-trick, sieve majorants, generalized von Neumann estimates, inverse Gowers theorems, Mobius-
nilsequence orthogonality, local factors, and conversion from weighted asymptotics to prime counts.
That list is only a discovery seed. No obligation registry, graph, composition certificate, or
closure credit is frozen at intake.
