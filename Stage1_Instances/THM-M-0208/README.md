# THM-M-0208 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for Viviani's theorem. The repository
catalog supplies the attribution Vincenzo Viviani, the year 1659, and only the gloss
`等边三角形内点到三边距离之和为常数`: for a point inside an equilateral triangle, the sum of
its distances to the three sides is constant. The catalog cites no source and fixes no definitions,
binder order, boundary cases, or formal artifact. Its `已验证` label is untrusted metadata.

The licensed MPIWG transcription of Viviani's 1659 *De maximis et minimis, geometrica divinatio*
was inspected and pinpointed at Appendix, `LEMMA II. PROP. II.`, printed pages 146-147. Its theorem
is broader: for any regular polygon and any two points inside or on its perimeter, the sums of the
perpendiculars to all sides are equal. Its area proof compares the two decompositions of the same
polygon. Thus the catalog claim is a natural strict-interior triangle specialization, but not a
literal transcription of the historical root. `primary-source-excerpt.md` preserves the locator,
Latin statement, working translation, proof boundary, license, and retrieved source hash.

Two versioned modern sources were also inspected: Abboud's arXiv paper `0903.0753v3` and Zhou's
`1008.1236v2`. They confirm the usual equilateral-triangle result and area architecture; Abboud
identifies the constant as the height. The primary text itself states point-to-point constancy, not
that altitude formula. Exact specialization and alternate-form transports, critical-edition and
errata review, translation approval, and independent source review remain open. The provisional
human-source classification is therefore `H1`, not `H0`.

Pinned mathlib provides unusually close formal infrastructure. `Affine.Simplex.Equilateral`,
strict and closed simplex interiors, simplex height, face `signedInfDist`, trilinear-coordinate
evaluation, and the conversion of absolute signed face distance to metric distance all elaborate
in `IntakeProbe.lean`. No named Viviani declaration or already packaged sum theorem was found in a
bounded local search. These are usable statement and reduction interfaces, not the canonical root
or proof, so the provisional machine classification is `M3`.

The source comparison still leaves proposition-changing choices: strict versus closed interior,
supporting lines versus finite side segments, signed versus nonnegative distance, the ambient
two-dimensional plane versus an affine span in a larger space, and whether `constant` is merely an
existential value or specifically the triangle's altitude. Intake records the standard altitude
formula only as a derived candidate supported by the modern lead and a boundary-point
specialization of the primary theorem. It does not silently adopt it.

The provisional vector is `[H1, M3, R4]`. `instance.json` is the structured scope authority, and
`task-dag.json` leaves all six downstream phases open. No canonical mathematical or Lean
statement, H0, M0, R0, accepted execution state, audit completion, theorem completion, accepted
receipt, or master acceptance is claimed.
