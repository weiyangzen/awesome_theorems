# Scope map

## Preserved catalog scope

The intake preserves target `THM-M-1388`, the title `特征值问题`, the gloss
`Sturm-Liouville特征值`, the attribution to multiple mathematicians, and the twentieth-century
date. Importance `high` and status `已验证` are catalog metadata, not human-source or kernel
evidence.

The title and gloss locate a Sturm-Liouville spectral family but do not identify one truth-valued
root. A later statement phase may select a proposition only from an immutable, independently
reviewed source passage and must preserve the neighboring target boundaries.

## Candidate interpretations not credited

1. A regular separated-boundary Sturm-Liouville problem has at least one eigenvalue.
2. Its eigenvalues are real, discrete, simple, bounded below, or countably infinite.
3. Its eigenvalues admit a strictly increasing enumeration tending to positive infinity.
4. Its normalized eigenfunctions form a complete orthonormal basis in a weighted function space.
5. The resulting eigenfunction series converges in a specified norm or uniformly under additional
   regularity.
6. A singular, periodic, coupled-boundary, matrix-valued, or operator-theoretic eigenvalue result.

These interpretations have different binders, assumptions, conclusions, exceptional cases, and
proof dependencies. None is selected, asserted, or credited at intake. In particular, their
conjunction must not be silently adopted merely because one modern textbook states several clauses
together.

## Proposition-changing decisions

Before the statement phase can close, an immutable source and independent review must fix:

- the exact numbered proposition or source-defined conjunction and its proof boundary;
- a finite regular interval versus a half-line, whole line, singular endpoint, periodic domain, or
  abstract Hilbert-space formulation;
- the scalar field and whether the coefficients and eigenfunctions are real- or complex-valued;
- the coefficient functions `p`, `q`, and weight `r` (often `w`), their regularity, integrability,
  positivity and nonvanishing assumptions, and equality-almost-everywhere conventions;
- the sign and normalization of the differential expression, including whether it is
  `-(p u')' + q u = lambda r u` or an equivalent weighted-operator form;
- the ambient weighted `L2` or continuous-function space, its measure and inner product, the
  unbounded-operator domain, and the exact derivative notion;
- separated Dirichlet, Neumann, Robin, mixed, periodic, antiperiodic, or coupled boundary
  conditions, including all endpoint parameters and self-adjointness restrictions;
- the definition of eigenvalue and eigenfunction, nonzero-vector condition, multiplicity
  convention, spectrum encoding, and treatment of zero;
- whether the conclusion is existence, reality, simplicity, discreteness, accumulation,
  enumeration, lower boundedness, completeness, convergence, or a checked conjunction;
- every ordered quantifier, universe and typeclass assumption, incorporated definition, edition,
  page, correction or errata, and source-to-clause mapping.

## Degenerate and boundary cases

The selected source must resolve an empty or reversed interval; coincident endpoints; zero-length
domains; zero, sign-changing, discontinuous, or singular `p` or weight; unbounded or complex
potential; regular versus singular endpoints; zero or repeated eigenvalues; empty, finite, or
two-sided spectra; multiplicity greater than one under coupled or periodic conditions; boundary
parameters whose equations are redundant or inconsistent; Dirichlet, Neumann, Robin, mixed,
periodic, and antiperiodic cases; zero eigenfunction exclusion and normalization; complex
eigenfunctions for a real problem; enumeration starting at zero or one; convergence topology; and
whether statements at spectral accumulation points are included.

## Neighbor and substitution exclusions

- `THM-M-1384` owns the broader Sturm-Liouville-theory target; a whole chapter or theory package
  cannot replace this spectral-problem label.
- `THM-M-1385`, `THM-M-1386`, and `THM-M-1387` own comparison, separation, and oscillation claims;
  zero-counting or interlacing cannot be silently adopted here.
- `THM-M-1389` owns the Weyl asymptotic formula, and `THM-M-1390` owns a min-max principle.
- A generic finite-dimensional eigenvalue theorem, compact-operator spectral theorem, Fredholm
  alternative, or Rayleigh-quotient extremum is supporting substrate, not a Sturm-Liouville result.
- A structure or hypothesis that stores the desired eigenvalue, basis, enumeration, compact
  resolvent, or spectral conclusion provides no proof.
- A constant-coefficient scalar example, finite-difference discretization, numerical eigensolver,
  floating-point spectrum, or plotted eigenfunction does not replace a source-selected theorem.
- The untrusted `已验证` label and discovery probe provide no source-fidelity or proof credit.

## Formal boundary

Pinned mathlib exposes generic derivative and ODE predicates, eigenvalues and eigenspaces,
symmetric and compact-operator spectral results, and finite-dimensional Rayleigh-quotient extrema.
The probe authenticates those adjacent interfaces only. It neither defines the source-selected
Sturm-Liouville operator and boundary conditions nor states or proves its spectral theorem.
