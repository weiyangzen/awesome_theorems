# THM-M-0221 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the Cauchy integral theorem. The
repository records Augustin Cauchy, the year 1825, and only the gloss "the integral of a
holomorphic function along a closed curve is zero." Its catalog label `已验证` ("verified") is
untrusted inventory metadata under rev-5.6 and supplies no source or Lean proof credit.

The gloss identifies a classical theorem family but is not a true binder-complete proposition. For
example, `f z = 1 / z` is holomorphic on `Complex \ {0}`, while its integral around the positively
oriented unit circle is `2 * pi * I`, not zero. A correct theorem therefore needs a condition such
as filled-region containment, a simply connected domain, null-homotopy, or a zero-index cycle.
The catalog selects none of these, and it also leaves the curve regularity, integral convention,
codomain, boundary behavior, and Cauchy-versus-Goursat formulation open. Intake does not silently
repair the source by choosing a convenient restricted theorem.

An inspected modern source lead confirms this ambiguity rather than resolving it: Stein and
Shakarchi first state the theorem loosely using a closed curve whose interior lies in the
holomorphy domain, then develop triangle, disk, circle, and toy-contour versions and defer the
general curve form. This source is not cited by the catalog and has not received the required
immutable source admission, complete assumption and errata audit, or independent review.

Pinned mathlib has strong restricted candidates. It proves Cauchy-Goursat zero-integral results
for rectangle boundaries and circles/disks, provides primitive infrastructure, and provides
curve-integral invariance under suitably smooth homotopies of closed one-forms. These declarations
show formal feasibility, but none is admitted as the exact root of the underspecified catalog
claim. `IntakeProbe.lean` authenticates the interfaces and their current axiom reports only.

The provisional vector is `[H1, M3, R4]`: a complete classical theorem family and modern source
lead are known; pinned formal theorem candidates exist; but the source-exact proposition,
source-to-Lean transport, and readable proof reconstruction are not accepted.

`instance.json` is the structured scope authority. `scope-map.md` and
`source-statement-crosswalk.md` freeze the admissible family, counterexample, and substitution
boundary. `task-dag.json` keeps all six downstream phases open. No H0, M0, R0, accepted execution
state, audit completion, theorem completion, or master acceptance is claimed.
