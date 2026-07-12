# THM-M-0770 rev-5.6 intake

This directory is the `planned` intake for Zorn's lemma: every nonempty partially ordered set in
which every chain has an upper bound has a maximal element. Here, maximal means that no strictly
larger element exists; it does not mean greatest.

The repository supplies only the gloss "existence of a maximal element in a partially ordered set,"
the attribution Max Zorn, the year 1935, and an untrusted "verified" label. Those fields omit the
chain-boundedness hypothesis and do not identify a source statement. This dossier restores the
necessary hypothesis while leaving the precise primary-source wording and the empty-chain convention
open for the statement phase. It does not silently identify this target with the separately owned
Hausdorff maximal principle or Kuratowski-Zorn target.

Pinned mathlib discovery found plausible declarations in `Mathlib.Order.Zorn`, but intake does not
select or credit one as the exact canonical target. The provisional root vector is `[H1, M3, R3]`.
No exact Lean target, source fidelity, proof credit, audit completion, or theorem completion is
claimed. `scope-map.md` fixes the mathematical boundaries, `source-statement-crosswalk.md` records
the evidence gaps, `task-dag.json` keeps all dependent work open, and `validation.md` records the
bounded checks performed.
