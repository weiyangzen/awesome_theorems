# THM-M-0961 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog entry named Meshulam's
theorem. The repository says only "upper bound for cap sets," attributes the result to Roy Meshulam
in 1995, and labels it verified. Under rev-5.6 that label is untrusted inventory metadata, not a
source audit, an exact Lean proposition, or proof evidence.

The bibliographic record identifies Roy Meshulam's 1995 paper *On subsets of finite abelian groups
with no 3-term arithmetic progressions*. Liu-Spencer-Zhao (2011) explicitly identifies Meshulam's
Theorem 1.2 as `D3(G) <= 2 * |G| / c(G)` for finite odd-order abelian `G`, where `c(G)` is the number
of nontrivial cyclic factors in invariant-factor form. Bateman-Katz identifies the resulting order
`1 / N` density bound in `F_3^N`. These sources give a high-confidence provisional human target, but
they do not substitute for direct, independently reviewed inspection of the 1995 theorem. The
catalog also does not choose the general theorem or its cap-set specialization. The canonical
statement and formal target therefore remain null until the dependent statement gate.

Pinned mathlib supplies `ThreeAPFree`, `addRothNumber`, `roth_3ap_theorem`, and related finite-group
and natural-number Roth interfaces. `IntakeProbe.lean` authenticates their types. The finite-group
theorem gives a density threshold through `cornersTheoremBound`; it does not state Meshulam's
explicit `2 * |G| / c(G)` bound or define the invariant `c(G)`. It is adjacent formal
infrastructure, not root proof credit.

The provisional vector is `[H1, M4, R4]`: a matching primary paper is identified but its exact
statement, assumptions, proof boundary, corrections, and independent crosswalk remain open; no
usable exact formal artifact for the still-unfrozen root is credited; and no source-faithful
readable proof reconstruction is attached. All six downstream phases remain open. No H0, M0, R0,
accepted execution state, audit completion, theorem completion, or master acceptance is claimed.
