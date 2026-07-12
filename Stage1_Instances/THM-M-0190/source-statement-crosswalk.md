# Source-statement crosswalk

## Available repository record

`Docs/researches/math_theorems.md` gives the name, attribution to Elwin Christoffel, year 1865,
the phrase `凸体表面预定曲率问题`, importance `高`, and the untrusted status `已验证`.
`Docs/Stage0_Blueprint.md` repeats those fields but supplies no definitions, source edition,
theorem number, page, hypotheses, proof, formal declaration, or errata record. The metadata status
therefore receives no human-proof or machine-proof credit.

## Crosswalk

| Source element | Information fixed | Information still required for an exact target | Intake result |
|---|---|---|---|
| "Christoffel problem" | names a classical convex-geometry problem family | exact smooth, weak, and dimensional variant | unresolved |
| Elwin Christoffel / 1865 | historical attribution and year | exact passage, mathematical translation, later solution theorem, errata | unresolved |
| "convex-body surface" | convex geometry is the intended domain | body class, ambient dimension, full-dimensionality, regularity | unresolved |
| "prescribed curvature" | some curvature-derived datum is prescribed | first area measure versus principal-radius function and its normalization | unresolved |
| `已验证` | secondary repository label only | inspectable proof source and kernel receipt | no credit |

## Primary historical locator

E. B. Christoffel, "Ueber die Bestimmung der Gestalt einer krummen Oberflaeche durch lokale
Messungen auf derselben," *Journal fuer die reine und angewandte Mathematik* 64 (1865), 193-209,
DOI `10.1515/crll.1865.64.193`.

This bibliographic record matches the repository attribution and date, but intake has not audited
the original German text passage by passage and does not claim that a modern existence-and-
uniqueness theorem appears there in its current form. The DOI is a discovery locator, not an
immutable source receipt.

## Modern formulation locators

- W. J. Firey, "The determination of convex bodies from their mean radius of curvature
  functions," *Mathematika* 14 (1967), 1-13, DOI `10.1112/S0025579300007956`.
- W. J. Firey, "Christoffel's problem for general convex bodies," *Mathematika* 15 (1968), 7-21,
  DOI `10.1112/S0025579300002321`.

These titles distinguish smooth mean-radius data from a general-convex-body formulation and are
candidates for the later source audit. They are not yet theorem/page crosswalks, immutable copies,
or accepted `H0` evidence.

## Lean boundary

No exact Lean candidate has been selected. A repository and pinned-mathlib text search at intake
found no occurrence of `Christoffel`, `Christoffel problem`, `first area measure`, or `mean radius`
in the Lean source trees searched. This negative text search is not a complete anchor audit and
does not rule out lower-level convex or measure infrastructure.

The statement phase must choose an exact source theorem first, map every domain, quantifier,
compatibility hypothesis, conclusion, and translation quotient to Lean, and mutation-test the
result. Only then may an anchor audit assign formal proof credit.
