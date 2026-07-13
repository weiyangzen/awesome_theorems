# THM-M-0930 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog entry named
Combinatorial Nullstellensatz. The repository attributes it to Noga Alon in 1999 but supplies only
the gloss `多项式方法在组合中的应用` ("applications of the polynomial method in combinatorics").
Its `已验证` label is untrusted inventory metadata under rev-5.6, not an exact source statement,
Lean target, or proof receipt.

The author-hosted text of Alon's 1999 paper was inspected. It says that both Theorem 1.1, the
vanishing-grid linear-combination theorem, and Theorem 1.2, the nonzero-coefficient grid
nonvanishing theorem, "may be called Combinatorial Nullstellensatz." The catalog's method gloss
does not choose either theorem or a bundle containing both. Intake therefore keeps the canonical
statement and formal target null rather than silently selecting familiar mathematics.

Pinned mathlib contains a dedicated `Mathlib.Combinatorics.Nullstellensatz` module that follows
Alon 1999. Its two principal declarations closely track the two source theorems, and the module also
contains the grid-vanishing lemma used in the proof. `IntakeProbe.lean` authenticates these pinned
interfaces and records their current axiom diagnostics. They are strong exact-topic candidates,
but source-root selection, checked source-to-Lean transports, terminal-body provenance, and trust
closure belong to later accepted phases.

The provisional vector is `[H1, M3, R4]`: a complete primary proof source and exact-topic pinned
interfaces are known, while the source root and premise mapping remain unaccepted and no
source-faithful readable reconstruction exists. `instance.json` is the structured intake authority,
and `task-dag.json` keeps all six downstream phases open. No canonical proposition, H0, M0, R0,
accepted execution state, audit completion, theorem completion, or master acceptance is claimed.
