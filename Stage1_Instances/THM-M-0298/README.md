# THM-M-0298 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the Calderon-Zygmund decomposition.
The repository catalogue attributes the target to Alberto Calderon and Antoni Zygmund in 1952,
but its entire statement gloss is only "function decomposition technique." The `已验证` label is
untrusted metadata under rev-5.6 and supplies no statement, source-fidelity, or proof credit.

The title identifies a classical theorem family, not one exact proposition. Standard formulations
decompose an integrable function at a positive height into a bounded good part and localized,
mean-zero bad parts. They vary materially in their ambient space, scalar codomain, cubes versus
balls, dyadic versus arbitrary selection, equality sense, overlap, constants, support dilation,
norm conclusions, and endpoint treatment. Choosing one familiar textbook formulation here would
silently supply proposition-changing mathematics absent from the catalogue.

Publisher and Crossref metadata identify Calderon and Zygmund's 1952 paper *On the existence of
certain singular integrals*, Acta Mathematica 88, pages 85-139, DOI `10.1007/BF02392130`, as a
matching primary-source lead. The paywalled article metadata was inspected, but no immutable
full-text passage, incorporated definitions, exact assumptions, proof boundary, correction or
errata audit, or independent source review is admitted. The citation is therefore an `H1` lead,
not an `H0` source packet.

Pinned mathlib has substantial adjacent infrastructure for set averages, the mean-zero identity,
Euclidean box volume, and Vitali/Besicovitch coverings. A bounded exact-name search found no local
Calderon-Zygmund decomposition declaration. An immutable external Lean project supplies a credible
kernel-checked metric-space decomposition bundle, but it uses a different Lean/mathlib pin and is
not in this repository's validation closure. The discovery-only local probe authenticates adjacent
APIs; it neither selects nor proves the root. The provisional root vector is `[H1, M1, R4]`.

All six downstream phases remain open in `task-dag.json`. No canonical mathematical or Lean
proposition, H0, M0, R0, accepted execution state, audit completion, theorem completion, or master
acceptance is claimed.
