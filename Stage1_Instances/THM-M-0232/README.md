# THM-M-0232 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for `鲁歇定理` (Rouché's theorem). The
repository supplies Eugène Rouché, the year 1862, and only the gloss `全纯函数零点个数比较`
("comparison of the numbers of zeros of holomorphic functions"). Its `已验证` label is untrusted
metadata and supplies no human-source or Lean proof credit.

The gloss identifies a classical theorem family, but it does not select an exact proposition. A
familiar formulation compares the zeros of `f` and `f + g` inside a closed contour under
`|g| < |f|` on the contour; another compares `f` and `g` under `|f - g| < |f|`. The catalog does
not fix the contour or domain, regularity neighborhood, strict inequality and function ordering,
zero-count representation and multiplicities, boundary-zero convention, or degenerate cases.
Selecting any textbook variant at intake would add proposition-changing mathematics.

The source catalog also gives the separate ID `THM-M-0234`, titled `儒歇定理`, with the gloss
"stability of the number of zeros of functions." That appears to overlap this theorem family, but
the two IDs may not be merged and evidence may not transfer until an independent scope review
resolves their relationship. `THM-M-0233` separately owns the argument principle.

The BnF catalog and a historical biography provide plausible leads to Rouché's 1862 *Mémoire sur
la série de Lagrange*, but no exact source page, incorporated definitions, proof passage, correction
history, or independent review is admitted. Pinned mathlib provides vanishing-order, divisor, and
circle-integral substrate. `IntakeProbe.lean` checks those APIs only; it states no target theorem.

The provisional vector is `[H1, M4, R4]`: a historically proved theorem family and source lead are
recognizable, the exact source statement is unaudited, no usable exact Lean artifact is credited,
and no source-faithful proof reconstruction can attach to an unfrozen root. `instance.json` is the
structured scope record, and all six downstream tasks remain open in `task-dag.json`. No canonical
statement, H0, M0, R0, accepted execution state, audit completion, theorem completion, accepted
receipt, or master acceptance is claimed.
