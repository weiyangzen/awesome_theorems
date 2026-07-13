# THM-M-0939 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog label
`Kemperman定理` (Kemperman theorem). The repository gives Johannes Kemperman, the year 1960, and
only the gloss `阿贝尔群上子集和的结构` (structure of subset sums in abelian groups). That gloss is
identical to the neighboring Kneser entry. The manifest's `已验证` label is untrusted metadata, not
a source, statement, or proof receipt.

Kemperman's primary paper *On small sumsets in an abelian group*, *Acta Mathematica* 103 (1960),
63-88, DOI `10.1007/BF02546525`, is the strongest bibliographic candidate. Modern inspected
sources make the likely subject materially more precise: Kemperman's structure theorem classifies
critical pairs of finite subsets of an arbitrary abelian group, rather than merely giving Kneser's
sumset-cardinality bound. The primary paper itself has not been admitted and mapped at theorem
resolution in this intake, so it remains a bibliographic candidate rather than the canonical root.

Two complete modern formulations were inspected. Boothby, DeVos, and Montejano,
arXiv:`1301.0095v2`, Theorem 4.5, gives a recursive classification of maximal nontrivial critical
trios by impure beats or chords ending in a pure beat or chord. Lev, arXiv:`math/0508179v2`,
Theorem C, presents a pair formulation attributed to Kemperman [K60, Theorem 5.1], using elementary
pairs, a subgroup and quotient pair, and a unique-representation condition. These are exact
source-root candidates, not interchangeable snippets. Their equivalence to the original theorem,
the definition chain, boundary conventions, and the catalog's intended root still require
independent review.

`IntakeProbe.lean` checks only adjacent pinned Cauchy-Davenport and stabilizer interfaces. It states
no Kemperman target and supplies no proof credit. The provisional vector is `[H1, M4, R4]`: complete
published proof candidates are known, but exact source identity and assumption mapping remain
unaudited; no usable exact Lean artifact is credited; and no source-faithful readable proof has
been reconstructed.

The canonical mathematical statement and Lean expression remain null. All six downstream tasks
remain open. No H0, M0, R0, accepted execution state, audit completion, theorem completion, or
master acceptance is claimed.
