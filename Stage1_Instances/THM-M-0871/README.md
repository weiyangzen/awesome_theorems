# THM-M-0871 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for Courcelle's theorem. The repository
supplies only the slogan `有界树宽图的MSO可判定性` (decidability of MSO on bounded-treewidth
graphs), the attribution Bruno Courcelle, the year 1990, and an untrusted `已验证` status. That
identifies a published theorem family, but not one binder-complete proposition.

Courcelle's 1990 primary article proves decidability for context-free graph sets and bounded
expression width, with linear evaluation when a fixed formula is applied to a supplied bounded-
width expression or grammar derivation. His 1992 primary article defines treewidth and obtains
polynomial and quadratic bare-hypergraph algorithms through a tree-decomposition bridge. These
results use finite labeled graphs or hypergraphs and a two-sorted logic quantifying over vertices,
edges, vertex sets, and edge sets; the 1990 main framework also admits counting atoms. They do not
select the familiar modern slogan as one unique MSO1, MSO2, CMSO, decidability, model-checking, or
linear-time statement.

The canonical mathematical statement and Lean expression therefore remain null. The provisional
vector is `[H1, M4, R4]`: published primary results support the family, but exact root, definitions,
assumptions, correction mapping, and independent review are open; no source-identical usable Lean
artifact is credited; and no readable proof reconstruction can attach to an unfrozen root.

`IntakeProbe.lean` checks only adjacent pinned first-order graph, finite simple-graph, tree, and
isomorphism APIs. It does not encode monadic second-order logic, tree decompositions, treewidth, a
decision procedure, or Courcelle's theorem. `instance.json` is the structured scope authority,
`scope-map.md` records the proposition-changing choices, `source-statement-crosswalk.md` records the
source boundary, and `task-dag.json` keeps all six downstream phases open.

No canonical statement, H0, M0, R0, accepted execution state, audit completion, theorem completion,
accepted receipt, or master acceptance is claimed.
