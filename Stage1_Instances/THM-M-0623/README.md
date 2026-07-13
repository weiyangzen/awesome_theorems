# THM-M-0623 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the Urysohn metrization theorem.
The repository catalog gives only the Chinese gloss `第二可数正则空间可度量化` ("a
second-countable regular space is metrizable"), attributes it to Pavel Urysohn in 1925, and labels
it `已验证`. Under rev-5.6 that label is untrusted metadata, not a source review or proof receipt.

The gloss identifies a classical theorem family, but its word "regular" is convention-sensitive.
Pinned mathlib's `RegularSpace` deliberately does not include `T0Space`. It proves only
`PseudoMetrizableSpace` from regularity and second countability. Its full metric result assumes
`T3Space`, which extends both `T0Space` and `RegularSpace`. Thus silently mapping the catalog word
to bare `RegularSpace` makes the metric conclusion false, while silently adding `T0Space` or
choosing `T3Space` changes an unstated source convention.

`IntakeProbe.lean` authenticates both pinned exact-topic candidates, their separation interfaces,
and their current axiom reports. It does not select either candidate as the canonical root, prove a
source transport, or confer proof credit. The historical paper locator in the crosswalk is only a
bibliographic discovery lead; no theorem passage, incorporated definitions, proof boundary,
translation, corrections, errata, or independent review is accepted.

The provisional root vector is `[H1, M3, R4]`: a historically proved theorem family and source lead
are known, usable pinned formal candidates exist, but the exact source convention and canonical
Lean target are not frozen and no source-faithful reconstruction exists. `instance.json` is the
structured scope authority, `scope-map.md` and `source-statement-crosswalk.md` freeze the ambiguity
and non-substitution boundary, and `task-dag.json` keeps all six downstream phases open. No H0,
M0, R0, accepted execution state, audit completion, theorem completion, or master acceptance is
claimed.
