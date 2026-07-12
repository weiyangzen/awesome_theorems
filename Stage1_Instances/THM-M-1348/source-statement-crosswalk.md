# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:9831-9836` supplies exactly the title
`Poincare-Bendixson theorem`, attribution to Henri Poincare and Ivar Bendixson, the year 1901, the
gloss `二维系统的极限集` (`limit sets of two-dimensional systems`), importance "high," and status
`已验证`. Git history places this uncited record in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. It contains no source, definitions, binders,
hypotheses, conclusion, proof boundary, correction history, or formal artifact.

`Docs/Stage0_Blueprint.md:36669-36694` repeats the gloss while explicitly leaving the formal system,
foundation, exact definitions and premises, proof route, dependencies, alternate forms, axioms,
machine status, and artifact links open. The rev-5.6 target manifest retains `已验证` only as
untrusted source metadata and resets the target to `L0 / rework_required`.

The repository also contains a Chinese-title duplicate, `THM-M-1400`, in the dynamics category. Its
legacy Lean boundary and current dossier are discovery input only. They are neither source authority
for `THM-M-1348` nor shared proof or intake evidence.

## Inspected source lead

Gerald Teschl, *Ordinary Differential Equations and Dynamical Systems*, Graduate Studies in
Mathematics 140, American Mathematical Society, 2012, is an authoritative modern source lead. The
author-hosted preliminary edition and the official errata updated 2026-06-23 were inspected. Section
7.3 distinguishes at least two candidate roots:

- Lemma 7.13, printed page 222: if a nonempty compact forward or backward omega-limit set contains
  no fixed points, then it is a regular periodic orbit.
- Theorem 7.16, printed pages 223-224: for a `C1` vector field on an open subset of `R^2`, a
  nonempty compact connected omega-limit set with finitely many fixed points is either a fixed orbit,
  a regular periodic orbit, or finitely many fixed points together with nonclosed connecting orbits.

The official errata is mathematically material. For page 222 it says the printed proof of Lemma
7.13 only establishes containment of a regular periodic orbit; equality additionally uses Lemma
7.14 after deriving connectedness from compactness as in Lemma 6.6. It also says the explicit
connectedness assumption in Theorem 7.16 is superfluous. Thus even an exact-root selection must bind
the relevant erratum, not merely cite the printed theorem name.

The repository does not cite this text or select Lemma 7.13, Theorem 7.16, or another classical
variant. The inspected files remain external source leads rather than owned or accepted evidence;
their observed SHA-256 digests and locators are recorded in `intake-receipt.json`. No source is
accepted as `H0`, and independent source review remains open.

## Component crosswalk

| Catalog component | Source-family alternatives | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| "two-dimensional systems" | `C1` autonomous vector field on an open subset of `R^2`, or another planar flow model | `R x R`, `IsIntegralCurve`, `Flow R` | phase space, regularity, and solution model open |
| "limit sets" | forward or backward omega-limit of one orbit | `omegaLimit atTop` or `omegaLimit atBot` over a singleton | direction, nonemptiness, compactness, and derivation open |
| equilibrium condition | no fixed point, finitely many fixed points, or fixed-orbit branch | fixed for all flow times or a source-equivalent vector-field zero | materially different roots |
| periodic conclusion | equality with a regular nonconstant periodic orbit | positive real period and equality with a flow range; discrete `IsPeriodicPt` is only adjacent | period, regularity, and equality conventions open |
| generalized conclusion | fixed orbit, regular periodic orbit, or finite equilibrium/connection configuration | future typed orbit and alpha/omega-limit predicates | not represented by the legacy finite-vertex placeholder |
| `已验证` | untrusted inventory label | no Lean proposition or proof object | no H or M credit |

## Related wording and Lean boundary

`Docs/researches/physics_theorems.md:6332-6338` says that bounded orbits of two-dimensional
continuous dynamical systems tend to fixed points or periodic orbits. That record belongs to a
different, non-Stage1 target and uses ambiguous convergence wording; it cannot select this root.

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the discovery-only
probe checks integral-curve, real-flow, omega-limit, closedness, invariance, and discrete
periodic-point interfaces. A bounded exact-topic search found no terminal Poincare-Bendixson
declaration in mathlib. The repo-local exact-topic file
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_297.lean` belongs to `THM-M-1400`, labels its
object as a statement boundary, and expressly says it does not prove the theorem. These observations
are not the later immutable external anchor audit and do not establish global absence.

Before leaving `H1`, accountable reviewers must select an immutable source proposition, preserve
the exact edition and errata, transcribe every incorporated definition, ordered binder, hypothesis,
and conclusion, resolve the `THM-M-1400` duplicate boundary, and independently approve the mapping.
Only then may the statement phase freeze minimal imports, an elaborated expression, checked
transports, and the required removed-hypothesis, changed-domain, binder-scope, and boundary mutations.
