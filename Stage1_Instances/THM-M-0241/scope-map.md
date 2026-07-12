# Scope map

## Preserved source scope

The repository fixes only the label `黎曼-希尔伯特问题`, the gloss `单值群与微分方程`
("monodromy group and differential equations"), the attribution Bernhard Riemann/David Hilbert,
and the year 1900. This identifies the historical inverse-monodromy problem family. It does not
select an exact theorem, hypotheses, a bibliographic proof source, or a formal artifact.

The intake preserves this family boundary: prescribed finite-dimensional complex monodromy data
on the complement of finitely many points of the Riemann sphere, and a complex linear differential
system or connection intended to realize those data with controlled singularities. This is a
topic-level boundary, not an asserted existence theorem.

## Proposition-changing decisions

An approved statement run must fix all of the following from an immutable source:

- the ambient complex curve, singular set, treatment of infinity, basepoint, and rank;
- whether monodromy data are a fundamental-group representation, generators with relations, local
  conjugacy classes, or data modulo overall conjugacy;
- whether the object sought is a scalar equation, first-order matrix system, logarithmic or
  meromorphic flat connection, and whether its bundle must be holomorphically trivial;
- the exact meaning of regular singular and Fuchsian, including pole orders and behavior at infinity;
- whether the singular locus is fixed exactly or additional apparent singularities are allowed;
- reducibility, resonance, determinant, eigenvalue, or other restrictions on monodromy;
- equivalence up to basis change, gauge transformation, or vector-bundle isomorphism;
- whether the result is positive existence, a restricted theorem, a classification, an
  obstruction, or a counterexample to unrestricted existence; and
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

`THM-M-0242` separately catalogs Hilbert's twenty-first problem with the gloss "monodromy group of
Fuchsian equations." Its overlap is a future target-reconciliation issue, not permission to merge
IDs or transfer evidence. `THM-M-1559` separately catalogs an integrable-systems Riemann-Hilbert
problem; its legacy operator-valued contour jump interface is not the historical inverse-monodromy
statement and cannot substitute for this target.

The intake also excludes a convenient rank-one or irreducible special case chosen without a source,
an arbitrary contour factorization theorem, a definition packaged as an assumed realization, or
the catalog's untrusted `已验证` label as human or kernel evidence.

## Formal boundary

No canonical Lean expression is frozen. Pinned mathlib supplies `OnePoint ℂ`, fundamental groups,
matrix general linear groups, and hence a type for representations of a punctured sphere's
fundamental group. The intake probe checks that substrate only. It does not supply a holomorphic
vector bundle, regular-singular connection, Fuchsian system, monodromy construction for such an
object, realization relation, or theorem. A complete formal-anchor audit is downstream.
