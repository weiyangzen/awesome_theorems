# THM-M-0110 anchor audit

Item `S56-M-0110-ANCHOR_AUDIT` audits the literal frozen declaration
`Stage1Instances.THMM0110.KodairaVanishingTarget` at expression SHA-256
`d0a9a0e873dd388aa37c0bcc77fce1fc38bae5911851a87570b94f50c80eecc6`.
This is bounded worker evidence pending master acceptance, not a proof.

## Literal target boundary

The target has concrete `Scheme`, `X.Modules`, and `Sheaf.H` carriers. Its
projectivity, canonical/dualizing, invertible/rank-one/ample, and tensor-product
fields are nevertheless independent propositions. Lean has no eliminator that
connects those labels to the stored `X`, `K`, `L`, or `KTensorL`. Candidate
normalization must therefore compare against this literal stronger expression,
not the comments' intended ordinary Kodaira theorem. This object-model
disconnect is the first integration blocker.

## Candidate result

| Candidate | Immutable boundary | Classification | Root credit |
|---|---|---|---|
| Legacy `Stage1.THMM0110.StatementShape` | repository blob `efb8630c...`, source SHA-256 `e9e6b6d9...` | non-exact planning/interface artifact, `M3/E3` | none |
| `CategoryTheory.Sheaf.H` | mathlib `8a178386...`, `SheafCohomology.Basic` | exact cohomology carrier only, `M3/E3` | none |
| `Sheaf.subsingleton_H_of_isZero` | same pin; axiom set `propext`, `Classical.choice`, `Quot.sound` | stronger `IsZero`-premise near-anchor, `M3/E3` | none |
| `Abelian.Ext.subsingleton_of_injective` | same pin and axiom set | stronger injectivity-premise near-anchor, `M3/E3` | none |
| properness of `Proj.toSpecZero` | same pin, source SHA-256 `139bce06...` | geometric substrate only, `M3/E3` | none |
| Atlas Kodaira/AG files | commit `34ffed39...`, tree `c12fe231...` | embedding, affine/P1, numerical, opaque, and placeholder-bearing mismatches, `M5/E3` | rejected |
| Physlib Kodaira fibers | commit `851e49a3...`, tree `09b9b323...` | name collision and domain mismatch, `M5/E3` | rejected |
| formal-conjectures | bounded Sourcegraph repository query | no candidate | none |

The target-owned Lean probe shows that the zero-sheaf lemma reaches exactly the
concrete `Sheaf.H` carrier only when given an additional `IsZero` premise. The
frozen target does not produce that premise. No exact or stronger terminal
theorem, external kernel closure, pin/import task, or repo-local wrapper was
found.

## Search and source boundary

Pinned mathlib at `8a178386ffc0f5fef0b77738bb5449d50efeea95`
(tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`) is clean. Exact
Kodaira, canonical/dualizing-sheaf, Serre-duality, ample-line-bundle,
projective-morphism, line-bundle, and `Scheme.Modules` tensor query families
returned no terminal candidate. Sourcegraph exact queries completed with
archived repositories and forks included and zero matches; its broad Kodaira
query returned only the classified Atlas and Physlib name matches. Five GitHub
repository queries completed with zero repositories. Anonymous GitHub code
search was rate-limited, so exhaustive discovery is not claimed.

DOI metadata verifies Kodaira's 1953 PNAS article and Hartshorne's 1977 book.
No immutable theorem-text scan or page/premise/errata audit was obtained. The
historical analytic source and the arbitrary-characteristic-zero algebraic
target remain at `H1`; metadata does not establish their transport.

## Decision

The root stays `[H1, M3, R3]`. The assigned inventory is classified, but the
theorem-wide audit, obligation tree, proof, trust closure, source/readability
reviews, validation, release, `AUDIT-Z`, and theorem completion all remain
open. Repair and re-accept the object model, or locate an exact proof of the
current literal target, before machine status can advance.
