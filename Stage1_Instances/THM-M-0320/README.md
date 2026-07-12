# THM-M-0320 rev-5.6 intake

This directory is the fail-closed `planned` intake for Kakutani's fixed-point theorem. It freezes
the intended human theorem family: a nonempty compact convex subset of a finite-dimensional real
vector space and an upper-hemicontinuous correspondence with nonempty compact convex values admit
a point belonging to its own value. The exact primary-source formulation and its transport to the
common compact-domain formulation remain statement-phase work.

The repository source gives only “fixed-point theorem for a set-valued map”; its `已验证` label is
untrusted metadata. The provisional root vector is `[H1, M4, R4]`. No canonical Lean expression,
source acceptance, proof, audit completion, or theorem completion is claimed.

`scope-map.md` records proposition-critical choices and exclusions,
`source-statement-crosswalk.md` maps the source vocabulary to the intended Lean surface, and
`task-dag.json` keeps every downstream phase open. Intake validation is recorded in
`validation.md`.
