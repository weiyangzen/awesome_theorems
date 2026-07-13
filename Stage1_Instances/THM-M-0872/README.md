# THM-M-0872 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog label
`Bodlaender算法` (Bodlaender algorithm). The repository supplies only the gloss
`树宽的线性时间近似` ("linear-time approximation of treewidth"), attributes it to Hans
Bodlaender in 1996, and labels it `已验证`. That label is untrusted metadata. The gloss omits
the approximation ratio, parameter and graph model, output, cost model, ordered binders, and
boundary cases, so it is not yet one truth-valued proposition.

The year-matched paper is Hans L. Bodlaender, *A Linear-Time Algorithm for Finding
Tree-Decompositions of Small Treewidth*, SIAM Journal on Computing 25(6), 1305-1317 (1996), DOI
`10.1137/S0097539793251219`. Its recorded summary states an exact fixed-parameter result: for
constant `k`, a linear-time algorithm decides whether `treewidth(G) <= k` and, in the positive
case, returns a decomposition of width at most `k`. That is not an approximation theorem. The
catalog-to-paper mismatch must be resolved by source and scope review rather than silently
replacing the received target.

Pinned mathlib supplies finite simple graphs, graph trees, and a Turing-machine time interface.
`IntakeProbe.lean` authenticates only those adjacent APIs. A bounded source search found no
treewidth, tree-decomposition, or Bodlaender declaration in the pinned Lean tree. The probe defines
no treewidth structure or algorithm and earns no statement or proof credit.

The provisional vector is `[H5, M4, R4]`. Here `H5` classifies the received approximation gloss as
not yet a stable proposition; it does not refute Bodlaender's published results. The canonical
human statement and Lean expression remain null, all six downstream phases remain open, and no
H0, M0, R0, audit completion, theorem completion, accepted receipt, or master acceptance is
claimed.
