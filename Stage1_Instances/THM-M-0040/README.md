# THM-M-0040 rev-5.6 dossier

This directory is the fail-closed `planned` intake dossier for the catalog target named the
Amitsur-Levitzki theorem. The repository supplies only the gloss `矩阵环满足的多项式恒等式`
("matrix rings satisfy a polynomial identity"), attributes the entry to Shimshon Amitsur and
Alexander Levitzki in 1950, and labels it verified. Under rev-5.6 that label is untrusted inventory
metadata, not an exact statement, human-source review, or machine-proof evidence.

The 1950 paper by A. S. Amitsur and J. Levitzki, *Minimal identities for algebras*, was inspected
from the AMS version-of-record PDF. Its formula (2) defines the alternating standard polynomial
`S_(2n)`, and Theorem 1 on printed page 455 proves that it vanishes on the complete algebra of
`n x n` matrices over the paper's underlying field. The paper also treats the lower bound on the
degree of a polynomial identity, uniqueness of multilinear minimal identities, exceptional
characteristic-two cases, and extensions to other finite-dimensional algebras. The catalog does
not cite this paper or say which part of that package is the target. Its forename "Alexander" also
does not agree with the paper and Crossref's `J. Levitzki` attribution.

Consequently, intake preserves the recognizable theorem family but does not choose whether the root
is only the standard identity, also includes minimality or uniqueness, uses the paper's field scope
or a later commutative-ring generalization, or includes all positive sizes and which boundary
conventions. Choosing one now would silently add proposition-changing clauses.

Pinned mathlib provides finite permutations and their signs, ordered list products, finite sums,
and square-matrix ring multiplication. `IntakeProbe.lean` authenticates those interfaces. A bounded
exact-topic search found no Amitsur-Levitzki or standard-polynomial theorem; the similarly named
Hopkins-Levitzki module is unrelated. These are encoding and discovery observations only, not an
anchor audit or proof credit.

The canonical mathematical statement and Lean target therefore remain null. The provisional root
vector is `[H1, M4, R4]`, and all six downstream tasks remain open. No H0, M0, R0, accepted proof
state, audit completion, theorem completion, or master acceptance is claimed.
