# THM-M-0626 rev-5.6 dossier

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

The intake's provisional vector is `[H1, M3, R4]`: a complete modern proof source lead is known but
its identity with the uncited catalog record and historical provenance remain unreviewed; a usable
pinned statement/proof candidate was found; and no reviewed source-faithful reconstruction exists.
`instance.json` remains the intake authority and `task-dag.json` keeps all six downstream phases
open. The statement proposal below adds a canonical expression, transport, and receipt without
changing that debt vector or claiming H0, M0, R0, acceptance, audit completion, or theorem
completion.

## Provisional statement freeze

`Statement.lean` now freezes the inspected source formulation as
`Stage1Instances.THM_M_0626.ConnectedImageTarget`: arbitrary topological spaces, an implicit
subset `s`, `IsConnected s`, a globally `Continuous` map `f`, and the direct-image conclusion
`IsConnected (f '' s)`. This selects the Stacks Project's global-continuity wording rather than
silently strengthening the catalog claim to the sharper local `ContinuousOn` theorem. The latter
is recorded as an alternate and has a checked one-way implication to the canonical target.

The statement checker serializes and fingerprints the explicit universe-polymorphic expression,
verifies the single direct import, rejects mutations removing either hypothesis, changing the
domain or binder scope, and allowing the empty source, and kernel-checks empty, singleton, and
constant-map boundaries. These are worker-local statement artifacts only. The provisional intake
has not been master-accepted, and its requested independent source/convention review is still
absent.

## Provisional anchor audit

The bounded immutable inventory finds an exact pinned-mathlib route. `IsConnected.image` proves the
sharper `ContinuousOn` form in `Mathlib.Topology.Connected.Basic`; `AnchorAudit.lean` checks a
literal copy of the global root by applying it to `Continuous.continuousOn`. The terminal theorem,
its substantive dependency `IsPreconnected.image`, and the adapter are sorry-free and report only
`propext`, `Classical.choice`, and `Quot.sound`. This is an `M0-W` candidate, while the accepted
root remains `M3` until proof integration, transitive provenance/trust validation, and master
acceptance.

The external search found a commit-pinned `formal-conjectures` wrapper expressing the same global
claim, but its body calls the same mathlib theorem and supplies no independent terminal proof.
Repository-local sources, every materialized non-mathlib package, and the bounded public queries
found no additional independent Lean 4 body. Code-search authentication and rate-limit failures are
recorded, so exhaustive discovery is not claimed. Proof architecture, proof acceptance, H0/R0,
hermetic validation, release, and every theorem-completion gate remain open.

## Provisional obligation architecture

Registry version 1 freezes 22 semantic obligations before proof installation or accepted closure
metrics. The
typed proof route separates the global-to-local continuity transport, image nonemptiness, and the
substantive arbitrary-open proof of `IsPreconnected.image`. That proof owns distinct obligations
for relative-preimage construction, image-cover normalization, witness pullback, source
intersection, and intersection pushforward. Source, provenance, evidence, trust, documentation,
and workflow relations remain separate graphs and cannot supply proof credit.

`ObligationTree.lean` checks conditional compositions for the separation engine, the preconnected
image, the local connected-image body, its candidate-interface identity, terminal global assembly,
and the exact root identity. The imported candidate and local reconstruction are modeled as
alternative, deduplicated routes rather than mandatory copies of one another. Every mathematical
leaf remains an explicit premise; the audited `IsConnected.image` candidate is not installed. The
registry therefore preserves the accepted
root `[H1, M3, R4]`, an empty accepted-proof set, and false audit/theorem completion flags.
