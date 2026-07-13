# Source-statement crosswalk

## Repository authority and provenance

`Docs/researches/math_theorems.md:1564-1569` is the sole repository source record. It supplies the
title "Klein model", attribution to Felix Klein, the year 1871, the complete gloss "a projective
model of hyperbolic geometry", high importance, and status `已验证` ("verified"). All six uncited
lines originate at repository commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record gives
no publication, edition, section, page, theorem, definitions, formula, quantifiers, hypotheses,
conclusion, proof, correction history, reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:6027-6052` repeats the gloss while explicitly leaving the formal system,
logical foundation, exact definitions and premises, proof route, dependencies, equivalent forms,
axioms, machine status, and artifact links open. Its generic claim that a closed result is believed
to exist is planning metadata, not evidence. The rev-5.6 manifest retains `已验证` only as
`source_status_untrusted` and resets this target to `L0 / rework_required`.

No immutable primary or authoritative external theorem passage is preserved in the repository, and
none is admitted by this intake. The source classification is therefore `H5`: the received record
is not a stable proposition. This neither refutes nor calls open any exact, source-selected theorem
about the Klein model. Ordinary theorem execution first requires redirection to an exact reviewed
proposition.

## Component crosswalk

| Repository phrase | Possible mathematical component | Prospective Lean component | Intake status |
|---|---|---|---|
| "Klein" | Klein or Beltrami-Klein disk/ball, or a historically specific projective construction | a source-frozen carrier and definitions | attribution and exact construction not sourced |
| "projective" | conic interior in real projective space, homogeneous coordinates, projective transformations, or cross-ratio invariance | `Projectivization`, linear/projective group actions, custom conic and chart predicates | generic pinned substrate probed; interpretation open |
| "hyperbolic geometry" | a synthetic hyperbolic plane, a metric space, a constant-curvature manifold, or another model | axiom structure, metric/Riemannian theorem, or checked comparison object | foundation and comparison object open |
| "model" | satisfaction of axioms, a metric construction, an equivalence/isometry, or a bundle of proved laws | a proposition relating the construction to the selected geometry | no conclusion supplied |
| common carrier | open unit disk in an affine chart or interior of a projective conic | `Complex.UnitDisc`, a real ball, or a custom projective subtype plus transports | not selected by the source |
| common distance | logarithm of a boundary-point cross ratio, with convention-dependent factor and order | a source-defined real-valued distance plus metric proof | no formula or cross-ratio convention supplied |
| common geodesics | intersections of projective lines with the interior, appearing as Euclidean chords | `Set.segment`/`Set.openSegment` plus projective-line and geodesic predicates | possible consequence, not present in the record |
| common symmetry | projective maps preserving the boundary conic act by isometries | `Matrix.ProjGenLinGroup` or another source-mapped action | group, action, and theorem open |
| `已验证` | untrusted inventory label | no proposition or proof object | explicitly rejected as H or M evidence |

## Candidate normalization not credited

A familiar modern presentation takes an open Euclidean ball, assigns the distance between two
interior points using the logarithm of the cross ratio with the two boundary intersections of their
line, and obtains straight chords as geodesics. Other presentations begin with a Lorentzian
quadratic form and project the hyperboloid model. Normalization, dimension, carrier, and theorem
bundle vary. These are source-search leads only; none is the canonical statement.

## Lean intake boundary

Pinned mathlib contains adjacent open-disk, convexity, segment, projectivization, projective-action,
and projective general-linear-group APIs. A bounded exact-topic search over repo-local Lean and
pinned mathlib found no Klein/Beltrami hyperbolic-model or cross-ratio declaration. A no-match result
does not establish global absence, and the adjacent APIs do not establish statement identity or
proof closure.

The statement phase must first preserve and hash an immutable primary or authoritative source,
transcribe every incorporated definition and the exact proposition, map each premise and conclusion,
inspect corrections and errata, reconcile neighboring model targets, and obtain independent review.
Only then may it minimize imports, elaborate and fingerprint a canonical Lean target, compile
credited transports, and run removed-hypothesis, changed-domain, binder-scope, and boundary-case
mutations. No H0, exact Lean statement, proof, audit completion, or theorem completion is claimed.
