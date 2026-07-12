# THM-M-0320 rev-5.6 intake

This directory is the fail-closed `planned` dossier for Kakutani's fixed-point theorem. The
statement phase freezes and elaborates the source's closed, bounded, convex Euclidean formulation
in `Statement.lean`; `statement.md` records its boundary and minimal imports.

The repository source gives only “fixed-point theorem for a set-valued map”; its `已验证` label is
untrusted metadata. The provisional root vector remains `[H1, M4, R4]`: elaborating a proposition
does not prove it. No source acceptance, proof, audit completion, or theorem completion is claimed.

`scope-map.md` records proposition-critical choices and exclusions,
`source-statement-crosswalk.md` maps the source vocabulary to the intended Lean surface, and
`task-dag.json` keeps every downstream phase open. Intake validation is recorded in
`validation.md`.
