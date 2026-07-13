# THM-M-0879 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog item `多商品流`
(`multicommodity flow`). The repository supplies only the gloss `多种商品的并发流` (`concurrent
flow of multiple commodities`), attributes it collectively to many mathematicians in the
twentieth century, and labels it `已验证`. Under rev-5.6 that label is untrusted metadata and gives
neither human-source nor machine-proof credit.

The wording identifies a problem family, not one truth-valued theorem. It does not choose a graph
or network model, commodity and demand data, capacity domain, splittable versus unsplittable flows,
edge-flow versus path-flow representation, feasibility or optimization objective, an exact
duality or flow-cut statement, or an approximation guarantee. Those choices are proposition
changing. In particular, the adjacent network-flow, minimum-cost-flow, and sparse-cut catalog
items cannot silently become this root.

Two bibliographic leads confirm that the phrase has several noninterchangeable meanings: Hu's 1963
paper treats simultaneous two-commodity flows, while Shahrokhi and Matula's 1990 paper studies the
maximum concurrent flow problem, its approximation scheme, and a path-cut duality. The catalog
cites neither work and selects none of those results. They are subject-discovery evidence only.

This intake freezes the received wording, repository provenance, scope choices, source leads,
neighbor boundaries, and adjacent pinned Lean APIs. It deliberately leaves the canonical
mathematical statement and Lean target null. The provisional root vector is `[H5, M4, R4]`: the
received wording is not a stable proposition, no exact usable formal artifact is credited, and no
source-faithful reconstruction can attach before a proposition is selected.

`instance.json` is the structured scope authority and `task-dag.json` leaves all six downstream
phases open. `IntakeProbe.lean` checks generic substrate only. No canonical statement, H0, M0, R0,
accepted execution state, audit completion, theorem completion, or master acceptance is claimed.
