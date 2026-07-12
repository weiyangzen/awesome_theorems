# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` identifies Rene Thom, the year 1954, and the claim
"transverse maps are generic." `Docs/Stage0_Blueprint.md` repeats that claim but supplies no
definitions, theorem number, page, assumptions, proof source, or formal artifact. Its label
"verified" is explicitly untrusted by the rev-5.6 manifest and supplies no `H0` or machine credit.

## Candidate mathematical sources

- Rene Thom, "Quelques proprietes globales des varietes differentiables," *Commentarii
  Mathematici Helvetici* 28 (1954), 17-86. This is the historical primary-source candidate behind
  the repository attribution. The exact theorem, page, statement conventions, and relation to the
  intended ordinary mapping-space result have not yet been inspected.
- Morris W. Hirsch, *Differential Topology*, Graduate Texts in Mathematics 33, Springer (1976),
  the transversality chapter. This is a stable modern source candidate for disambiguating ordinary,
  parametric, approximation, and mapping-space formulations; exact theorem/page, edition wording,
  hypotheses, and errata remain to be checked.

These are discovery anchors only. Before `H0`, an independent reviewer must inspect a fixed edition,
record theorem and page, verify every assumption and erratum, and approve a source-to-formal row for
each binder and conclusion.

## Crosswalk

| Repository phrase | Intended mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "transverse maps" | `f` is transverse to `S` at every point over `S` | smooth manifolds, tangent spaces, derivative, tangent subspace sum | included; API open |
| "generic" | residual, hence dense under a Baire hypothesis, or another source-defined notion | topology and Baire structure on a smooth mapping space | included; exact meaning open |
| "map" | variable smooth map `M -> N` | bundled/unbundled smooth map and regularity predicate | included; representation open |
| target submanifold | smooth embedded `S subset N` | concrete embedded-submanifold predicate and tangent inclusion | included; conventions open |
| perturbation route | approximation or parameter-family argument yielding genericity | topology-aware approximation and parametric bridge | proof architecture only; not credited |

## Existing Lean boundary

A scoped text search found no target-specific module or declaration for `THM-M-0596`. Hits in
`S1_M_117.lean`, `S1_M_131.lean`, `S1_M_297.lean`, and other target dossiers merely mention
transversality as an input or future obligation; they neither state nor prove this theorem. The
statement phase must search pinned mathlib semantically after the exact source statement is fixed.
No external formalization is credited at intake.
