# Source-statement crosswalk

| Claim component | Human source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Identity of the item | `Docs/researches/math_theorems.md`, entry `等周不等式`: Paul Levy, 1951, "isoperimetric inequality for sets on the sphere" | none | Repo-local metadata identifies the spherical family but is not a primary mathematical source and does not specify a variant |
| Fixed-measure extremizer | Provisional classical Levy spherical-isoperimetry reading: a spherical cap is extremal | none | Frozen as intended scope, but edition/theorem/page and assumptions are not yet pinned: `H3` |
| Neighbourhood inequality | For equal-measure `A` and cap `C`, `mu(C_r) <= mu(A_r)` for each nonnegative radius | no declaration identified or inspected at intake | Canonical provisional root; exact open/closed neighbourhood and normalization choices remain statement obligations |
| Perimeter formulation | Spherical caps minimize boundary measure at fixed volume | none | Related classical formulation only; not substituted for the root and no equivalence is credited |
| Concentration formulation | Bounds for neighbourhoods of sets of measure at least one half, or for Lipschitz functions | none | Consequence/specialization only; explicitly outside root closure |

The local metadata's `verified` status is untrusted under rev-5.6 and supplies no `H0` or machine
credit. The attribution "Paul Levy, 1951" is also insufficient to select an immutable edition:
intake located no repository-held primary text, theorem number, page, assumptions list, or errata
record. Consequently this dossier does not pretend that the precise source wording has been
recovered.

The statement phase must resolve all of the following before an exact-statement receipt can exist:

1. Pin a primary edition and page/theorem for the neighbourhood form, plus relevant corrections.
2. Fix `S^n` versus a radius-scaled sphere, the dimension range, normalized measure, measurability,
   cap parameterization, and open/closed geodesic neighbourhood convention.
3. Inspect the actual pinned mathlib environment and choose a canonical Lean expression.
4. Elaborate it, serialize its normalized expression and environment fingerprint, and probe all
   boundary cases listed in `intake.json`.
5. Prove checked transports before crediting perimeter, complement, or concentration encodings.

No external URL or secondary summary is presented as immutable evidence, and no `H0`, `M0`, or
theorem-completion claim is made.
