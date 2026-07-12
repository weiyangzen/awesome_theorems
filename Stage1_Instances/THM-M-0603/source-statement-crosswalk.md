# Source-statement crosswalk

## Repository source record

`Docs/researches/math_theorems.md` contains two matching records: `托姆配边理论` and `配边理论`.
Both attribute the result to Rene Thom (1954), gloss it as `流形的配边分类`, and label it
`已验证`. `Docs/Stage0_Blueprint.md` repeats the latter record but leaves definitions and sources
open. The rev-5.6 manifest explicitly imports `已验证` only as `source_status_untrusted`.

These metadata establish a topic, not an exact theorem and not machine evidence.

## Primary-source candidate

Rene Thom, "Quelques proprietes globales des varietes differentiables," *Commentarii Mathematici
Helvetici* 28 (1954), 17-86, is the identified primary publication. It is a discovery anchor only:
this intake did not accept an immutable scan hash, exact theorem/page locator, premise mapping,
translation, or errata review. Those omissions prevent `H0`.

## Claim crosswalk

| Received phrase | Candidate mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "manifolds" | closed smooth manifolds of one fixed dimension | concrete smooth manifold types, compactness, no-boundary and dimension witnesses | family identified; exact binders open |
| "bordism" | a compact smooth manifold whose boundary is the disjoint union of the inputs, with category-compatible structure | manifold-with-boundary/corners, boundary decomposition and orientation conventions | included; API open |
| "classification" | equality in a bordism group iff all invariants in a complete family agree | quantified invariant family and both implications | meaning unresolved |
| unoriented candidate | Stiefel-Whitney numbers form a complete invariant for unoriented bordism | mod-2 cohomology, Stiefel-Whitney classes, fundamental class and evaluations | candidate; not selected |
| oriented candidate | Stiefel-Whitney and Pontryagin numbers form the relevant complete invariant for oriented bordism | orientations, integral/rational characteristic numbers and all degree constraints | candidate; not selected |
| Pontryagin-Thom candidate | bordism classes correspond to stable homotopy classes into a Thom object | Thom spaces/spectra, stabilization and an explicit equivalence | related candidate; not selected |

The source audit must pinpoint the exact primary theorem and determine whether the catalog's
singular word "classification" refers to the characteristic-number criterion, Pontryagin-Thom, or
another result in the paper. It must map assumptions and every direction of the conclusion, inspect
corrections and later convention changes, and obtain independent review before assigning `H0`.

## Lean discovery boundary

No formal declaration is credited at intake. Repository references to cobordism in other theorem
dossiers are audit prose or obligations, not a proof body for this target. The anchor-audit phase
must separately search pinned mathlib and credible Lean 4 projects at immutable revisions, recording
exact declaration types, terminal bodies, axioms, licenses, and integration feasibility. A type that
merely postulates bordism classification is inadmissible.
