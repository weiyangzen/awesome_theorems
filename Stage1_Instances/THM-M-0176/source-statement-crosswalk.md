# Source-statement crosswalk

## Candidate sources

- Friedrich Hirzebruch, *Topological Methods in Algebraic Geometry*, 3rd enlarged edition,
  Springer, 1966, the Riemann-Roch theorem in the chapter on characteristic classes. This is the
  historically primary book candidate; an immutable scan, exact theorem/page, and errata check are
  still required.
- William Fulton, *Intersection Theory*, 2nd edition, Springer, 1998, Chapter 15 (Riemann-Roch).
  This is a secondary normalization/reference candidate, not a replacement for primary-source
  fidelity.

These are discovery anchors only. They do not establish `H0`, and bibliographic location must be
verified from a stable edition before statement acceptance.

## Crosswalk

| Repository/intended component | Source concept to verify | Lean-side obligation | Intake disposition |
|---|---|---|---|
| "higher-dimensional algebraic variety" | smooth projective complex variety | choose an algebraic or analytic object model with smoothness and properness | unresolved |
| Euler characteristic | alternating sum of finite-dimensional sheaf cohomology | define cohomology, finiteness, and integer-valued alternating sum | included, not encoded |
| vector bundle `E` | locally free sheaf/bundle of finite rank | select representation and checked equivalence if transported | unresolved |
| `ch(E)` | rational Chern character | characteristic-class API and normalization | unresolved |
| `td(T_X)` | Todd class of tangent bundle | tangent bundle and power-series characteristic class | unresolved |
| integral/top component | evaluation on fundamental class or pushforward to a point | grading, orientation/cycle class, and coefficient comparison | unresolved |

Before `H0`, a reviewer must record exact source wording, label/pages, definitions, assumptions,
coefficient conventions, and errata, then map every clause to the canonical claim. Before statement
acceptance, alternate Chow/cohomology encodings require checked transports rather than prose.
