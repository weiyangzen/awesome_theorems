# Source-statement crosswalk

## Catalog evidence

The Stage0 row names the target "Sobolev space interpolation" but gives the theorem content only as
"Besov spaces and Triebel-Lizorkin spaces." It contains no quantified statement or bibliographic
anchor. These phrases admit several inequivalent interpolation theorems, so source fidelity forbids
selecting one during intake.

## Candidate primary statement sources

- Joran Bergh and Jorgen Lofstrom, *Interpolation Spaces: An Introduction*, Springer, 1976. This
  is a candidate source for real/complex interpolation conventions and classical function-space
  examples; exact theorem/page and applicability to the catalog phrase remain unverified.
- Hans Triebel, *Theory of Function Spaces*, Birkhauser, 1983. This is a candidate source for
  interpolation identities among Sobolev/Bessel-potential, Besov, and Triebel-Lizorkin scales;
  exact edition, theorem/page, assumptions, and errata remain unverified.

These are discovery anchors only, not `H0` evidence.

## Crosswalk

| Catalog phrase | Mathematical decision required | Lean surface required | Intake status |
|---|---|---|---|
| Sobolev space interpolation | endpoints, functor, parameter, equality or embedding | concrete interpolation construction and Sobolev spaces | unresolved |
| Besov spaces | homogeneous/inhomogeneous definition and indices | concrete Besov-space encoding | unresolved |
| Triebel-Lizorkin spaces | definition, indices, endpoint restrictions | concrete Triebel-Lizorkin encoding | unresolved |
| "verified" | provenance of that assertion | kernel-checkable declaration and evidence | untrusted metadata |

Before statement acceptance, an independent reviewer must inspect a stable edition, freeze one
exact theorem and all definitions, check errata, and map every binder and hypothesis to Lean. A
repository and pinned-mathlib API search belongs to the later anchor-audit phase and receives no
credit here.
