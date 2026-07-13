# Source-statement crosswalk

## Repository authority

`Docs/researches/math_theorems.md:6292-6297` records the Chinese title "Brooks theorem," attributes
it to Rowland Brooks, gives the year 1941 and the complete gloss "an upper bound for the chromatic
number," and labels it `已验证`. All six uncited lines originate at repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. They contain no formula, bibliography, definitions,
hypotheses, proof boundary, correction history, or formal artifact.

`Docs/Stage0_Blueprint.md:23414-23439` repeats the gloss while explicitly leaving the formal system,
precise definitions and premises, proof route, dependencies, equivalent formulations, axioms,
machine status, and artifact links open. The rev-5.6 manifest retains `已验证` only as
`source_status_untrusted` and resets this target to `L0 / rework_required`.

## Inspected primary source lead

R. L. Brooks, *On colouring the nodes of a network*, Proceedings of the Cambridge Philosophical
Society 37(2) (April 1941), pages 194-197, DOI `10.1017/S030500410002168X`. Publisher metadata and
the publisher's first-page facsimile were inspected. The facsimile has SHA-256
`10837123a6d5f8a87d70fdfe6628799a0710ab4cd6efe292717e282f281ee9c4` and contains the complete
theorem paragraph, the definition of `n`-simplex, and the statement that the network may be
infinite and nonplanar. The note begins its proof on the same page.

This is a pinpoint primary statement and proof lead at printed page 194, not yet `H0`: the four-page source has not been
preserved in this dossier, the graph-versus-network semantics and proof premises have not been
fully crosswalked, corrections and errata have not been audited, and no independent reviewer has
accepted the mapping.

## Literal crosswalk

| Printed source component | Prospective Lean component | Intake status |
|---|---|---|
| network (or linear graph) `N` | `G : SimpleGraph V` | candidate; loopless simple graphs fit, but parallel-line semantics remain under review |
| "not more than `n` lines meet" each node | `[G.LocallyFinite]` and `forall v, G.degree v <= n` | source-shaped candidate; pointwise rather than global maximum-degree form |
| `n > 2` | `2 < n` | material root hypothesis; `n = 2` is not silently added |
| no line has both ends at the same node | `SimpleGraph` looplessness | direct representation; source-to-model transport still needs review |
| no connected component is an `n`-simplex | `forall c : G.ConnectedComponent, not (IsNSimplex c.toSimpleGraph n)` | candidate all-components encoding |
| `n`-simplex has `n + 1` mutually joined nodes | `Nonempty (H ≃g completeGraph (Fin (n + 1)))` | candidate exact finite-isomorphism predicate |
| color nodes with `n` colors, joined nodes distinct | `G.Colorable n` | direct proper-coloring API |
| `N` may be infinite and nonplanar | arbitrary `V`, with no `Finite V`, `Fintype V`, or planarity hypothesis | preserved by the envelope |

## Modern-form boundary

The widely quoted modern theorem for a finite connected simple graph bounds its chromatic number by
its maximum degree unless it is complete or an odd cycle. That formulation is closely related but
not textually identical to the 1941 paragraph. Its finite carrier, connected root, maximum-degree
parameter, and explicit odd-cycle exception cannot be imported into the canonical target without
checked transports and a reviewed source decision. Conversely, Brooks's `n > 2` branch and
componentwise simplex exclusion must not be dropped merely because the modern slogan is familiar.

## Lean intake boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, `IntakeProbe.lean`
elaborates a candidate envelope with the fields above and checks the relevant APIs. A bounded
repository and pinned-mathlib search found no exact Brooks theorem. The probe declares no theorem
and supplies no proof body, expression fingerprint, transport, mutation result, or machine-proof
credit. Those belong to the dependent statement and anchor-audit phases.
