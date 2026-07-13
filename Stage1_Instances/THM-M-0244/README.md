# THM-M-0244 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog entry named the
Lindelof theorem. The repository supplies only the gloss "the Phragmen-Lindelof principle in an
angular region," attributes it to Ernst Lindelof in 1908, and labels it verified. Under rev-5.6
that label is untrusted inventory metadata, not a source-reviewed proposition or machine-proof
evidence.

The 1908 paper by E. Phragmen and Ernst Lindelof was inspected from a Zenodo copy of the published
Acta Mathematica scan. Part II, nos. 4-5, journal pages 385-387, proves closely related angular-domain
maximum principles. They vary the angular domain and the growth condition, and the paper also has
a more general opening principle. The catalog does not identify which numbered result it means,
does not name Phragmen as coauthor, and omits the angle, function, boundary, growth, and conclusion
conventions. The paper is therefore a strong primary-source lead, but no variant is silently adopted
or credited as `H0`.

Pinned mathlib contains the proof-bearing module
`Mathlib.Analysis.Complex.PhragmenLindelof`. It exposes strip, coordinate-quadrant, and right
half-plane forms. `IntakeProbe.lean` authenticates representative terminal declarations and their
types in the pinned environment. These are highly relevant formal candidates, but the catalog's
generic angular wording has not been mapped to any one of them, and the current module has no
arbitrary-angle theorem. Intake therefore grants no exact-root `M0` credit.

The provisional vector is `[H1, M3, R4]`: a primary proof source and a close pinned formal theorem
family are known, but the exact human claim and source assumptions are not accepted; related
proof-bearing Lean declarations exist but no canonical root identity or checked angular transport
is frozen; and no source-faithful readable reconstruction exists. `instance.json` freezes this
boundary, while `task-dag.json` keeps all six downstream phases open. No H0, accepted M0, R0,
accepted execution state, audit completion, theorem completion, or master acceptance is claimed.
