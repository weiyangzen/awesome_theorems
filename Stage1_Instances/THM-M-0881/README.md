# THM-M-0881 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog item `扩展图`
("expander graphs"). The repository supplies only the gloss `扩展图的存在性与构造`
("existence and construction of expander graphs"), attributes it to many mathematicians in the
twentieth century, and labels it `已验证`. Under rev-5.6 that label is untrusted metadata and gives
neither human-source nor machine-proof credit.

The gloss identifies a theorem family, not one truth-valued proposition. It does not choose vertex,
edge, or spectral expansion; a graph model; degree and expansion parameters; the quantification over
orders; an infinite-family convention; or probabilistic versus explicit construction. These choices
are not interchangeable. In particular, nearby Margulis, LPS, Ramanujan, Morgenstern, and MSS entries
are separate target IDs and cannot silently become this root.

This intake freezes the received wording, source provenance, proposition-changing choices,
neighbor boundaries, and adjacent pinned Lean APIs. It deliberately leaves the canonical
mathematical statement and Lean target null. The provisional root vector is `[H5, M4, R4]`: the
received target is not yet a stable proposition, no exact formal artifact is credited, and no
source-faithful proof reconstruction can attach before a proposition is selected. This does not say
that standard expander existence theorems are false or open.

`instance.json` is the structured scope authority. `scope-map.md` records the admissible target
questions and prohibited substitutions. `source-statement-crosswalk.md` maps every supplied phrase
to the missing mathematical and Lean components. `task-dag.json` keeps all downstream phases open.
`IntakeProbe.lean` checks only adjacent pinned finite-simple-graph and matrix interfaces. Exact
validation commands and their boundaries are recorded in `validation.md` and
`intake-receipt.json`.

No canonical statement, H0, M0, R0, accepted execution state, audit completion, theorem completion,
or master acceptance is claimed.
