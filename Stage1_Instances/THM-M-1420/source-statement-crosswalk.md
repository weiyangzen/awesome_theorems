# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:10376-10381` supplies exactly the title `Pesin理论`, Yakov
Pesin, 1977, the gloss `非一致双曲理论`, importance "high," and status `已验证`. The
six-line record entered the repository in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`; it has no citation or theorem statement.

`Docs/Stage0_Blueprint.md:38618-38643` repeats that gloss and explicitly leaves definitions and
premises, proof route, dependencies, equivalent forms, axioms, machine status, and artifact links
open. The rev-5.6 manifest carries `已验证` only as `source_status_untrusted` and resets the target
to `L0 / rework_required`.

## Literal crosswalk

| Repository element | Possible mathematical component | Required Lean component | Intake result |
|---|---|---|---|
| `Pesin理论` | an umbrella theory containing several theorem families | no single declaration follows from a theory name | not a stable proposition |
| "nonuniform" | point-dependent rates or uniform estimates restricted to increasing Pesin blocks | exact measurable/a.e. scopes, tempered bounds, constants, and block predicates | all open |
| "hyperbolic" | nonzero Lyapunov exponents and measurable stable/unstable Oseledets directions | cocycle or tangent derivative, spectrum, subspaces, invariance, norms, estimates | meaning and assumptions open |
| "theory" | invariant manifolds, absolute continuity, closing results, ergodic consequences, and entropy results | one exact `Prop` with ordered binders, hypotheses, and conclusion | no truth-valued conclusion supplied |
| Yakov Pesin / 1977 | historical attribution and year | pinpoint source provenance only | no edition, stable theorem ID, page, assumptions, proof, or errata |
| `已验证` | untrusted inventory metadata | inspectable source proof and kernel receipt would be required | no H or M credit |

## Bibliographic discovery boundary

Two distinct works commonly associated with the record are Yakov Pesin, *Families of Invariant
Manifolds Corresponding to Nonzero Characteristic Exponents*, Math. USSR-Izvestiya 10(6) (1976),
DOI `10.1070/IM1976v010n06ABEH001835`, and *Characteristic Lyapunov Exponents and Smooth Ergodic
Theory*, Russian Mathematical Surveys 32(4) (1977), DOI
`10.1070/RM1977v032n04ABEH001639`. They are listed only as bibliographic discovery candidates.
Neither work, its incorporated definitions, exact theorem locators, assumptions, proof boundary,
or errata was inspected and frozen for this intake. Their existence reinforces rather than resolves
the ambiguity; neither receives H credit or becomes the canonical claim.

## Neighbor and variant boundary

The repository separately catalogs SRB measures, Lyapunov exponents, Oseledets' theorem, and
Pesin's entropy formula. It also gives the general stable-manifold theorem and uniform hyperbolic
systems separate IDs. This separation is affirmative evidence that none of those familiar results
may be chosen merely because it is convenient to state in Lean.

## Source gate

Before an approved correction can leave `H5`, an accountable reviewer must preserve and hash an
immutable primary source, select one exact theorem and edition/page/section, transcribe every
incorporated definition, ordered binder, hypothesis, conclusion, and exceptional case, inspect its
proof dependencies and corrections or errata, and justify why that proposition represents
`THM-M-1420` rather than a neighboring target. A second qualified reviewer must approve the
source-to-canonical-statement mapping.

## Lean discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, a bounded source-name
search found no occurrence of "Pesin," "nonuniform hyperbolic," or "non-uniform hyperbolic" in
Lean sources. Pinned APIs do include `MeasurePreserving`, `Ergodic`, `mfderiv`, and `tangentMap`.
These are discovery facts only, not a complete formal-candidate audit and not evidence for a
canonical target.

The canonical module, expression, expression hash, checked transports, and statement mutations
remain null. No H0, M0, readable-proof closure, audit completion, or theorem completion is claimed.
