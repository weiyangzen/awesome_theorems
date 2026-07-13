# THM-M-0831 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog label `Karger算法`
(Karger algorithm). The repository supplies only the gloss `全局最小割的随机算法` ("a randomized
algorithm for global minimum cut"), attributes it to David Karger in 1993, and labels it `已验证`.
An algorithm name and purpose are not a truth-valued proposition with ordered binders,
hypotheses, and a conclusion. The verified label is untrusted metadata and supplies neither source
nor proof credit.

An author-hosted copy of David R. Karger's 1993 SODA paper *Global Min-cuts in RNC, and Other
Ramifications of a Simple Min-Cut Algorithm* was inspected and hashed. Section 2 defines the
random contraction procedure on connected undirected multigraphs. Theorem 2.1 says that a fixed
minimum cut is returned with probability `Omega(n^-2)`; its proof gives the explicit lower bound
`1 / binom(n, 2)`. Corollary 2.1 amplifies independent trials to high probability. This is a
strong primary-source lead, but the catalog cites no source and does not choose the single-trial
bound, an amplification statement, weighted implementation, correctness, runtime, or RNC result.
No errata audit or independent source review has accepted one of those materially different claims.

Pinned mathlib supplies a general undirected multigraph type `Graph` that retains loops and parallel
edges, plus finite uniform probability-mass functions. `IntakeProbe.lean` authenticates those
interfaces. A bounded search found no Karger, graph-contraction, or minimum-cut theorem in the
pinned tree. The probe is encoding-substrate evidence only; it neither defines the contraction
dynamics nor proves this target.

The provisional vector is `[H5, M4, R4]`. Here `H5` classifies the received catalog method gloss as
not yet a stable proposition; it does not refute Karger's established theorems. The canonical human
statement and Lean expression remain null, and all six downstream phases remain open. No H0, M0,
R0, accepted execution state, audit completion, theorem completion, accepted receipt, or master
acceptance is claimed.
