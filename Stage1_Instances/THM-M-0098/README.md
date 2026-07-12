# THM-M-0098 rev-5.6 intake

This directory is the `planned` intake dossier for catalog target `THM-M-0098`. The repository
record is not yet a theorem statement: its title says "Langlands program fundamental lemma", while
its only mathematical gloss says "a correspondence between automorphic representations and Galois
representations". Those phrases normally identify different theorem families.

The conflict is preserved rather than resolved by guesswork. The title branch points toward an
endoscopic orbital-integral Fundamental Lemma; the literal gloss points toward a local or global
Langlands reciprocity program. The repository already assigns those topics to separate targets
`THM-M-0434` and `THM-M-0430`, respectively, but their artifacts and state cannot be copied into
this target.

No canonical human claim or Lean proposition is frozen. The provisional intake vector is
`[H5, M4, R4]`: `H5` records that the current catalog record is not a stable proposition, not that
either candidate theorem is refuted or independent. Accepted proof state is empty, and both audit
and theorem completion are false. The
first downstream task must identify an immutable primary-source statement and reconcile the title,
gloss, attribution, date, and neighboring target ownership before selecting binders or imports.

`scope-map.md` records the two unresolved readings and explicit non-substitution boundary.
`source-statement-crosswalk.md` preserves the catalog wording and source candidates.
`task-dag.json` contains only open downstream tasks. `IntakeProbe.lean` checks adjacent pinned Lean
APIs for both readings, not either root theorem. Exact commands and results are in `validation.md`
and the provisional node receipt `intake-receipt.json`.

This dossier is worker-local planned-intake evidence pending master acceptance. It supplies no
statement, source-fidelity, proof, audit-completion, or theorem-completion credit.
