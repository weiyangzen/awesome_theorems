# Scope map

## Preserved source scope

The repository fixes only the label `希尔伯特第21问题`, the gloss `Fuchs方程的单值群`
("monodromy group of Fuchsian equations"), David Hilbert, and the year 1900. Hilbert's published
Problem 21 identifies the family more fully: construct a linear differential equation of the
Fuchsian class with given singular points and prescribed monodromic group. This is a historical
problem statement, not by itself a source-selected, corrected theorem.

The intake preserves that family boundary: prescribed finite-dimensional complex monodromy data
on the complement of finitely many points of the Riemann sphere, and a complex linear differential
equation, system, or connection intended to realize those data with controlled singularities. It
does not assert unrestricted existence.

## Proposition-changing decisions

An approved statement run must fix all of the following from immutable sources:

- the ambient complex curve or sphere, singular set, treatment of infinity, basepoint, and rank;
- whether monodromy data are a fundamental-group representation, generators with relations, local
  conjugacy classes, or data modulo simultaneous conjugacy;
- whether the sought object is a scalar equation, first-order matrix system, or logarithmic or
  meromorphic flat connection, and whether the underlying bundle must be holomorphically trivial;
- the exact meanings of regular singularity and Fuchsian, including pole orders and infinity;
- whether the singular locus is fixed exactly or added apparent singularities are allowed;
- reducibility, resonance, determinant, eigenvalue, or other restrictions on monodromy;
- equivalence up to basis change, gauge transformation, or vector-bundle isomorphism;
- whether the result is positive existence, restricted existence, classification, obstruction, or
  counterexample to unrestricted existence; and
- uniqueness, moduli, boundary cases, and the complete order and scope of quantifiers.

These decisions alter the proposition and sometimes its truth value. They are a resolution
checklist, not a canonical claim.

## Candidate branches not credited

- Realization by a regular-singular logarithmic connection on some holomorphic vector bundle.
- Realization by a Fuchsian matrix system on the trivial bundle with exactly the prescribed poles.
- A positive theorem for irreducible or otherwise restricted representations.
- An obstruction or counterexample theorem for unrestricted trivial-bundle realization.

No branch is selected, asserted, or credited at intake.

## Explicit exclusions

`THM-M-0241` separately catalogs the Riemann-Hilbert problem with the gloss "monodromy group and
differential equations." The records substantially overlap; that is a future target-reconciliation
issue, not permission to merge IDs or transfer evidence. `THM-M-1559` separately catalogs an
integrable-systems Riemann-Hilbert problem; its legacy contour jump interface cannot substitute for
the historical inverse-monodromy target.

The intake also excludes a convenient rank-one or irreducible special case chosen without an
approved source, a covering-space monodromy theorem, an arbitrary contour factorization theorem, a
definition that assumes realization, or the catalog's untrusted `已验证` label as proof evidence.

## Formal boundary

No canonical Lean expression is frozen. Pinned mathlib supplies `OnePoint ℂ`, fundamental groups,
matrix general linear groups, and therefore a type for representations of a punctured sphere's
fundamental group. The intake probe checks that substrate only. It does not supply a Fuchsian
differential equation or system, a regular-singular connection, a monodromy construction for such
an object, a realization relation, or the target theorem. A complete formal-anchor audit is
downstream.
