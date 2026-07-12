# Source-statement crosswalk

## Repository sources inspected

`Docs/researches/math_theorems.md:10320-10325` is the complete repository research record. It gives
the title `Anosov微分同胚`, proposer Dmitri Anosov, year 1967, gloss `一致双曲系统`, importance
"high," and status `已验证`. Git history traces these lines to repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`, which is repository provenance rather than an
immutable mathematical source.

`Docs/Stage0_Blueprint.md:38402-38427` repeats the same metadata while explicitly leaving the
background, precise definitions and premises, proof process and date, theorem tree, equivalent
forms, axioms, machine status, and artifact links open. The rev-5.6 manifest carries `已验证` only
in the field `source_status_untrusted` and resets this target to `L0 / rework_required`.

A repository-wide bounded search found no other Anosov source statement or theorem-specific
artifact. No primary monograph edition, paper, translation, theorem or definition number, page,
assumption list, errata record, proof boundary, or reviewer is identified.

Two historical discovery candidates are Dmitri Anosov's *Geodesic Flows on Closed Riemannian
Manifolds with Negative Curvature* (Steklov Institute volume 90, Russian 1967; English record
1969) and Stephen Smale's *Differentiable Dynamical Systems*, *Bulletin of the AMS* 73 (1967),
DOI `10.1090/S0002-9904-1967-11798-1`. Neither was supplied by the repository or inspected here to
an immutable pinpoint proposition. The first concerns flows rather than selecting this
diffeomorphism item. Both remain search leads only and receive no source or statement credit.

## Crosswalk

| Repository phrase | Possible mathematical component | Prospective Lean component | Intake assessment |
|---|---|---|---|
| `Anosov微分同胚` | a globally invertible smooth self-map satisfying uniform hyperbolicity | `Diffeomorph` plus source-selected hyperbolicity data | names a class; not a proposition |
| "diffeomorphism" | smooth bijection with smooth inverse | `Diffeomorph I I M M n` | pinned generic substrate exists; regularity and manifold data absent |
| "system" | iterations of a self-map on a phase space | `Function.iterate` or a source-selected integer action | time domain and claimed dynamical property absent |
| "uniformly hyperbolic" | stable/unstable tangent splitting, derivative invariance, and uniform estimates | `TangentSpace`, `mfderiv`, subspaces/subbundles, norms, and quantified estimates | descriptive gloss only; exact encoding and constants absent |
| "Dmitri Anosov, 1967" | historical discovery pointer | immutable primary edition and pinpoint locator required | no bibliographic identity or theorem locator supplied |
| `已验证` | catalog classification | no Lean proposition or proof object | explicitly rejected as evidence |

## Missing source-to-statement decisions

Before a canonical statement can be frozen, the dependent statement phase must obtain and
independently review an immutable primary edition or accepted translation and record:

1. the exact definition or theorem passage and every incorporated definition, with stable page or
   section locators and content hashes;
2. the complete manifold, metric, regularity, compactness, dimension, and invertibility premises;
3. the precise splitting or equivalent encoding, derivative invariance, constants, iterate
   domain, norm, and inequalities;
4. the proposition-level conclusion and whether the item is definitional, existential,
   classificatory, or a consequence theorem;
5. translation fidelity, correction and errata status, dependent source passages, and a named or
   assigned independent reviewer;
6. all boundary cases and a justification that the selected proposition is this catalog target
   rather than a nearby hyperbolic-dynamics result.

Until those decisions are made, the received target is classified `H5`: it is not yet a stable
proposition. This is a routing classification, not a claim that standard definitions or theorems
about Anosov diffeomorphisms are false or historically open.

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the discovery-only
probe elaborates generic `Diffeomorph`, `Diffeomorph.refl`, `Diffeomorph.symm`, `mfderiv`, and
`tangentMap` APIs. A bounded case-insensitive source search found no `Anosov`, `uniformly
hyperbolic`, `hyperbolic diffeomorphism`, or dynamical `hyperbolic system` name. These are intake
observations only: they do not constitute the downstream immutable anchor audit, an exhaustive
external negative result, a canonical statement, or proof evidence.
