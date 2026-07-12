# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` identifies the entry as "Handle decomposition theorem" and gives
only "handle decomposition of manifolds" as its statement. `Docs/Stage0_Blueprint.md` repeats that
phrase. The metadata label `已验证` is untrusted by rev-5.6 and supplies none of the compactness,
smoothness, boundary, finiteness, or reconstruction conventions needed for an exact proposition.

## Candidate mathematical sources

- John Milnor, *Morse Theory*, Annals of Mathematics Studies 51, Princeton University Press
  (1963), the chapter on handlebodies. This is the principal candidate for the local bridge from a
  nondegenerate critical point to a handle attachment. Exact theorem/page, hypotheses, printing,
  and errata have not yet been inspected in this run.
- Yukio Matsumoto, *An Introduction to Morse Theory*, Translations of Mathematical Monographs 208,
  American Mathematical Society (2002), the handle-decomposition chapters. This is a modern source
  candidate for the global compact-manifold statement. Exact theorem/page and conventions remain
  to be inspected.
- Antoni A. Kosinski, *Differential Manifolds*, Pure and Applied Mathematics 138, Academic Press
  (1993), the handlebody chapter. This is a candidate independent exposition, not yet pinpointed.

These bibliography records are discovery anchors only. They do not establish `H0`; the next phase
must select a stable edition, inspect the exact result and definitions, check errata, and obtain an
independent review.

## Crosswalk

| Repository phrase | Frozen interpretation | Source fact required | Required Lean object | Intake status |
|---|---|---|---|---|
| "manifold" | compact finite-dimensional smooth manifold | category and countability hypotheses | concrete smooth manifold and compactness instances | included; boundary model open |
| "handle" | `D^k x D^(n-k)` attached on `S^(k-1) x D^(n-k)` | smoothing/corner and collar conventions | disks, attaching embedding, boundary/corner data | mathematical shape frozen; API open |
| "decomposition" | finite ordered attachment filtration | initial object, order, and reconstruction equivalence | finite indexed filtration plus checked reconstruction | included; exact encoding open |
| existence | every object in the selected class has such data | global Morse-function/exhaustion hypotheses | existential theorem with no certificate field assumed | included |
| boundary | source-selected closed or relative version | incoming/outgoing boundary convention | boundary faces and relative diffeomorphism | unresolved hard statement choice |

## Lean discovery boundary

The pinned mathlib tree contains general smooth-manifold infrastructure, which is confirmed only by
the narrow elaboration smoke check in `IntakeCheck.lean`. A repository search performed during this
intake found no declaration named or documented as a handle decomposition, handlebody theorem,
Morse function, or Morse handle-attachment theorem. This negative bounded search is not the formal
candidate audit and gives no proof credit.

Before the statement gate passes, every crosswalk row must point to an inspected source location
and a concrete Lean signature. Alternate closed/relative formulations require checked transports;
name similarity or a prose equivalence is insufficient.
