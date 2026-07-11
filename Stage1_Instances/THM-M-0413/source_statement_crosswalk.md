# Source-statement crosswalk

| Claim component | Human source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| A number field has a Dedekind ring of integers | J. Neukirch, *Algebraic Number Theory*, Springer, 1999, Chapter I, section 6 (Dedekind domains and rings of integers), candidate primary textbook anchor | A proposition shaped as `IsDedekindDomain (NumberField.RingOfIntegers K)` | The repository's one-line claim agrees with the standard theorem, but edition-page/theorem pinpointing and errata review are not accepted: `H1` |
| Number-field domain | Same source: finite extensions of `Q` | A characteristic-zero field with finite-dimensional `Q`-algebra structure | Binder order and the canonical mathlib abstraction remain unverified |
| Ring of integers | Same source: algebraic integers in `K`, equivalently integral closure of `Z` in `K` | `NumberField.RingOfIntegers K` or an integral-closure construction | Identifier and definitional equality are candidates only |
| Dedekind conclusion | Same source's Dedekind-domain characterization | `IsDedekindDomain` typeclass/predicate family | Exact namespace, parameters, and instance/theorem form require lookup in a pinned mathlib checkout |
| Degree-one boundary | Specialization `K = Q`, whose ring of integers is `Z` | A later mutation/boundary test | In scope, but no checked specialization is credited |

The source record at `Docs/researches/math_theorems.md` supplies only the Chinese sentence
“数域的整数环是 Dedekind 整环,” an attribution to Richard Dedekind, the year 1871, and an untrusted
formalization label. It supplies no proof, bibliographic edition, theorem number, assumptions, or
formal artifact. The modern English statement above is a faithful scope normalization, not an
accepted source audit.

No `H0` or machine-closure claim is made. The statement phase must inspect the actual pinned
declaration type, serialize its normalized expression, and mutation-test the number-field
finiteness, base field, integral-closure object, and full Dedekind conclusion. The anchor-audit
phase must then locate exact mathlib declarations and immutable source revisions and check their
terminal bodies, axioms, placeholders, and dependency feasibility.

Discovery bibliography (not an immutable evidence receipt):

- J. Neukirch, *Algebraic Number Theory*, translated by N. Schappacher, Springer, 1999,
  DOI `10.1007/978-3-662-03983-0`.
