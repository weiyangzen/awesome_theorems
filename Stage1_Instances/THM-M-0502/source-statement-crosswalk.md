# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` identifies A. Page, the year 1935, and the phrase "existence of
real zeros of L-functions." This is metadata-level discovery provenance. It omits the family of
characters, conductor bound, zero region, constant, quantifiers, and the standard at-most-one
conclusion, so it is not an exact mathematical statement and supplies no `H0` evidence.

## Primary and modern discovery anchors

- A. Page, "On the number of primes in an arithmetic progression," *Proceedings of the London
  Mathematical Society*, second series 39 (1935), 116-141,
  DOI `10.1112/plms/s2-39.1.116`. This is the historical primary-paper candidate. An archival copy,
  pinpoint theorem/page, exact notation, assumptions, and correction history have not yet been
  inspected in this dossier.
- H. Iwaniec and E. Kowalski, *Analytic Number Theory*, AMS Colloquium Publications 53 (2004), the
  discussion commonly indexed as the Landau-Page theorem. This is a modern statement candidate,
  not the primary historical source. Edition, proposition/page, constants, and errata remain to be
  pinned and reviewed.

These citations are discovery anchors only. Neither has an immutable source hash, premise-level
mapping, errata determination, or independent reviewer receipt.

## Crosswalk

| Repository/source component | Intended mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "L-functions" | Dirichlet L-functions attached to characters | `DirichletCharacter.LFunction` plus conductor-indexed character family | family narrowed; exact encoding open |
| "real zeros" | real `beta` with `L(beta, chi) = 0`, near 1 | real-to-complex coercion, equality to zero, interval predicate | included; endpoints open |
| Page theorem | uniform exceptional-zero uniqueness | finite/small cardinality or pairwise uniqueness statement | included; uniqueness unit open |
| conductor bound | primitive conductors uniformly bounded by `Q` | primitive predicate, conductor, bounded sigma type | required; API unverified |
| absolute constant | source constant defining the zero region | positive real constant and quantified threshold | required; exact quantifier order open |
| exceptional character | the sole possible member of the family | character identity modulo reviewed primitive representation | optional existence forbidden; refinements open |

## Existing Lean boundary

The pinned module `Mathlib.NumberTheory.LSeries.DirichletContinuation` defines the analytic
continuation `DirichletCharacter.LFunction`. The neighboring module
`Mathlib.NumberTheory.LSeries.Nonvanishing` proves nonvanishing on `re s >= 1`. The checked intake
probe establishes only that these declaration surfaces elaborate in this repository environment.
It does not establish a Page-theorem declaration, the required cross-modulus family, or any root
proof credit.

Before `H0`, a qualified reviewer must approve a pinpoint primary-source record with stable edition
or scan identity, theorem/page, every assumption and conclusion, notation translation, dependent
source results, and errata status. The source phrase must not be broadened into arbitrary
L-functions or weakened to a generic existence claim.
