# THM-M-0625 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog entry named the Bing
metrization theorem. The repository supplies only the gloss "metrizability of collectionwise
normal spaces", attributes it to R. H. Bing in 1951, and labels it verified. That label is
untrusted inventory metadata, not an exact statement or proof receipt.

Bing's primary paper, *Metrization of Topological Spaces*, was inspected. It does not state that
collectionwise normality alone implies metrizability. The directly relevant result is Theorem 10
on page 182: a Moore space is metrizable if it is collectionwise normal. In Bing's terminology a
Moore space is a regular developable space. The catalog gloss therefore omits a proposition-critical
Moore/developability hypothesis and could also be read as the related Theorem 14, which says only
that collectionwise normality implies normality. Intake preserves this ambiguity instead of
silently asserting the false broadened implication.

Pinned mathlib defines `RegularSpace`, `NormalSpace`, `Set.PairwiseDisjoint`, and
`TopologicalSpace.MetrizableSpace`. `IntakeProbe.lean` authenticates those interfaces. A bounded
search found no collectionwise-normal, development, Moore-space, screenability, or Bing
metrization declaration. These APIs are substrate, not a formal theorem candidate.

The provisional vector is `[H1, M4, R4]`: a primary theorem and proof are known, but the catalog-to-
source identity, exact modern definitions, errata review, and independent source review remain
open; no usable exact Lean artifact or readable formal reconstruction is credited. `instance.json`
is the scope authority and `task-dag.json` keeps all downstream phases open. No H0, M0, R0,
accepted execution state, audit completion, theorem completion, or master acceptance is claimed.
