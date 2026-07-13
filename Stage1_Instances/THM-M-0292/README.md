# THM-M-0292 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog item `迪尼定理`
(Dini's theorem). The repository gives Ulisse Dini, the year 1878, the gloss
`单调函数列的一致收敛` (uniform convergence of a monotone sequence of functions), and an
untrusted `已验证` label. It does not give a binder-complete proposition or proof evidence.

## Intake result

The gloss identifies the classical Dini uniform-convergence family, but it omits the hypotheses
that distinguish that theorem from a false unrestricted claim: compactness of the domain,
continuity of every function, pointwise convergence, continuity of the limit, and whether the
sequence is increasing or decreasing. It also does not say whether monotonicity is in the sequence
index or in each function's domain variable.

The catalog's 1878 date has a bibliographically matching Dini book lead: Ulisse Dini,
*Fondamenti per la teorica delle funzioni di variabili reali*, Pisa, Tipografia T. Nistri e C.,
1878. A public 430-image scan
was located, but no exact original theorem, definition chain, page span, proof, correction, or
erratum was identified or independently reviewed. A secondary encyclopedia gives a nonnegative-
series form on a closed interval; transporting it to monotone partial sums is nontrivial evidence
work, not an intake assumption. At family level, the secondary naming and this bibliographic lead
support only a provisional `H1`; the book-to-theorem relationship itself remains unverified.

## Formal boundary

Pinned mathlib directly contains `Mathlib.Topology.UniformSpace.Dini`. Its increasing and decreasing
compact-set declarations, `Monotone.tendstoUniformlyOn_of_forall_tendsto` and
`Antitone.tendstoUniformlyOn_of_forall_tendsto`, are exact-topic formal candidates. The module also
has compact-space, locally uniform, and bundled continuous-map variants, and generalizes beyond
real sequences to preorder-indexed functions valued in normed ordered lattices.

`IntakeProbe.lean` authenticates these pinned interfaces and checks their classical `ℕ`/`ℝ`
specializations without declaring the target or adding a proof body. Because the catalog and
unreviewed source lead do not yet select one variant, the canonical mathematical statement and Lean
expression remain null. The provisional vector is `[H1, M3, R4]`: a family-level human proof is
believed published but its primary mapping is unverified; kernel-visible theorem declaration
interfaces exist but the exact root is unfrozen; and no accepted
source-faithful readable proof exists.

`instance.json` is the planned scope authority, `scope-map.md` freezes proposition-changing choices,
`source-statement-crosswalk.md` records the source and Lean boundaries, and `task-dag.json` keeps all
six downstream phases open. No `H0`, `M0`, `R0`, accepted execution state, audit completion,
theorem completion, or master acceptance is claimed.
