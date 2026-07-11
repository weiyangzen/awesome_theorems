# THM-M-0466 rev-5.6 intake

This is the `planned` intake dossier for the Manin-Mumford conjecture. The source metadata phrase
"distribution of torsion points on curves" is only a gloss. The frozen human claim is the standard
Raynaud theorem: if a closed subvariety of an abelian variety over an algebraically closed field of
characteristic zero contains a Zariski-dense set of torsion points, then it is a finite union of
torsion translates of abelian subvarieties. Equivalently, its torsion points lie in such a finite
union. The curve formulation is a specialization, not the root statement.

No exact Lean expression is claimed at intake. `instance.json` records the scope boundary,
`scope-map.md` separates the root from variants and degenerate cases, and
`source-statement-crosswalk.md` identifies the primary proof source and the audit still required.
The open phase DAG is in `task-dag.json`.

## Intake verdict

Lifecycle is `planned`, with provisional root vector `[H1, M4, R4]`. Human proof existence is
anchored to Raynaud's 1983 paper, but edition/page-level premise and errata review is not complete.
The machine statement, imports, environment fingerprint, transports, and all proof evidence remain
open. `audit_complete=false` and `theorem_complete=false`.

