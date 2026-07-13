# THM-M-0616 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog item
`连续性定义` (continuity definition). The received claim is only:

> The epsilon-delta definition and the open-preimage definition are equivalent.

The gloss identifies a standard continuity-equivalence family, but it does not freeze one exact
proposition. It omits the domain and codomain; metric versus pseudometric structure; global,
pointwise, or on-a-set continuity; strict versus non-strict inequalities; and all boundary cases.
It also does not cite an edition, theorem, proof, errata record, or reviewer. The catalog label
`已验证` is untrusted metadata and supplies no source or machine-proof credit.

Sidney A. Morris's *Topology Without Tears*, version of August 6, 2024, is an inspected modern
source lead. Section 5.1 gives the epsilon-delta definition for real functions, proves its local
open-neighborhood form in Lemma 5.1.1, proves the open-preimage/local-neighborhood equivalence in
Lemma 5.1.2, and gives the open-preimage definition in Definition 5.1.3. This closely supports the
catalog family, but the repository does not cite it, and it does not by itself select the general
metric-space formulation or supply an independently reviewed source-to-root crosswalk. It is an
`H1` lead, not `H0` evidence.

Pinned mathlib contains direct exact-topic interfaces. `continuous_def` exposes the open-preimage
definition, while `Metric.continuous_iff`, `Metric.continuousAt_iff`, and
`Metric.continuousOn_iff` expose distinct epsilon-delta formulations on pseudometric spaces.
`IntakeProbe.lean` authenticates their types and reported axioms. These interfaces justify the
provisional `M3` classification, but no one declaration has been selected as the source-identical
root and no proof body receives credit.

The provisional vector is `[H1, M3, R4]`. `instance.json` is the structured scope authority,
`scope-map.md` records proposition-changing choices and exclusions,
`source-statement-crosswalk.md` maps the repository, inspected source, and pinned Lean surfaces,
and `task-dag.json` keeps every downstream phase open. No canonical proposition, accepted proof
state, `H0`, `M0`, `R0`, audit completion, theorem completion, release, or master acceptance is
claimed.
