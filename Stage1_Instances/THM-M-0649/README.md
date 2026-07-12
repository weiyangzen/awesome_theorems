# THM-M-0649 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the elementary chain theorem,
also called the Tarski union theorem. The repository wording is frozen as follows: for a nonempty
linearly ordered increasing family of first-order structures in one language, when every earlier
structure is an elementary substructure of every later structure, the union carries the induced
structure and every member of the chain is an elementary substructure of that union.

The exact encoding of a chain whose carriers are different types is deliberately left to the
statement phase. Pinned mathlib has elementary embeddings/substructures, the Tarski-Vaught test,
directed suprema of substructures, and direct limits. `IntakeProbe.lean` checks those ingredients,
but no exact elementary-chain union declaration was located by the scoped repository search. The
probe is discovery evidence only and gives no statement or proof credit.

The lifecycle remains `planned` at `[H2, M4, R4]`. Exact primary-source pinpointing, canonical Lean
elaboration, and all later gates remain open. No accepted proof state, audit completion, or theorem
completion is claimed.
