# THM-M-1468 scope map

## Catalog scope preserved

- Target identity: `THM-M-1468`, named `hp有限元` (hp finite elements).
- Catalog attribution and date: Barna Szabo and Ivo Babuska, 1986.
- Literal gloss: `h-细化和p-升阶` (h-refinement and p-enrichment/degree elevation).
- Recognizable topic boundary: a finite-element approximation strategy combining geometric mesh
  refinement (`h`) with increased local polynomial degree (`p`).

This is all the repository fixes. A method and two mechanisms do not assert a unique conclusion.

## Decisions required before statement freeze

An accountable source correction must select one immutable proposition and freeze:

1. The exact primary or authoritative edition, theorem/page, incorporated definitions, proof
   boundary, corrections, catalog-identity rationale, and independent review.
2. The PDE or approximation problem, spatial dimension, scalar field, domain and boundary
   decomposition, boundary conditions, solution notion, coefficients, and data.
3. The continuous variational problem, trial and test spaces, norms and seminorms, form, load,
   continuity/coercivity/inf-sup assumptions, and any consistency or regularity hypotheses.
4. The cells and reference elements; conforming or nonconforming assembly; mesh-size convention;
   refinement relation; nestedness; shape regularity; quasiuniformity or grading; and admissible
   hanging-node or anisotropic behavior.
5. The elementwise or global polynomial-degree function; degree convention; enrichment relation;
   conformity across interfaces; lower and upper bounds on `p`; and the rule coupling `h` and `p`.
6. Whether the root concludes density, best approximation, discrete solvability, quasi-optimality,
   an a priori error estimate, algebraic or exponential convergence, complexity, reliability of an
   adaptive choice, or an explicitly sourced conjunction.
7. Every constant and dependency, the error and regularity norms, asymptotic index, exact rate,
   quantifier order, alternate encoding, foundation profile, and exact-versus-numerical boundary.

These choices change the truth conditions and proof architecture. They are a resolution checklist,
not a canonical statement.

## Boundary and degenerate cases

Statement review must decide empty or zero-dimensional domains; zero forcing; incompatible mixed
boundary data; degenerate, inverted, empty, or disconnected meshes; zero mesh diameter; fixed
meshes; no-op refinements; `p = 0`; nonpositive or unbounded degree assignments; enrichment without
nested spaces; vanishing coercivity or regularity constants; exact representability; corner or edge
singularities; nonsmooth data; and denominators or logarithms at endpoint parameter values.

## Candidate theorem families not credited

- An hp best-approximation or interpolation estimate for a specified Sobolev class.
- A quasi-optimal Galerkin error bound combined with an hp approximation estimate.
- Algebraic convergence on quasiuniform meshes with uniform degree.
- Exponential convergence on geometrically graded meshes for analytic or weighted-analytic data.
- A singular-solution estimate near polygonal corners.
- Convergence or optimality of an adaptive hp-refinement algorithm.

The catalog does not choose among them. No candidate is the canonical root at intake.

## Explicit exclusions

- Generic finite-element, Galerkin, Lax-Milgram, projection, or polynomial-space facts cannot
  replace a source-selected hp-FEM result.
- An h-only convergence theorem, p-only approximation theorem, or spectral-element theorem cannot
  stand for the combined hp claim.
- `THM-M-1461` (finite-element method), `THM-M-1462` (Galerkin), `THM-M-1467` (spectral elements),
  `THM-M-1469` (adaptive FEM), and `THM-M-1470`/`1471` (error estimates) are separate catalog roots
  and confer no statement or proof credit.
- Mesh generation, degree bookkeeping, numerical experiments, or a structure storing the desired
  estimate as a field is not a theorem proof.
- The catalog value `已验证`, a source-title match, or a successful API probe gives no H or M credit.

## Formal boundary

No canonical Lean expression is frozen. Pinned mathlib provides coercive variational solvability,
Hilbert-space best approximation, and nested univariate polynomial degree submodules, but it does
not thereby define finite-element meshes or prove an hp error theorem. The bounded discovery search
is not an exhaustive downstream anchor audit or a global absence claim.
