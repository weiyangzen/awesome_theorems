# THM-M-0928 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label
`波利亚计数定理` (Pólya enumeration theorem). The catalog supplies only the gloss
`考虑对称性的计数` ("counting while accounting for symmetry"), an attribution to George Pólya,
the year 1937, and an untrusted `已验证` label. It gives no formula, action, color inventory,
generating function, source locator, or formal declaration.

A primary bibliographic lead was identified: G. Pólya, *Kombinatorische Anzahlbestimmungen für
Gruppen, Graphen und chemische Verbindungen*, Acta Mathematica 68 (1937), 145-254,
DOI `10.1007/BF02546665`. Crossref metadata matches the catalog author and year, and points to an
open Project Euclid copy. The paper text was not obtained in this run, so no theorem/page,
assumption, proof, translation, correction, or errata crosswalk is claimed.

The familiar theorem name covers proposition-changing variants: a finite permutation group or a
more general action; unrestricted colors versus a prescribed inventory; the number of coloring
orbits versus a cycle-index substitution polynomial; and labeled versus weighted colors. Selecting
one now would silently narrow or broaden the received claim. `instance.json` therefore keeps the
canonical mathematical and Lean statements null and records `[H1, M3, R4]` only as a provisional
debt classification.

Pinned mathlib provides exact adjacent ingredients: Burnside's orbit-counting lemma, fixed-point
and orbit objects, and permutation cycle types. `IntakeProbe.lean` authenticates those APIs without
declaring or proving a Pólya root. Burnside's lemma is also the separately owned target
`THM-M-0929`; it cannot be substituted for this theorem or receive duplicate proof credit here.

`scope-map.md` freezes the formulation choices and non-substitution boundary,
`source-statement-crosswalk.md` records the repository/source/Lean relationship, and
`task-dag.json` leaves all six downstream phases open. No exact target, H0, M0, R0, accepted proof
state, audit completion, theorem completion, or master acceptance is claimed.
