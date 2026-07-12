# THM-M-1374 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label
`Noether定理` (Noether's theorem). The catalog supplies only Emmy Noether, 1918, and the gloss
`对称性与守恒量` (symmetries and conserved quantities). It supplies no cited proposition,
definitions, hypotheses, conclusion, or proof boundary. Its `已验证` status is explicitly
untrusted metadata under rev-5.6.

The name denotes a theorem family rather than one fixed proposition. Noether's 1918 paper states
two materially different theorems for invariant variational integrals: a finite-continuous-group
invariance result yielding linearly independent divergence relations, with a source-qualified
converse, and an infinite-group result relating arbitrary-function symmetries to differential
identities among Euler-Lagrange expressions. Common modern formulations further specialize the
first theorem to point mechanics or field theory and differ over exact versus quasi-invariance,
boundary terms, regularity, locality, the meaning of on-shell conservation, and whether a converse
is included. The catalog selects none of these contracts.

This intake freezes that ambiguity rather than inventing missing mathematics. The provisional root
vector is `[H5, M4, R4]`. `H5` records that the supplied title and relation are not yet a stable
truth-valued proposition; it does not say that Noether's established theorems are false or open. No
source-identical usable Lean artifact or source-faithful proof reconstruction can attach before a
proposition is selected.

M. A. Tavel's English translation of Emmy Noether's *Invariante Variationsprobleme* was inspected
as a primary-text discovery lead. It exposes the finite/infinite group distinction and the direct
and converse clauses, but the repository does not cite that edition or identify one theorem as its
root. No complete transcription, incorporated-definition crosswalk, correction audit, immutable
source admission, or independent review is accepted at intake.

The repository also has the distinct target `THM-M-1515` (`诺特定理`) in mathematical physics and
a legacy `S1-M-184` Lean artifact for that target. Its prose calls the model finite-dimensional,
but its formal binders require only a real normed space. It assumes the decisive current-derivative
bridge and proves a zero-Lagrangian special case; its own comments deny terminal closure. Neither
its statement choice nor any of its evidence is inherited by `THM-M-1374`.

`IntakeProbe.lean` checks only adjacent pinned calculus and flow interfaces. It states no Noether
theorem and receives no statement or proof credit. The structured scope authority is
`instance.json`, the resolution boundary is in `scope-map.md`, the literal source crosswalk is in
`source-statement-crosswalk.md`, and all six downstream phases remain open in `task-dag.json`.

No canonical Lean expression, H0, M0, R0, accepted execution state, audit completion, theorem
completion, or master acceptance is claimed.
