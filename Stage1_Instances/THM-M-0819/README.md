# THM-M-0819 rev-5.6 dossier

This directory is the fail-closed `planned` intake dossier for the theorem family cataloged as
Dilworth's theorem. The repository gloss says only "the minimum number for decomposing a partially
ordered set into chains." It omits what that minimum equals, whether the poset is finite, and the
definitions of chain decomposition, cover, width, and the empty case.

The inspected primary statement is R. P. Dilworth's Theorem 1.1 on original page 161. It assumes
that every `(k + 1)`-element subset of a poset is dependent and that some `k`-element subset is
independent, and concludes that the poset is a set sum of `k` disjoint chains. The primary paper
treats the finite case first and then the general case by a transfinite argument. Only a two-page
publisher preview was lawfully inspected, so the full proof, corrections, and independent source
review remain open.

Pinned mathlib supplies `IsChain`, `IsAntichain`, set cardinality, and chain-height infrastructure,
but no Dilworth declaration or the needed antichain-width and chain-partition definitions. Its
curated `1000.yaml` points to Vlad Tsyrklevich's external Lean 4 proof. At immutable commit
`f82f920f05a381bb1ce5e8903bde33e27f4365b6`, that file states the standard finite-poset equality
`minChainPartition_eq_antichainWidth`. The source has no textual proof escape, but it was written
for Lean 4.28.0-rc1 and mathlib `3234d21e...`; direct checking under this repository's newer pin
fails at three locations and consequently reports `sorryAx`. It is therefore a credible but blocked
formal candidate, never root proof credit.

The intake leaves the canonical statement and formal target null. Its provisional vector is
`[H1, M5, R3]`: a pinpoint primary statement lead is known but not fully reviewed; a credible Lean
4 candidate is blocked under the local validation environment; and this dossier supplies only a
labeled source, scope, and blocker report rather than a proof reconstruction. All six downstream
tasks remain open. No accepted state, audit completion, theorem completion, or master acceptance is
claimed.
