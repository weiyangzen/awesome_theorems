# THM-M-0895 source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:6551-6556` supplies exactly the Chinese title `strongly regular
graphs`, Raj Chandra Bose, 1963, the gloss `parameter constraints of strongly regular graphs`, high
importance, and status `verified`. Git history places all six uncited fields in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.

`Docs/Stage0_Blueprint.md:24413-24438` repeats that gloss while leaving the target formal system,
foundation, exact definitions and premises, proof route, dependencies, equivalent forms, axiom
policy, machine status, and artifact links open. The rev-5.6 manifest preserves `verified` only as
untrusted metadata and resets the target to `L0 / rework_required`.

The plural phrase "parameter constraints" has no parameter list, quantifiers, hypotheses, or
conclusion. It does not distinguish a counting identity from spectral, integrality, complement,
partial-geometry, or feasibility-bound results.

## Primary-source lead

Publisher and Crossref metadata identify Raj Chandra Bose, *Strongly regular graphs, partial
geometries and partially balanced designs*, *Pacific Journal of Mathematics* **13**(2), 389-419
(1963), DOI `10.2140/pjm.1963.13.389`. The publisher landing page gives the title, sole author,
date, pagination, DOI, and links a public PDF. This is an exact bibliographic match to the catalog
attribution and year.

A complete 3,289,073-byte, 35-page publisher PDF was inspected from temporary storage; its observed
SHA-256 is `2d73e39655a2f2b1ba3827e901a20fe40521fa0e4118db856b530451b37be614`.
Section 2, printed pages 393-395, defines a finite strongly regular graph using degree `n1`, number
of nonneighbors `n2`, and constant common-neighbor counts. Equation (2.1) gives
`n1 + n2 = v - 1`; equations (2.3)-(2.5) give further relations; and the text says the graph
parameters are connected by (2.1)-(2.5), of which only four are linearly independent. One relation
translates in modern notation to `k(k-lambda-1) = (v-k-1)mu`: combine (2.3),
`p^1_12 = n1 - p^1_11 - 1`, with the first balance equality in (2.5),
`n1 p^1_12 = n2 p^2_11`, and (2.1), `n2 = v - 1 - n1`. Later sections give distinct
partial-geometry parameter and integrality constraints.

This inspection sharpens rather than removes the ambiguity. The catalog has no citation and does
not say whether its plural phrase selects all of (2.1)-(2.5), only the modern feasibility equation,
a later geometry-specific theorem, another standard constraint, or a conjunction. The PDF remains
outside the repository, and no exact root admission, complete definition and proof-node crosswalk,
correction or errata audit, or independent review exists. The source status is therefore H1.

## Component crosswalk

| Repository or candidate element | Material meaning | Prospective pinned Lean surface | Intake assessment |
|---|---|---|---|
| strongly regular graph | finite regular graph with constant common-neighbor counts on adjacent and distinct nonadjacent vertex pairs | `SimpleGraph.IsSRGWith n k l mu` | close representation; nontriviality conventions differ and source mapping is open |
| parameters | usually vertex count, degree, adjacent common-neighbor count, and nonadjacent common-neighbor count | ordered naturals `(n,k,l,mu)` | order and source notation not frozen |
| parameter constraints | counting equation, matrix relation, spectral restrictions, multiplicity integrality, bounds, or specialized geometry/design relations | several different declarations or future statements | canonical conclusion absent |
| positive order | at least one vertex | `0 < n` | explicit premise of pinned `param_eq`; source status unresolved |
| feasibility equation | `k(k-lambda-1) = (v-k-1)mu` | `SimpleGraph.IsSRGWith.param_eq` | highly plausible candidate only |
| adjacency identity | length-two walk counts expressed by adjacency matrices | `SimpleGraph.IsSRGWith.matrix_eq` | different conclusion from scalar feasibility equation |
| complement parameters | transformation under graph complementation | `SimpleGraph.IsSRGWith.compl` | related theorem, not automatically part of the root |
| `verified` | untrusted inventory label | no declaration or proof object | no H/M credit |

## Lean discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the module
`Mathlib.Combinatorics.SimpleGraph.StronglyRegular` defines `IsSRGWith` and contains the close
declarations `param_eq`, `matrix_eq`, and `compl`. `IntakeProbe.lean` checks those interfaces plus
the empty and complete graph boundary theorems under the pinned toolchain.

The `param_eq` interface is:

```text
(h : G.IsSRGWith n k l mu) -> (hn : 0 < n) ->
  k * (k - l - 1) = (n - k - 1) * mu
```

This exact interface confirms that one plausible formal candidate exists; it does not establish
that the catalog intended this equation rather than the other candidate constraints. Intake has
not performed the downstream terminal proof-body, axiom, provenance, or exhaustive anchor audit,
so it assigns no M0 proof credit.

## Required source admission

Before statement acceptance, accountable reviewers must preserve a lawful immutable source,
select one exact proposition or explicit conjunction and locator, and crosswalk every definition,
domain, ordered binder, hypothesis, conclusion, arithmetic convention, degenerate case, proof
boundary, correction, and erratum. The statement phase may then elaborate precisely that claim,
record expression and environment fingerprints, compile every credited transport, and execute all
required mutation classes. Choosing the already available `param_eq` first and treating it as the
source would reverse this required direction of authority.
