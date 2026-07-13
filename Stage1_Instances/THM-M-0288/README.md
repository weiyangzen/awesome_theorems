# THM-M-0288 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the Vitali covering theorem. The
repository catalogue gives Giuseppe Vitali, the year 1908, and only the gloss "covering lemma and
differentiation theorem." Its `已验证` label is untrusted metadata under rev-5.6 and supplies no
source, statement, or proof credit.

The gloss does not identify one proposition. In particular, it appears to bundle a covering
selection result with a downstream differentiation result. It does not select a topological
closed-ball lemma, a measurable almost-everywhere covering theorem, a Vitali-relation formulation,
the differentiation of measures, the Lebesgue density theorem, or the Lebesgue differentiation
theorem. Nor does it specify the ambient space, measure hypotheses, fine-cover convention,
enlargement constant, countability, exact-versus-almost-everywhere coverage, differentiated object,
or conclusion. Selecting any familiar variant at intake would silently supply proposition-changing
mathematics.

A contemporary JFM/zbMATH record authenticates Vitali's 1908 paper *Sui gruppi di punti e sulle
funzioni di variabili reali* and describes an interval-family theorem used for new proofs of earlier
integral-function results. The primary text was not obtained, and modern secondary metadata
disagrees with the JFM record on pagination. An open scan of Vitali's distinct 1904 paper *Sui
gruppi di punti* concerns extension and measurability of point sets. These records corroborate the
historical family, but neither supplies a reviewed exact modern statement or bundle.

Pinned mathlib contains several strong exact-topic candidates: topological and measurable covering
theorems in `Mathlib.MeasureTheory.Covering.Vitali`, the `VitaliFamily` abstraction, differentiation
of measures through `VitaliFamily.ae_tendsto_rnDeriv`, and Lebesgue differentiation through
`VitaliFamily.ae_tendsto_average`. The intake probe authenticates those interfaces at the pinned
revision, but none is silently equated with the unfrozen catalogue root.

The provisional root vector is `[H1, M3, R4]`: a classical proved family and source leads exist but
the exact claim and source mapping remain open; usable pinned formal candidates exist but no
canonical source target or checked transport is frozen; and no source-faithful readable proof
reconstruction exists. All six downstream phases remain open in `task-dag.json`.

No canonical mathematical or Lean proposition, H0, M0, R0, accepted execution state, audit
completion, theorem completion, or master acceptance is claimed.
