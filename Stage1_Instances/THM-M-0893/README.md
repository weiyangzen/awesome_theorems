# THM-M-0893 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for `THM-M-0893`, the repository's
`Bannai-Ito猜想` (Bannai-Ito conjecture). The catalog attributes it to Eiichi Bannai and Tatsuro
Ito in 1984 but gives only the gloss `距离正则图直径的界` (a bound on the diameter of
distance-regular graphs). Its `已证明` field is untrusted metadata and supplies no source or proof
credit.

## Intake result

The standard named conjecture is more precise than the catalog gloss: for each fixed valency
greater than two, there are only finitely many distance-regular graphs. Bang, Dubickas, Koolen,
and Moulton state this verbatim as Theorem 1.1 in arXiv `0909.5253v1` and prove it in the published
paper, *Advances in Mathematics* **269** (2015), 1-55, DOI
`10.1016/j.aim.2014.09.025`. Their introduction attributes the original conjecture to Bannai and
Ito, *Algebraic Combinatorics I*, p. 237 (1984).

The proof paper explains why a diameter bound depending only on fixed valency would imply the
finiteness theorem, and separately quotes Ivanov's bound `D <= F(k) h`. The repository gloss does
not say which diameter-bound formulation it means. It therefore cannot silently be replaced by an
explicit inequality, by the finiteness theorem, or by one intermediate reduction. The named root
is strongly identified, but original-source inspection, exact definition and assumption admission,
correction review, the diameter-gloss transport, and independent review remain open. Source status
is consequently `H1`, not `H0`.

## Formal boundary

`IntakeProbe.lean` elaborates the pinned finite simple-graph, connectedness, regularity, distance,
diameter, and graph-isomorphism interfaces adjacent to a future encoding. A bounded search found
no distance-regular-graph or Bannai-Ito target declaration in repo-local Lean or pinned mathlib.
Mathlib also lacks an identified distance-regular predicate, so the exact representation of
intersection numbers and finiteness up to graph isomorphism remains a statement-phase design and
source-fidelity obligation.

The canonical Lean expression remains null. The provisional vector is `[H1, M4, R4]`: the
published root and proof source are identified but not accepted as a complete source crosswalk; no
usable exact formal artifact is credited; and no source-faithful readable reconstruction is
accepted. All six downstream tasks remain open. No accepted execution state, audit completion,
theorem completion, or master acceptance is claimed.
