# THM-M-0183 rev-5.6 intake

This is the `planned` intake for the Calabi conjecture proved by Yau. The repository gloss is the
Ricci-flat corollary: a compact Kahler manifold with vanishing real first Chern class admits a
Ricci-flat Kahler metric in each prescribed Kahler class. The prescribed-class clause is retained;
dropping it would silently weaken the classical result. Uniqueness and the full prescribed-Ricci-
form theorem are source-side strengthening/context and are not credited to this root at intake.

`Statement.lean` now freezes and kernel-elaborates that proposition against explicit typed
interfaces for notions absent from pinned mathlib. This statement gate is pending master acceptance
and claims no proof or native geometry transport. The provisional vector remains `[H2, M4, R4]`:
the primary sources are identified, but exact edition/page/errata review, native API integration,
and the proof remain open.

`scope-map.md` freezes the human boundary, `source-statement-crosswalk.md` records source fidelity,
and `task-dag.json` records the downstream work. Intake evidence is in `validation.md`; statement
evidence is in `statement-validation.md` and `statement.json`.
