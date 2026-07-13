# THM-M-0851 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog item `连通性阈值`
(connectivity threshold). The repository supplies only the gloss `随机图连通的阈值`, attributes
the topic to Erdos and Renyi in 1959, and labels it `已验证`. The label is explicitly untrusted and
provides no source, statement, or proof credit.

The wording identifies a random-graph connectivity-threshold family, not one stable truth-valued
proposition. It does not choose the fixed-edge model `G(n,m)`, the independent-edge model `G(n,p)`,
or the coupled random graph process. It also leaves open the threshold parameterization, ordered
asymptotic quantifiers, one-sided versus two-sided conclusion, critical-window limit law,
connectivity convention, and finite boundary cases. Choosing the familiar formula from folklore
would substitute an unstated theorem.

Erdos and Renyi's 1959 paper *On Random Graphs I* is a strong primary-source candidate matching the
catalog attribution and year. Theorem 1 on pages 290-291 gives a fixed-edge critical-window
connectivity limit law, while Theorem 4 is a distinct sequential edge-process stopping result. This
intake records that source family only as discovery evidence: the repository does not select either
variant, and the complete definition/assumption/proof/errata crosswalk and independent review remain
open.

The canonical mathematical statement and Lean expression therefore remain null. The provisional
root vector is `[H1, M4, R4]`: a named primary-source candidate is known but exact source fidelity
is open; no usable exact formal theorem is identified; and no source-faithful proof reconstruction
can attach to an unfrozen root.

Pinned mathlib exposes `SimpleGraph.binomialRandom` and `SimpleGraph.Connected`, but the former is
the independent-edge law and mathlib explicitly distinguishes it from the historical fixed-edge
Erdos-Renyi model. `IntakeProbe.lean` checks only these adjacent APIs and connectivity boundary
conventions. It states and proves no threshold theorem. All six downstream tasks remain open; no
exact target, proof, accepted state, audit completion, theorem completion, or master acceptance is
claimed.
