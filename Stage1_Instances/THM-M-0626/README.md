# THM-M-0626 rev-5.6 intake

This directory is the self-tested `planned` intake dossier for `连通性定理` (continuous images
preserve connectedness). The repository gives the literal claim `连通集的连续像连通` ("the
continuous image of a connected set is connected"), attributes it only to many mathematicians in
the nineteenth century, and labels it `已验证`. Under rev-5.6 that label is untrusted catalog
metadata, not a source audit or proof receipt.

The claim is specific enough to freeze a candidate human scope: for arbitrary topological spaces,
a globally continuous function sends a nonempty connected subset to a connected set-theoretic
image. A current, immutable secondary source lead, the Stacks Project Lemma 5.7.2 (tag `0376`),
states and proves precisely that formulation. It also defines connected spaces as nonempty.
The catalog does not cite this source, and no primary historical source, attribution audit, errata
review, or independent source review has been accepted, so the source status remains `H1`, not
`H0`.

Pinned mathlib has the direct formal candidate `IsConnected.image` in
`Mathlib.Topology.Connected.Basic`. It assumes `IsConnected s` and `ContinuousOn f s` and concludes
`IsConnected (f '' s)`. `IntakeProbe.lean` authenticates that candidate, the nonempty definition of
`IsConnected`, and nearby variants. Its weaker local continuity is the natural exact set-image
encoding; a checked relation to the globally continuous Stacks statement remains statement-phase
work. Candidate discovery does not supply accepted proof credit.

The provisional vector is `[H1, M3, R4]`: a complete modern proof source lead is known but its
identity with the uncited catalog record and historical provenance remain unreviewed; a usable
pinned statement/proof candidate exists but no canonical expression, transport, provenance audit,
or receipt is frozen; and no reviewed source-faithful reconstruction exists. `instance.json` is the
structured scope authority and `task-dag.json` keeps all six downstream phases open. No H0, M0,
R0, accepted execution state, audit completion, theorem completion, or master acceptance is
claimed.
