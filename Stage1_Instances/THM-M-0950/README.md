# THM-M-0950 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label
`Polymath项目` (Polymath project). The catalog gloss, `密度Hales-Jewett定理的组合证明`
("a combinatorial proof of the density Hales-Jewett theorem"), names a collaboration and a proof
route rather than one truth-valued proposition with fixed binders, hypotheses, conclusion, and
proof-provenance boundary. The catalog value `已验证` is untrusted metadata and supplies no proof
credit.

The matching primary source is D. H. J. Polymath, "A new proof of the density Hales-Jewett
theorem," *Annals of Mathematics* 175 (2012), 1283-1327. Its Theorem 1.4 states qualitative density
Hales-Jewett, while Theorem 1.5 records new quantitative bounds. The repository does not say
whether `THM-M-0950` owns Theorem 1.4 with a required Polymath proof provenance, Theorem 1.5, an
exact conjunction, or a correctness claim about the combinatorial proof. Moreover,
`THM-M-0949` separately owns the label "density Hales-Jewett theorem." Selecting an exact root or
sharing the underlying proposition therefore requires accountable source and duplicate-scope
review.

This intake freezes that ambiguity rather than substituting the neighboring theorem. Its
provisional vector is `[H5, M4, R4]`: `H5` classifies the supplied project/proof description as not
yet a stable proposition, not the published results as false; `M4` records that no exact Lean
target or proof artifact is credited; and `R4` records that no readable proof reconstruction can
attach to an unidentified root.

The structured scope authority is `instance.json`. `scope-map.md` and
`source-statement-crosswalk.md` preserve the exact boundary and primary-source candidates. All six
downstream phases remain open in `task-dag.json`. `IntakeProbe.lean` checks only pinned
combinatorial-line and finite-density APIs and states no theorem. Exact validation evidence is in
`validation.md` and the provisional `intake-receipt.json`.

No H0, M0, R0, accepted proof state, audit completion, theorem completion, accepted receipt, or
master acceptance is claimed.
