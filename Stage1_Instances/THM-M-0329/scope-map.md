# Scope map

## Included working boundary

- A real Hilbert space, pending confirmation of the exact source's scalar convention.
- A bounded bilinear form and a quantitative coercivity hypothesis with a positive constant.
- A continuous linear right-hand-side functional, either explicit or represented by a Hilbert-space
  vector through Riesz representation.
- Existence and uniqueness of a representing solution, plus continuous dependence only when the
  selected source statement includes it.

## Decisions required at statement freeze

The repository gloss does not fix whether the form is real or complex, symmetric or nonsymmetric,
whether coercivity is `C * ‖u‖^2 ≤ B u u` or uses a real part, which argument contains the unknown,
or whether the right-hand side is a functional or a vector. It also does not distinguish a
pointwise `∃!` theorem from the stronger packaging as an isomorphism or continuous equivalence.
Those choices affect the exact proposition and cannot be inferred from the theorem name alone.

Boundary handling must cover the zero Hilbert space, zero functional/vector, strict positivity of
the coercivity constant, and the relationship between `‖u‖^2` and `‖u‖ * ‖u‖`. Any complex-space
version must state the sesquilinearity convention and use of `re (B u u)` explicitly.

## Explicit exclusions

- The Banach-Nečas-Babuška theorem, inf-sup conditions, or a PDE weak-solution theorem as a
  substitute for Lax-Milgram.
- A finite-dimensional linear-system theorem that drops completeness/coercivity structure.
- A symmetric-form-only theorem unless the selected source imposes symmetry.
- A complex formulation silently identified with the pinned real mathlib declaration.
- Treating a continuous equivalence as automatically crosswalked to a source-level functional
  `∃!` statement without checked Riesz and argument-orientation transports.
- The repository label `已验证` or the presence of a mathlib declaration as human-source evidence.

No canonical formal target is frozen during intake.
